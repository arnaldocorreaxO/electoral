var input_searchproducts;
var tblProducts;
var tblSearchProducts;

var inventory = {
    details: {
        products: []
    },
    add_product: function (item) {
        this.details.products.push(item);
        this.list_products();
    },
    list_products: function () {
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
                {data: "stock"},
                {data: "newstock"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" style="width: 100px;" autocomplete="off" name="newstock" value="' + row.newstock + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
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
                tr.find('input[name="newstock"]')
                    .TouchSpin({
                        min: 0,
                        max: 10000000,
                        verticalbuttons: true,
                    })
                    .keypress(function (e) {
                        return validate_form_text('numbers', e, null);
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
};

$(function () {

    input_searchproducts = $('input[name="searchproducts"]');

    input_searchproducts.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(inventory.get_products_ids()),
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
            ui.item.newstock = ui.item.stock;
            inventory.add_product(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_searchproducts.val('').focus();
    });

    $('#tblProducts tbody')
        .on('change', 'input[name="newstock"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            inventory.details.products[tr.row].newstock = parseInt($(this).val());
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            inventory.details.products.splice(tr.row, 1);
            inventory.list_products();
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
                    'ids': JSON.stringify(inventory.get_products_ids()),
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
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        return '<span class="badge badge-warning">' + data + '</span>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var row = tblSearchProducts.row(tr.row).data();
            row.newstock = row.stock;
            inventory.add_product(row);
            tblSearchProducts.row(tblSearchProducts.row(tr.row).node()).remove().draw();
        });

    $('.btnRemoveAllProducts').on('click', function () {
        if (inventory.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            inventory.details.products = [];
            inventory.list_products();
        }, function () {

        });
    });

    inventory.list_products();

    $('.btnCreate').on('click', function () {
        if (inventory.details.products.length === 0) {
            message_error('Debe tener al menos un producto en su detalle');
            return false;
        }
        submit_with_ajax('Notificación', '¿Estas seguro de realizar la siguiente acción?', pathname,
            {
                'action': 'create',
                'products': JSON.stringify(inventory.details.products)
            },
            function (request) {
                location.href = '/dashboard/';
            }
        );
    });
})