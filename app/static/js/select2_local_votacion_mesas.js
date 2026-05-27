/* ===================================================================
Author: xO
Refactored: API Select2 unificada para el change_form de Django Admin
Manejo dinámico de Local de Votación -> Mesas
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

  $('select[name="local_votacion"]').on("change", function () {
    var id = $(this).val();

    // Vaciamos Select2 de forma nativa sin romper la instancia visual
    select_mesas
      .empty()
      .append(new Option("(Todos)", "", true, true))
      .trigger("change.select2");

    if (id === "") {
      return false;
    }

    $.ajax({
      headers: { "X-CSRFToken": token.val() },
      // Usamos la URL actual del navegador para que sirva tanto en ADD como en CHANGE (Edit)
      url: "/electoral/elector/add/",
      type: "POST",
      data: {
        action: "search_mesa_id",
        id: id,
      },
      dataType: "json",
    })
      .done(function (data) {
        if (!data.hasOwnProperty("error")) {
          // Iteramos los datos e inyectamos nuevas opciones usando la API oficial
          $.each(data, function (index, item) {
            // item.text e item.id deben venir formateados desde el backend (JsonVertical/Diccionario)
            var option = new Option(item.text, item.id, false, false);
            select_mesas.append(option);
          });

          // Refrescamos visualmente Select2 una sola vez al terminar el bucle
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
      });
  });

  // Monitoreo de cambio de mesa (Mantiene la consistencia del log)
  select_mesas.on("change", function () {
    var selectedData = $(this).select2("data");
    if (selectedData && selectedData.length > 0) {
      console.log("Mesa seleccionada:", selectedData[0]);
    }
  });
});
