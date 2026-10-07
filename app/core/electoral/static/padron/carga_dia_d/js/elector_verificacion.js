/*
 * Verificación de elector antes de cargarlo en la tabla del puesto de control.
 *
 * Uso:
 *   ElectorVerificacion.init({
 *       input: $('input[name="searchElector"]'),
 *       button: $('.btnConsultarElector'),  // opcional: botón que dispara la búsqueda
 *       url: pathname,
 *       statusField: 'pasoxpc',            // campo que indica si ya fue cargado
 *       statusMessage: 'YA PASÓ POR PC',
 *       onConfirm: function (elector) { addElector(elector.id); }
 *   });
 */
var ElectorVerificacion = (function ($) {
    var cfg = {};
    var $modal;
    var electores = [];
    var selected = null;
    var busy = false;

    function textOrDash(value) {
        return (value === null || value === undefined || value === '') ? '-' : value;
    }

    function setTitle(text) {
        $modal.find('.verificar-titulo').text(text);
    }

    function isAlreadyLoaded(elector) {
        return cfg.statusField && elector[cfg.statusField] === 'S';
    }

    function hasPago(elector) {
        return cfg.pagoField && elector[cfg.pagoField] === 'S';
    }

    function validHex(value) {
        return /^#[0-9A-Fa-f]{6}$/.test(value || '') ? value : null;
    }

    function contrastColor(hex) {
        var r = parseInt(hex.substr(1, 2), 16), g = parseInt(hex.substr(3, 2), 16), b = parseInt(hex.substr(5, 2), 16);
        return (r * 299 + g * 587 + b * 114) / 1000 > 150 ? '#000000' : '#FFFFFF';
    }

    function localColors(elector) {
        var bg = validHex(elector.local_votacion_color) || '#6C757D';
        return {bg: bg, fg: validHex(elector.local_votacion_text_color) || contrastColor(bg)};
    }

    function pagoBadge() {
        return $('<span class="badge badge-success ml-1">').attr('title', cfg.pagoMessage)
            .append('<i class="fas fa-dollar-sign"></i>');
    }

    function showList() {
        selected = null;
        var $body = $modal.find('.verificar-lista-body').empty();
        $.each(electores, function (index, elector) {
            var $tr = $('<tr>').attr('data-index', index).css('cursor', 'pointer');
            $tr.append($('<td>').text(textOrDash(elector.ci)));
            var $name = $('<td>').text(elector.fullname);
            if (isAlreadyLoaded(elector)) {
                $name.append(' ').append($('<span class="badge badge-warning">').text(cfg.statusMessage));
            }
            if (hasPago(elector)) {
                $name.append(pagoBadge());
            }
            $tr.append($name);
            var colors = localColors(elector);
            $tr.append($('<td>').append(
                $('<span class="badge d-inline-block text-wrap text-left">')
                    .css({'background-color': colors.bg, 'color': colors.fg, 'font-size': '.85rem'})
                    .text(textOrDash(elector.local_votacion_denominacion))
            ));
            $tr.append($('<td class="text-center h5 font-weight-bold mb-0">').text(textOrDash(elector.mesa)));
            $tr.append($('<td class="text-center h5 font-weight-bold mb-0">').text(textOrDash(elector.orden)));
            $tr.append($('<td class="text-center">').append(
                $('<button type="button" class="btn btn-primary btn-xs btn-flat verificar-btn-seleccionar" title="Seleccionar">')
                    .append('<i class="fas fa-hand-pointer"></i>')
            ));
            $body.append($tr);
        });

        $modal.find('.verificar-total').text(cfg.lastTotal);
        var $limite = $modal.find('.verificar-limite');
        if (cfg.lastTotal > electores.length) {
            $limite.text('Se muestran los primeros ' + electores.length +
                ' resultados. Refine la búsqueda para mayor precisión.').show();
        } else {
            $limite.hide();
        }

        setTitle('Seleccione el Elector');
        $modal.find('.verificar-detalle, .verificar-btn-volver, .verificar-btn-confirmar').hide();
        $modal.find('.verificar-lista').show();
    }

    function showDetail(elector, fromList) {
        selected = elector;
        $modal.find('.verificar-detalle [data-field]').each(function () {
            var field = $(this).data('field');
            $(this).text(textOrDash(elector[field]));
        });

        var colors = localColors(elector);
        $modal.find('.verificar-local').css({'background-color': colors.bg, 'color': colors.fg});

        var $pago = $modal.find('.verificar-pago');
        $pago.find('.verificar-pago-texto').text(cfg.pagoMessage || '');
        $pago.toggle(!!hasPago(elector));

        var $alert = $modal.find('.verificar-ya-paso');
        var $confirm = $modal.find('.verificar-btn-confirmar');
        if (isAlreadyLoaded(elector)) {
            $alert.find('span').text(cfg.statusMessage);
            $alert.show();
            $confirm.prop('disabled', true);
        } else {
            $alert.hide();
            $confirm.prop('disabled', false);
        }

        setTitle('Verificación de Elector');
        $modal.find('.verificar-lista').hide();
        $modal.find('.verificar-detalle').show();
        $modal.find('.verificar-btn-volver').toggle(!!fromList);
        $confirm.show();
        if (!$confirm.prop('disabled')) {
            $confirm.trigger('focus');
        }
    }

    function open(params) {
        if (busy) {
            return;
        }
        if (cfg.beforeSearch() === false) {
            return;
        }
        busy = true;
        $.ajax({
            url: cfg.url,
            type: 'POST',
            dataType: 'json',
            data: $.extend({'action': 'verify_elector'}, params)
        }).done(function (response) {
            if (response.hasOwnProperty('error')) {
                message_warning(response.error);
                return;
            }
            electores = response.electores || [];
            cfg.lastTotal = response.total || 0;
            if (!electores.length) {
                message_warning(response.mode === 'ci'
                    ? 'No se encontró ningún elector con la cédula ingresada'
                    : 'No se encontraron electores con el nombre ingresado');
                return;
            }
            if (cfg.input.data('ui-autocomplete')) {
                cfg.input.autocomplete('close');
            }
            if (electores.length === 1) {
                showDetail(electores[0], false);
            } else {
                showList();
            }
            $modal.modal('show');
        }).fail(function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown + ' ' + textStatus);
        }).always(function () {
            busy = false;
        });
    }

    function search(term) {
        term = $.trim(term || '');
        if (!term.length) {
            return;
        }
        open({'term': term});
    }

    function init(options) {
        cfg = $.extend({
            input: null,
            button: null,
            url: window.location.pathname,
            statusField: null,
            statusMessage: 'YA FUE CARGADO',
            pagoField: null,
            pagoMessage: 'YA PASÓ POR GS',
            // Devolver false para cancelar la consulta (ej. falta un dato previo).
            beforeSearch: function () { return true; },
            onConfirm: function () {}
        }, options);
        $modal = $('#modal-verificar-elector');

        if (cfg.button && cfg.button.length) {
            cfg.button.on('click', function () {
                var term = $.trim(cfg.input.val());
                if (!term.length) {
                    message_warning('Ingrese un número de cédula o nombre y/o apellido');
                    cfg.input.trigger('focus');
                    return;
                }
                search(term);
            });
        }

        // ENTER en el buscador: si el autocompletado tiene un ítem activo lo maneja él.
        cfg.input.on('keydown', function (e) {
            if (e.which !== 13 || e.isDefaultPrevented()) {
                return;
            }
            e.preventDefault();
            search($(this).val());
        });

        $modal.on('click', '.verificar-lista-body tr', function () {
            showDetail(electores[$(this).data('index')], true);
        });

        $modal.on('click', '.verificar-btn-volver', function () {
            showList();
        });

        $modal.on('click', '.verificar-btn-confirmar', function () {
            if (!selected || $(this).prop('disabled')) {
                return;
            }
            var elector = selected;
            $(this).prop('disabled', true);
            $modal.modal('hide');
            cfg.onConfirm(elector);
            cfg.input.val('');
        });

        $modal.on('shown.bs.modal', function () {
            if (cfg.input.data('ui-autocomplete')) {
                cfg.input.autocomplete('disable');
            }
            var $confirm = $modal.find('.verificar-btn-confirmar');
            if ($confirm.is(':visible') && !$confirm.prop('disabled')) {
                $confirm.trigger('focus');
            }
        });

        $modal.on('hidden.bs.modal', function () {
            selected = null;
            if (cfg.input.data('ui-autocomplete')) {
                cfg.input.autocomplete('enable');
            }
            cfg.input.trigger('focus');
        });
    }

    return {
        init: init,
        search: search,
        openById: function (id) {
            open({'id': id});
        }
    };
})(jQuery);
