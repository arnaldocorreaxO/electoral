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
 
    var select_manzanas = $('select[name="manzana"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    // alert(token.val())

    $('select[name="barrio"]').on('change', function () {
        var id = $(this).val();
        var options = '<option value="">--------------</option>';
        if (id === '') {
            select_manzanas.html(options);
            return false;
        }
        $.ajax({
            headers: { "X-CSRFToken": token.val() },            
            // url: window.location.pathname,
            url: '/electoral/elector/add/',
            type: 'POST',
            data: {
                'action': 'search_manzana_id',
                'id': id
            },
            dataType: 'json',
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                select_manzanas.html('').select2({
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

    select_manzanas.on('change', function () {
        var value = select_manzanas.select2('data')[0];
        console.log(value);
    });
});