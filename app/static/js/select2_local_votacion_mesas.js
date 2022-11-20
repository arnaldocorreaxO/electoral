/*
===================================================================
Author: xO
C:\Users\arnaldo\proyectos\electoral\.env\Lib\site-packages\django\
contrib\admin\templates\admin\change_form.html
Se utiliza para modificar el comportamiento de todos los SELECT en 
el Administrador de Django
En ese path se referencia a este js para Select2 Anidado de Barrios 
y Manzanas
====================================================================
*/
$(function () {
    
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
 
    var select_mesas = $('select[name="mesa"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    // alert(token.val())

    $('select[name="local_votacion"]').on('change', function () {
        var id = $(this).val();
        var options = '<option value="">--------------</option>';
        if (id === '') {
            select_mesas.html(options);
            return false;
        }
        $.ajax({
            headers: { "X-CSRFToken": token.val() },            
            // url: window.location.pathname,
            url: '/electoral/elector/add/',
            type: 'POST',
            data: {
                'action': 'search_mesa_id',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                select_mesas.html('').select2({
                    theme: "bootstrap4",
                    language: 'es',
                    data: data                    
                });
                return false;
            }
            message_error(data.error);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {
            //select_manzanas.html(options);
        });
    });

    select_mesas.on('change', function () {
        var value = select_mesas.select2('data')[0];
        console.log(value);
    });
});