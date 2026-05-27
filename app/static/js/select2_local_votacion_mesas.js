/* ===================================================================
Author: xO
Refactored: API Select2 unificada para el change_form de Django Admin
Manejo dinámico de Local de Votación -> Mesas (Blindado contra doble Ajax)
==================================================================== */
$(function () {
  // 1. Inicialización Base de Select2 en el Admin de Django
  var select2Config = {
    theme: "bootstrap4",
    language: "es",
    allowClear: true,
    placeholder: {
      id: "",
      text: "(Todos)",
    },
  };

  $(".select2").select2(select2Config);

  var select_mesas = $('select[name="mesa"]');
  var token = $('input[name="csrfmiddlewaretoken"]');

  // Bandera de control para evitar colisiones o ejecuciones simultáneas
  var isAjaxRunning = false;

  // Cambiamos 'change' por 'select2:select' y 'select2:unselect' para capturar la
  // acción pura del usuario sobre la interfaz y no los rebotes del DOM nativo.
  $('select[name="local_votacion"]').on(
    "select2:select select2:unselect change",
    function (e) {
      // Si el evento es el 'change' interno/automático de Select2 y no una acción directa, lo ignoramos
      if (e.namespace === "select2") return;

      var id = $(this).val();

      // Vaciamos Select2 de forma limpia antes de arrancar
      select_mesas
        .empty()
        .append(new Option("(Todos)", "", true, true))
        .trigger("change.select2");

      if (id === "") {
        return false;
      }

      // Si ya hay una petición en curso, abortamos esta para evitar duplicados
      if (isAjaxRunning) {
        return false;
      }

      // Encendemos el bloqueo
      isAjaxRunning = true;

      $.ajax({
        headers: { "X-CSRFToken": token.val() },
        url: "/electoral/elector/add/",
        type: "POST",
        data: {
          action: "search_mesa_id",
          id: id,
        },
        dataType: "json",
      })
        .done(function (data) {
          // Volvemos a asegurar que la lista esté limpia justo antes de inyectar
          select_mesas.empty().append(new Option("(Todos)", "", true, true));

          if (!data.hasOwnProperty("error")) {
            // Iteramos los datos e inyectamos nuevas opciones
            $.each(data, function (index, item) {
              var option = new Option(item.text, item.id, false, false);
              select_mesas.append(option);
            });

            // Refrescamos visualmente Select2 de forma controlada con su namespace
            select_mesas.trigger("change.select2");
            return false;
          }

          if (typeof message_error === "function") {
            message_error(data.error);
          } else {
            alert("Error: " + data.error);
          }
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
          console.error("Error en peticion de mesas:", textStatus, errorThrown);
        })
        .always(function () {
          // Apagamos la bandera para permitir futuras consultas al cambiar de local
          isAjaxRunning = false;
        });
    },
  );

  // Monitoreo de cambio de mesa
  select_mesas.on("change.select2", function () {
    var selectedData = $(this).select2("data");
    if (selectedData && selectedData.length > 0) {
      console.log("Mesa seleccionada:", selectedData[0]);
    }
  });
});
