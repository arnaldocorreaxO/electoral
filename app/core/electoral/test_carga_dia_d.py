import json
from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.template.loader import get_template
from django.test import RequestFactory, SimpleTestCase

from core.electoral.forms import LocalVotacionForm
from core.electoral.models import Elector, LocalVotacion
from core.security.models import Dashboard
from core.electoral.views.padron.carga_dia_d.views import (
    CargaDiaDElectorView,
    CargaDiaDElectorViewGs,
    CargaDiaDListView,
)


class CargaDiaDTestBase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.elector = Elector(
            id=1,
            ci=1234567,
            nombre="Ana",
            apellido="Perez",
            fecha_nacimiento=date(1990, 1, 2),
            fecha_afiliacion=date(2010, 3, 4),
            fecha_inscripcion=date(2026, 10, 7),
            fec_modificacion=datetime(2026, 10, 7, 11, 47, 24),
        )

    def post(self, view_class, parameters):
        request = self.factory.post("/electoral/carga_dia_d_list_gs", parameters)
        request.user = SimpleNamespace(distrito=1)
        queryset = MagicMock()
        queryset.annotate.return_value = queryset
        queryset.filter.return_value = queryset
        queryset.extra.return_value = queryset
        queryset.order_by.return_value = queryset
        queryset.select_related.return_value = queryset
        queryset.__getitem__.return_value = queryset
        queryset.__iter__.return_value = iter([self.elector])
        queryset.count.return_value = 1
        self.queryset = queryset
        with patch(
            "core.electoral.views.padron.carga_dia_d.views.Elector.objects",
            queryset,
        ):
            return view_class.as_view()(request)

    def assert_elector(self, item):
        self.assertEqual(item["fecha_inscripcion"], "2026-10-07")
        self.assertEqual(item["fecha_nacimiento"], "02/01/1990")
        self.assertEqual(item["fecha_afiliacion"], "04/03/2010")
        self.assertEqual(item["fec_modificacion"], "07/10/2026 11:47:24")
        self.assertEqual(item["fullname"], "Perez, Ana")
        self.assertEqual(item["ci"], 1234567)


class CargaDiaDSerializationTests(CargaDiaDTestBase):
    def test_search_returns_array_with_serializable_dates(self):
        for view_class, action in (
            (CargaDiaDListView, "search"),
            (CargaDiaDElectorView, "search_elector"),
            (CargaDiaDElectorViewGs, "search_elector"),
        ):
            with self.subTest(view=view_class.__name__):
                response = self.post(
                    view_class,
                    {
                        "action": action,
                        "term": "1234567",
                        "local_votacion": "1",
                        "mesa": "1",
                    },
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["Content-Type"], "application/json")
                payload = json.loads(response.content)
                self.assertIsInstance(payload, list)
                self.assertEqual(len(payload), 1)
                self.assert_elector(payload[0])

    def test_paginated_search_preserves_datatable_response(self):
        for view_class, action in (
            (CargaDiaDListView, "search_pasoxmv"),
            (CargaDiaDElectorView, "search_pasoxpc"),
            (CargaDiaDElectorViewGs, "search_pasoxgs"),
        ):
            with self.subTest(view=view_class.__name__):
                response = self.post(
                    view_class,
                    {
                        "action": action,
                        "start": "0",
                        "length": "10",
                        "search[value]": "",
                        "local_votacion": "1",
                        "mesa": "1",
                    },
                )
                self.assertEqual(response.status_code, 200)
                payload = json.loads(response.content)
                self.assertEqual(payload["page"], 1)
                self.assertEqual(payload["per_page"], 10)
                self.assertEqual(payload["recordsTotal"], 1)
                self.assertEqual(payload["recordsFiltered"], 1)
                self.assert_elector(payload["data"][0])

    def test_null_registration_date_remains_null(self):
        self.elector.fecha_inscripcion = None
        response = self.post(
            CargaDiaDElectorViewGs,
            {"action": "search_elector", "term": "1234567"},
        )
        self.assertIsNone(json.loads(response.content)[0]["fecha_inscripcion"])

    def test_empty_search_remains_an_empty_array(self):
        response = self.post(
            CargaDiaDElectorViewGs,
            {"action": "search_elector", "term": ""},
        )
        self.assertEqual(json.loads(response.content), [])

    def test_invalid_action_preserves_error_response(self):
        response = self.post(CargaDiaDElectorViewGs, {"action": "invalid"})
        self.assertIn("error", json.loads(response.content))

class ElectorVerificacionTests(CargaDiaDTestBase):
    VIEWS = (CargaDiaDElectorView, CargaDiaDElectorViewGs)

    def setUp(self):
        super().setUp()
        self.elector.mesa = "12"
        self.elector.orden = "34"
        self.elector.local_votacion = LocalVotacion(id=3, denominacion="Escuela Central")

    def verify(self, view_class, **params):
        response = self.post(view_class, dict(action="verify_elector", **params))
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content)

    def test_search_by_ci_accepts_dots_and_returns_full_data(self):
        for view_class in self.VIEWS:
            with self.subTest(view=view_class.__name__):
                payload = self.verify(view_class, term=" 1.234.567 ")
                self.assertEqual(payload["mode"], "ci")
                self.assertEqual(payload["total"], 1)
                self.queryset.filter.assert_any_call(ci=1234567)
                elector = payload["electores"][0]
                self.assertEqual(elector["fullname"], "Perez, Ana")
                self.assertEqual(elector["local_votacion_denominacion"], "3 - Escuela Central")
                self.assertEqual(elector["local_votacion_color"], LocalVotacion.COLORES_DEFECTO[3])
                self.assertIn(elector["local_votacion_text_color"], ("#000000", "#FFFFFF"))
                self.assertEqual(elector["mesa"], "12")
                self.assertEqual(elector["orden"], "34")
                self.assertEqual(elector["pasoxpc"], "N")
                self.assertEqual(elector["pasoxgs"], "N")

    def test_search_by_id(self):
        payload = self.verify(CargaDiaDElectorViewGs, id="1")
        self.assertEqual(payload["mode"], "id")
        self.queryset.filter.assert_any_call(id=1)

    def test_search_by_name_filters_each_token_and_ranks_prefix(self):
        payload = self.verify(CargaDiaDElectorView, term="per  ana")
        self.assertEqual(payload["mode"], "nombre")
        q_filters = [
            c[0][0] for c in self.queryset.filter.call_args_list
            if c[0] and isinstance(c[0][0], Q)
        ]
        self.assertEqual(len(q_filters), 2)
        self.assertIn(("nombre__icontains", "per"), q_filters[0].children)
        self.assertIn(("apellido__icontains", "ana"), q_filters[1].children)
        self.assertTrue(self.queryset.annotate.called)
        self.queryset.order_by.assert_called_with("_rank", "apellido", "nombre")

    def test_invalid_term_returns_error(self):
        payload = self.verify(CargaDiaDElectorView, term="...")
        self.assertIn("error", payload)

    def test_modal_template_is_included(self):
        html = get_template("padron/carga_dia_d/modal_verificar_elector.html").render({})
        self.assertIn('id="modal-verificar-elector"', html)
        self.assertIn("verificar-btn-confirmar", html)
        for name in ("pc", "gs"):
            source = get_template(
                "padron/carga_dia_d/list_carga_dia_d_elector_%s.html" % name
            ).template.source
            self.assertIn("modal_verificar_elector.html", source)
            self.assertIn("elector_verificacion.js", source)
            self.assertIn("btnConsultarElector", source)
            self.assertIn("Consultar Elector", source)

    def test_modal_uses_dashboard_theme_color(self):
        template = get_template("padron/carga_dia_d/modal_verificar_elector.html")
        themed = template.render({"dshboard": Dashboard(card="card-danger", navbar="navbar-dark navbar-danger")})
        self.assertIn("modal-header bg-danger", themed)
        self.assertIn("btn bg-danger btn-flat verificar-btn-confirmar", themed)
        self.assertNotIn("bg-primary", themed)
        self.assertIn("modal-header bg-primary", template.render({}))

    def test_modal_has_local_highlight_and_pago_indicator(self):
        html = get_template("padron/carga_dia_d/modal_verificar_elector.html").render({})
        self.assertIn("verificar-local", html)
        self.assertIn("verificar-pago", html)
        self.assertIn("fa-dollar-sign", html)
        pc_js = open(finders.find("padron/carga_dia_d/js/list_carga_dia_d_elector_pc.js"), encoding="utf-8").read()
        gs_js = open(finders.find("padron/carga_dia_d/js/list_carga_dia_d_elector_gs.js"), encoding="utf-8").read()
        self.assertIn("pagoField: 'pasoxgs'", pc_js)
        self.assertNotIn("pagoField", gs_js)

    def test_gs_requires_monto_before_search(self):
        gs_js = open(finders.find("padron/carga_dia_d/js/list_carga_dia_d_elector_gs.js"), encoding="utf-8").read()
        self.assertIn("beforeSearch: validarMonto", gs_js)
        for monto in ("", "  "):
            with self.subTest(monto=monto):
                payload = json.loads(self.post(
                    CargaDiaDElectorViewGs, {"action": "edit_pasoxgs", "id": "1", "monto": monto}
                ).content)
                self.assertIn("monto", payload["error"])
                self.queryset.get.assert_not_called()


class LocalVotacionColorTests(SimpleTestCase):
    def test_configured_color_and_contrast(self):
        self.assertEqual(LocalVotacion(id=1, color="#ffff00").get_color(), "#FFFF00")
        self.assertEqual(LocalVotacion(id=1, color="#FFFF00").get_text_color(), "#000000")
        self.assertEqual(LocalVotacion(id=1, color="#000080").get_text_color(), "#FFFFFF")

    def test_default_color_by_id(self):
        palette = LocalVotacion.COLORES_DEFECTO
        self.assertEqual(LocalVotacion(id=2).get_color(), palette[2])
        self.assertEqual(LocalVotacion(id=len(palette) + 2).get_color(), palette[2])

    def test_color_validator_rejects_invalid_hex(self):
        field = LocalVotacion._meta.get_field("color")
        field.clean("#1a2B3c", None)
        for invalid in ("red", "#12345", "#GGGGGG"):
            with self.assertRaises(ValidationError):
                field.clean(invalid, None)

    def test_form_uses_color_picker_with_initial_color(self):
        form = LocalVotacionForm(instance=LocalVotacion(id=4))
        self.assertEqual(form.fields["color"].widget.input_type, "color")
        self.assertEqual(form.initial["color"], LocalVotacion.COLORES_DEFECTO[4])


class DashboardThemeColorTests(SimpleTestCase):
    def test_theme_color_from_card_then_navbar(self):
        self.assertEqual(Dashboard(card="card-danger", navbar="navbar-dark navbar-info").get_theme_color(), "danger")
        self.assertEqual(Dashboard(card="card-maroon").get_theme_color(), "maroon")
        self.assertEqual(Dashboard(card="card-outline", navbar="navbar-dark navbar-success").get_theme_color(), "success")
        self.assertEqual(Dashboard(card=" ", navbar="navbar-light navbar-warning").get_theme_color(), "warning")
        self.assertEqual(Dashboard(card=" ", navbar="navbar-expand navbar-dark").get_theme_color(), "primary")
