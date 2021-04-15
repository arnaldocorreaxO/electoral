

$(function () {    
 
    var select_manzanas = $('select[name="manzana"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    alert(token.val())

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

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
            url: '/electoral/padron/elector/add/',
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
                /*$.each(data, function (key, value) {
                    options += '<option value="' + value.id + '">' + value.name + '</option>';
                });*/
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


document.addEventListener('DOMContentLoaded', function (e) {
            const form = document.getElementById('frmForm');
            const fv = FormValidation.formValidation(form, {
                    locale: 'es_ES',
                    localization: FormValidation.locales.es_ES,
                    plugins: {
                        trigger: new FormValidation.plugins.Trigger(),
                        submitButton: new FormValidation.plugins.SubmitButton(),
                        bootstrap: new FormValidation.plugins.Bootstrap(),
                        icon: new FormValidation.plugins.Icon({
                            valid: 'fa fa-check',
                            invalid: 'fa fa-times',
                            validating: 'fa fa-refresh',
                        }),
                    },
                    fields: {
                        denominacion: {
                            validators: {
                                notEmpty: {},
                                stringLength: {
                                    min: 2,
                                },
                                remote: {
                                    url: pathname,
                                    data: function () {
                                        return {
                                            obj: form.querySelector('[name="denominacion"]').value,
                                            type: 'denominacion',
                                            action: 'validate_data'
                                        };
                                    },
                                    message: 'El nombre ya se encuentra registrado',
                                    method: 'POST'
                                }
                            }
                        }
                    },
                }
            )
                .on('core.element.validated', function (e) {
                    if (e.valid) {
                        const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                        if (groupEle) {
                            FormValidation.utils.classSet(groupEle, {
                                'has-success': false,
                            });
                        }
                        FormValidation.utils.classSet(e.element, {
                            'is-valid': false,
                        });
                    }
                    const iconPlugin = fv.getPlugin('icon');
                    const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
                    iconElement && (iconElement.style.display = 'none');
                })
                .on('core.validator.validated', function (e) {
                    if (!e.result.valid) {
                        const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                        messages.forEach((messageEle) => {
                            const validator = messageEle.getAttribute('data-validator');
                            messageEle.style.display = validator === e.validator ? 'block' : 'none';
                        });
                    }
                })
                .on('core.form.valid', function () {
                    submit_formdata_with_ajax_form(fv);
                });
        });
        