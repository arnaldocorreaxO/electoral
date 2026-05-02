var current_date;
var fv;
var input_enddate;
var input_startdate;
var input_searchproducts;
var tblProducts;
var tblSearchProducts;
var input_dsctomassive;

var promotions = {
    details: {
        start_date: '',
        end_date: '',
        products: [],
    },
    calculate_dscto: function () {
        $.each(this.details.products, function (i, item) {
            item.pos = i;
            item.total_dscto = parseFloat(item.pvp) * (parseFloat(item.dscto) / 100);
            var multiplier = 100;
            item.total_dscto = Math.floor(item.total_dscto * multiplier) / multiplier;
            item.price_final = item.pvp - item.total_dscto;
        });
    },
    list_products: function () {
        this.calculate_dscto();
        tblProducts = $('#tblProducts').DataTable({
            // responsive: true,
            // autoWidth: false,
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
                {data: "category.name"},
                {data: "pvp"},
                {data: "dscto"},
                {data: "total_dscto"},
                {data: "price_final"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" style="width: 100px;" name="dscto" value="' + row.dscto + '">';
                    }
                },
                {
                    targets: [-1, -2, -4],
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
                var frm = $(row).closest('tr');

                frm.find('input[name="dscto"]')
                    .TouchSpin({
                        min: 0.01,
                        max: 100,
                        step: 0.01,
                        decimals: 2,
                        boostat: 5,
                        prefix: '%',
                        maxboostedstep: 10,
                        verticalbuttons: true,
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
    const form = document.getElementById('frmForm');
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
            },
            startEndDate: new FormValidation.plugins.StartEndDate({
                format: 'YYYY-MM-DD',
                startDate: {
                    field: 'start_date',
                    message: 'La fecha de inicio debe ser una fecha válida y anterior a la fecha de finalización'
                },
                endDate: {
                    field: 'end_date',
                    message: 'La fecha de finalización debe ser una fecha válida y posterior a la fecha de inicio'
                },
            }),
            fields: {
                start_date: {
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
                end_date: {
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

            promotions.details.start_date = input_startdate.val();
            promotions.details.end_date = input_enddate.val();

            if (promotions.details.products.length === 0) {
                message_error('Debe tener al menos un item en el detalle');
                return false;
            }

            submit_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                {
                    'action': $('input[name="action"]').val(),
                    'promotions': JSON.stringify(promotions.details)
                },
                function () {
                    location.href = form.getAttribute('data-url');
                },
            );
        });
});

$(function () {

    current_date = new moment().format("YYYY-MM-DD");
    input_enddate = $('input[name="end_date"]');
    input_startdate = $('input[name="start_date"]');
    input_searchproducts = $('input[name="searchproducts"]');
    input_dsctomassive = $('input[name="dsctomassive"]');

    input_enddate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: current_date
    });

    input_enddate.datetimepicker('date', input_enddate.val());

    input_startdate.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        minDate: current_date
    });

    input_startdate.datetimepicker('date', input_startdate.val());

    input_startdate.on('change.datetimepicker', function (e) {
        fv.revalidateField('start_date');
        input_endate.datetimepicker('minDate', e.date);
        input_endate.datetimepicker('date', e.date);
    });

    input_enddate.on('change.datetimepicker', function (e) {
        fv.revalidateField('end_date');
    });

    /* Products */

    input_searchproducts.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(promotions.get_products_ids()),
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
            ui.item.dscto = 0.00;
            promotions.add_product(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_searchproducts.val('').focus();
    });

    $('#tblProducts tbody')
        .on('change', 'input[name="dscto"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            promotions.details.products[tr.row].dscto = parseFloat($(this).val());
            promotions.calculate_dscto();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + promotions.details.products[tr.row].total_dscto.toFixed(2));
            $('td:eq(6)', tblProducts.row(tr.row).node()).html('$' + promotions.details.products[tr.row].price_final.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            promotions.details.products.splice(tr.row, 1);
            promotions.list_products();
        });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': input_searchproducts.val(),
                    'ids': JSON.stringify(promotions.get_products_ids()),
                },
                dataSrc: ""
            },
            //paging: false,
            //ordering: false,
            //info: false,
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {data: "name"},
                {data: "category.name"},
                {data: "pvp"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var html = '<div class="checkbox">';
                        html += '<label><input type="checkbox" name="choose" value=""></label>';
                        html += '</div>';
                        return html;
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
        });
        $('input[name="chooseallproducts"]').prop('checked', false);
        $('#myModalSearchProducts').modal('show');
    });

    $('#myModalSearchProducts').on('hide.bs.modal', function () {
        var products = tblSearchProducts.rows().data().toArray().filter(function (item, key) {
            return item.choose;
        });
        var dsctomassive = parseFloat(input_dsctomassive.val());
        $.each(products, function (key, value) {
            value.dscto = dsctomassive;
            promotions.details.products.push(value);
        });
        promotions.list_products();
    })

    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchProducts.row($(this).parents('tr')).data();
            row.dscto = 0.01;
            promotions.add_product(row);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        })
        .on('change', 'input[name="choose"]', function () {
            var row = tblSearchProducts.row($(this).parents('tr')).data();
            row.choose = this.checked;
        });

    $('.btnRemoveAllProducts').on('click', function () {
        if (promotions.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            promotions.details.products = [];
            promotions.list_products();
        }, function () {

        });
    });

    input_dsctomassive
        .TouchSpin({
            min: 0.01,
            max: 1000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
            prefix: '%'
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            var dsctomassive = parseFloat($(this).val());
            promotions.details.products = [];
            $.each(tblProducts.rows().data(), function (key, item) {
                item.dscto = dsctomassive;
                promotions.details.products.push(item);
            });
            promotions.list_products();
        })
        .keypress(function (e) {
            return validate_decimals($(this), e);
        });

    $('input[name="chooseallproducts"]')
        .on('change', function () {
            var state = this.checked;
            var cells = tblSearchProducts.cells().nodes();
            $(cells).find('input[name="choose"]').prop('checked', state).change();
            $.each(tblSearchProducts.rows().data(), function (key, item) {
                item.choose = state;
            });
        });
});
