var fv;

document.addEventListener('DOMContentLoaded', function (e) {
    const passwordMeter = document.getElementById('strengthBar');

    const randomNumber = function (min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    };
    const form = document.getElementById('frmChangePassword');
    fv = FormValidation.formValidation(form, {
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
                passwordStrength: new FormValidation.plugins.PasswordStrength({
                    field: 'password',
                    message: 'La contraseña es débil',
                    minimalScore: 3,
                    onValidated: function (valid, message, score) {
                        switch (score) {
                            case 0:
                                passwordMeter.style.width = randomNumber(1, 20) + '%';
                                passwordMeter.style.backgroundColor = '#ff4136';
                            case 1:
                                passwordMeter.style.width = randomNumber(20, 40) + '%';
                                passwordMeter.style.backgroundColor = '#ff4136';
                                break;
                            case 2:
                                passwordMeter.style.width = randomNumber(40, 60) + '%';
                                passwordMeter.style.backgroundColor = '#ff4136';
                                break;
                            case 3:
                                passwordMeter.style.width = randomNumber(60, 80) + '%';
                                passwordMeter.style.backgroundColor = '#ffb700';
                                break;
                            case 4:
                                passwordMeter.style.width = '100%';
                                passwordMeter.style.backgroundColor = '#19a974';
                                break;
                            default:
                                break;
                        }
                    },
                }),
            },
            fields: {
                password: {
                    validators: {
                        notEmpty: {
                            message: 'El password es requerido'
                        },
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: 'El password es requerido'
                        },
                        identical: {
                            compare: function () {
                                return form.querySelector('[name="password"]').value;
                            },
                            message: 'La contraseña y su confirmación no son las mismas.'
                        }
                    }
                },

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
            var parameters = {};
            $.each($(fv.form).serializeArray(), function (key, item) {
                parameters[item.name] = item.value;
            });
            submit_with_ajax('Alerta', '¿Estas seguro de cambiar tu password?', pathname, parameters, function () {
                alert_sweetalert('success', 'Alerta', 'Tu clave ha sido cambiada satisfactoriamente', function () {
                    //submitButton.removeAttribute('disabled');
                    location.href = fv.form.getAttribute('data-url');
                }, 5000, null);
            });
        });
});

$(function () {

    $('.btnShowPassword').on('click', function () {
        var i = $(this).find('i');
        var input = $(this).parent().parent().find('input');
        if (i.hasClass('fa fa-eye-slash')) {
            i.removeClass();
            i.addClass('fa fa-eye');
            input.attr('type', 'password');
        } else {
            i.removeClass();
            i.addClass('fa fa-eye-slash');
            input.attr('type', 'text');
        }
    });

    fv.revalidateField('password')
        .then(function (status) {
            fv.resetForm(true);
        });
});


