var current_date;

var fvSale;
var fvClient;

var select_client;
var input_birthdate;
var select_paymentcondition;
var select_paymentmethod;
var input_cash;
var input_cardnumber;
var input_amountdebited;
var input_titular;
var input_change;

var tblSearchProducts;
var tblProducts;

var input_searchclient;
var input_searchproducts;
var input_endcredit;
var inputs_vents;

var vents = {
    details: {
        client: '',
        end_credit: '',
        payment_method: '',
        payment_condition: '',
        type_voucher: '',
        subtotal: 0.00,
        iva: 0.00,
        total_iva: 0.00,
        dscto: 0.00,
        total_dscto: 0.00,
        total: 0.00,
        cash: 0.00,
        change: 0.00,
        card_number: 0.00,
        titular: 0.00,
        amount_debited: 0.00,
        products: [],
    },
    calculate_invoice: function () {
        var total = 0.00;
        $.each(this.details.products, function (i, item) {
            item.pos = i;
            item.cant = parseInt(item.cant);
            item.subtotal = item.cant * parseFloat(item.price_current);
            item.total_dscto = (parseFloat(item.dscto) / 100) * item.subtotal;
            item.total = item.subtotal - item.total_dscto;
            console.log(item);
            total += item.total;
        });

        vents.details.subtotal = total;
        vents.details.dscto = parseFloat($('input[name="dscto"]').val());
        vents.details.total_dscto = vents.details.subtotal * (vents.details.dscto / 100);
        vents.details.total_iva = vents.details.subtotal * (vents.details.iva / 100);
        vents.details.total = vents.details.subtotal + vents.details.total_iva - vents.details.total_dscto;

        $('input[name="subtotal"]').val(vents.details.subtotal.toFixed(2));
        $('input[name="iva"]').val(vents.details.iva.toFixed(2));
        $('input[name="total_iva"]').val(vents.details.total_iva.toFixed(2));
        $('input[name="total_dscto"]').val(vents.details.total_dscto.toFixed(2));
        $('input[name="total"]').val(vents.details.total.toFixed(2));
    },
    list_products: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            //responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {data: "id"},
                {data: "name"},
                //{data: "category.name"},
                {data: "stock"},
                {data: "cant"},
                {data: "price_current"},
                {data: "subtotal"},
                {data: "dscto"},
                {data: "total_dscto"},
                {data: "total"},
            ],
            columnDefs: [
                {
                    targets: [2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.category.inventoried) {
                            if (row.stock > 0) {
                                return '<span class="badge badge-success">' + row.stock + '</span>';
                            }
                            return '<span class="badge badge-danger">' + row.stock + '</span>';
                        }
                        return '<span class="badge badge-secondary">Sin stock</span>';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" style="width: 100px;" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" style="width: 100px;" autocomplete="off" name="dscto_unitary" value="' + row.dscto + '">';
                    }
                },
                {
                    targets: [-1, -2, -4, -5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fa fa-trash fa-1x"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                var stock = data.category.inventoried ? data.stock : 1000000;
                tr.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: stock,
                        verticalbuttons: true
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
                    });

                tr.find('input[name="dscto_unitary"]')
                    .TouchSpin({
                        min: 0.00,
                        max: 100,
                        step: 0.01,
                        decimals: 2,
                        boostat: 5,
                        verticalbuttons: true,
                        maxboostedstep: 10,
                    })
                    .keypress(function (e) {
                        return validate_decimals($(this), e);
                    });
            },
            initComplete: function (settings, json) {

            },
        });
    },
    get_products_ids: function () {
        var ids = [];
        $.each(this.details.products, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
    add_product: function (item) {
        this.details.products.push(item);
        this.list_products();
    },
};

document.addEventListener('DOMContentLoaded', function (e) {
    const frmClient = document.getElementById('frmClient');
    fvClient = FormValidation.formValidation(frmClient, {
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
                first_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        regexp: {
                            regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                            message: 'Debe ingresar sus dos nombres y solo utilizando caracteres alfabéticos'
                        },
                    }
                },
                last_name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        regexp: {
                            regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
                            message: 'Debe ingresar sus dos apellidos y solo utilizando caracteres alfabéticos'
                        },
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        callback: {
                            message: 'Introduce un número de cedula válido',
                            callback: function (input) {
                                return validate_dni_ruc(input.value);
                            }
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmClient.querySelector('[name="dni"]').value,
                                    type: 'dni',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de cedula ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 7
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmClient.querySelector('[name="mobile"]').value,
                                    type: 'mobile',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de teléfono ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El formato email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: frmClient.querySelector('[name="email"]').value,
                                    type: 'email',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST'
                        }
                    }
                },
                address: {
                    validators: {
                        stringLength: {
                            min: 4,
                        }
                    }
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                birthdate: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
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
            const iconPlugin = fvClient.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmClient.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fvClient.form);
            parameters.append('action', 'create_client');
            submit_formdata_with_ajax('Notificación', '¿Estas seguro de realizar la siguiente acción?', pathname,
                parameters,
                function (request) {
                    var newOption = new Option(request.user.full_name, request.id, false, true);
                    select_client.append(newOption).trigger('change');
                    fvSale.revalidateField('client');
                    $('#myModalClient').modal('hide');
                }
            );
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    function validateChange() {
        var cash = parseFloat(input_cash.val());
        var method_payment = select_paymentmethod.val();
        if (method_payment === 'efectivo') {
            return cash >= vents.details.total;
        } else if (method_payment === 'efectivo_tarjeta') {
            var amount_debited = parseFloat(input_amountdebited.val());
            var amount = amount_debited + cash;
            return amount >= vents.details.total;
        }
        return true;
    }

    function validateAmountDebited() {
        var amount_debited = parseFloat(input_amountdebited.val());
        var method_payment = select_paymentmethod.val();
        if (method_payment === 'tarjeta_debito_credito') {
            return amount_debited >= vents.details.total;
        } else if (method_payment === 'efectivo_tarjeta') {
            var cash = parseFloat(input_cash.val());
            var amount = amount_debited + cash;
            return amount >= vents.details.total;
        }
        return true;
    }

    const frmSale = document.getElementById('frmSale');
    fvSale = FormValidation.formValidation(frmSale, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                client: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cliente'
                        },
                    }
                },
                end_credit: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                payment_condition: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una forma de pago'
                        },
                    }
                },
                payment_method: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un método de pago'
                        },
                    }
                },
                type_voucher: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de comprobante'
                        },
                    }
                },
                card_number: {
                    validators: {
                        notEmpty: {},
                        regexp: {
                            regexp: /^\d{4}\s\d{4}\s\d{4}\s\d{4}$/,
                            message: 'Debe ingresar un numéro de tarjeta en el siguiente formato 1234 5678 9103 2247'
                        },
                        stringLength: {
                            min: 2,
                            max: 19,
                        },
                    }
                },
                titular: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 3,
                        },
                    }
                },
                amount_debited: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        },
                        callback: {
                            message: 'El monto a debitar no puede ser menor al total a pagar',
                            callback: function (input) {
                                return validateAmountDebited();
                            }
                        }
                    }
                },
                cash: {
                    validators: {
                        notEmpty: {},
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
                    }
                },
                change: {
                    validators: {
                        notEmpty: {},
                        callback: {
                            message: 'El cambio no puede ser negativo',
                            callback: function (input) {
                                return validateChange();
                            }
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
            const iconPlugin = fvSale.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(frmSale.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            vents.details.client = select_client.val();
            vents.details.end_credit = input_endcredit.val();
            vents.details.payment_condition = select_paymentcondition.val();
            vents.details.payment_method = select_paymentmethod.val();
            vents.details.type_voucher = $('select[name="type_voucher"]').val();
            vents.details.cash = input_cash.val();
            vents.details.change = input_change.val();
            vents.details.card_number = input_cardnumber.val();
            vents.details.titular = input_titular.val();
            vents.details.amount_debited = input_amountdebited.val();

            if (vents.details.products.length === 0) {
                message_error('Debe tener al menos un item en el detalle de la venta');
                return false;
            }

            submit_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'vents': JSON.stringify(vents.details)
                },
                function (request) {
                    dialog_action('Notificación', '¿Desea Imprimir el Comprobante?', function () {
                        window.open('/pos/crm/sale/print/voucher/' + request.id + '/', '_blank');
                        location.href = '/pos/crm/sale/admin/';
                    }, function () {
                        location.href = '/pos/crm/sale/admin/';
                    });

                },
            );

        });
});

function printInvoice(id) {
    var printWindow = window.open("/pos/crm/sale/print/voucher/" + id + "/", 'Print', 'left=200, top=200, width=950, height=500, toolbar=0, resizable=0');
    printWindow.addEventListener('load', function () {
        printWindow.print();
    }, true);
}

function hideRowsVents(values) {
    $.each(values, function (key, value) {
        if (value.enable) {
            $(inputs_vents[value.pos]).show();
        } else {
            $(inputs_vents[value.pos]).hide();
        }
    });
}

$(function () {

    current_date = new moment().format("YYYY-MM-DD");
    input_searchclient = $('input[name="search_client"]');
    input_searchproducts = $('input[name="searchproducts"]');
    select_client = $('select[name="client"]');
    input_birthdate = $('input[name="birthdate"]');
    input_endcredit = $('input[name="end_credit"]');
    select_paymentcondition = $('select[name="payment_condition"]');
    select_paymentmethod = $('select[name="payment_method"]');
    input_cardnumber = $('input[name="card_number"]');
    input_amountdebited = $('input[name="amount_debited"]');
    input_cash = $('input[name="cash"]');
    input_change = $('input[name="change"]');
    input_titular = $('input[name="titular"]');
    modal_sale = $('#myModalSale');
    inputs_vents = $('.modal-sale .row');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    /* Product */

    input_searchproducts.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(vents.get_products_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            if (ui.item.stock === 0 && ui.item.category.inventoried) {
                message_error('El stock de este producto esta en 0');
                return false;
            }
            ui.item.cant = 1;
            vents.add_product(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_searchproducts.val('').focus();
    });

    $('#tblProducts tbody')
        .on('change', 'input[name="cant"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.details.products[tr.row].cant = parseInt($(this).val());
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.details.products[tr.row].subtotal.toFixed(2));
            $('td:eq(8)', tblProducts.row(tr.row).node()).html('$' + vents.details.products[tr.row].total.toFixed(2));
        })
        .on('change', 'input[name="dscto_unitary"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.details.products[tr.row].dscto = parseFloat($(this).val());
            vents.calculate_invoice();
            $('td:eq(7)', tblProducts.row(tr.row).node()).html('$' + vents.details.products[tr.row].total_dscto.toFixed(2));
            $('td:eq(8)', tblProducts.row(tr.row).node()).html('$' + vents.details.products[tr.row].total.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.details.products.splice(tr.row, 1);
            vents.list_products();
        });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': input_searchproducts.val(),
                    'ids': JSON.stringify(vents.get_products_ids()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "name"},
                {data: "category.name"},
                {data: "pvp"},
                {data: "price_promotion"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.category.inventoried) {
                            if (row.stock > 0) {
                                return '<span class="badge badge-success">' + row.stock + '</span>';
                            }
                            return '<span class="badge badge-danger">' + row.stock + '</span>';
                        }
                        return '<span class="badge badge-secondary">Sin stock</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>';
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchProducts.row($(this).parents('tr')).data();
        row.cant = 1;
        vents.add_product(row);
        tblSearchProducts.row($(this).parents('tr')).remove().draw();
    });

    $('.btnRemoveAllProducts').on('click', function () {
        if (vents.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            vents.details.products = [];
            vents.list_products();
        });
    });

    /* Client */

    select_client.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        dropdownParent: modal_sale,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_client'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            fvSale.revalidateField('client');
        })
        .on('select2:clear', function (e) {
            fvSale.revalidateField('client');
        });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function () {
        fvClient.resetForm(true);
    });

    $('input[name="dni"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="mobile"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    input_birthdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    input_birthdate.datetimepicker('date', input_birthdate.val());

    input_birthdate.on('change.datetimepicker', function (e) {
        fvClient.revalidateField('birthdate');
    });

    /* Sale */

    select_paymentcondition
        .on('change', function () {
            var id = $(this).val();
            hideRowsVents([{'pos': 2, 'enable': false}, {'pos': 3, 'enable': false}, {'pos': 4, 'enable': false}]);
            switch (id) {
                case "contado":
                    select_paymentmethod.prop('disabled', false).val('efectivo').trigger('change');
                    break;
                case "credito":
                    hideRowsVents([{'pos': 4, 'enable': true}]);
                    select_paymentmethod.prop('disabled', true);
                    break;
            }
        });

    select_paymentmethod.on('change', function () {
        var id = $(this).val();
        hideRowsVents([{'pos': 2, 'enable': false}, {'pos': 3, 'enable': false}, {'pos': 4, 'enable': false}]);
        input_cash.val('0.00');
        input_amountdebited.val('0.00');
        switch (id) {
            case "efectivo":
                fvSale.enableValidator('change');
                hideRowsVents([{'pos': 2, 'enable': true}]);
                break;
            case "tarjeta_debito_credito":
                hideRowsVents([{'pos': 3, 'enable': true}]);
                break;
            case "efectivo_tarjeta":
                fvSale.disableValidator('change');
                hideRowsVents([{'pos': 2, 'enable': true}, {'pos': 3, 'enable': true}]);
                break;
        }
    });

    input_cash
        .TouchSpin({
            min: 0.00,
            max: 100000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fvSale.revalidateField('cash');
            var cash = parseFloat($(this).val());
            var change = cash - vents.details.total;
            input_change.val(change.toFixed(2));
            fvSale.revalidateField('change');
            if (select_paymentmethod.val() === 'efectivo_tarjeta') {
                fvSale.revalidateField('amount_debited');
                input_change.val('0.00');
            }
        })
        .keypress(function (e) {
            return validate_decimals($(this), e);
        });

    input_amountdebited
        .TouchSpin({
            min: 0.00,
            max: 10000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fvSale.revalidateField('amount_debited');
            if (select_paymentmethod.val() === 'efectivo_tarjeta') {
                fvSale.revalidateField('change');
            }
        })
        .keypress(function (e) {
            return validate_decimals($(this), e);
        });

    input_cardnumber
        .on('keypress', function (e) {
            fvSale.revalidateField('card_number');
            return validate_form_text('numbers_spaceless', e, null);
        })
        .on('keyup', function (e) {
            var number = $(this).val();
            var number_nospaces = number.replace(/ /g, "");
            if (number_nospaces.length % 4 === 0 && number_nospaces.length > 0 && number_nospaces.length < 16) {
                number += ' ';
            }
            $(this).val(number);
        });

    input_titular.on('keypress', function (e) {
        return validate_form_text('letters', e, null);
    });

    input_endcredit.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: current_date
    });

    input_endcredit.datetimepicker('date', input_endcredit.val());

    input_endcredit.on('change.datetimepicker', function (e) {
        fvSale.revalidateField('end_credit');
    });

    $('input[name="dscto"]')
        .TouchSpin({
            min: 0.00,
            max: 100,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            var dscto = $(this).val();
            if (dscto === '') {
                $(this).val('0.00');
            }
            vents.calculate_invoice();
        })
        .keypress(function (e) {
            return validate_decimals($(this), e);
        });

    $('.btnCollect').on('click', function () {
        select_client.val('').trigger('change');
        fvSale.resetForm(true);
        input_endcredit.datetimepicker('date', current_date);
        hideRowsVents([{'pos': 2, 'enable': true}, {'pos': 3, 'enable': false}, {'pos': 4, 'enable': false}]);
        if (vents.details.products.length === 0) {
            message_error('Debe tener al menos un item en el detalle de la venta');
            return false;
        }
        $('input[name="amount"]').val(vents.details.total.toFixed(2));
        input_cash.val('0.00');
        modal_sale.modal('show');
    });

    $('.btnProforma').on('click', function () {
        if (vents.details.products.length === 0) {
            message_error('Debe tener al menos un item en el detalle para poder crear una proforma');
            return false;
        }

        var parameters = {
            'action': 'create_proforma',
            'vents': JSON.stringify(vents.details)
        };

        $.ajax({
            url: pathname,
            data: parameters,
            method: 'POST',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (request) {
                if (!request.hasOwnProperty('error')) {
                    var d = new Date();
                    var date_now = d.getFullYear() + "_" + d.getMonth() + "_" + d.getDay();
                    var a = document.createElement("a");
                    document.body.appendChild(a);
                    a.style = "display: none";
                    const blob = new Blob([request], {type: 'application/pdf'});
                    const url = URL.createObjectURL(blob);
                    a.href = url;
                    a.download = "download_pdf_" + date_now + ".pdf";
                    a.click();
                    window.URL.revokeObjectURL(url);
                    return false;
                }
                message_error(request.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
    });
});