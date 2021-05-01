var input_searchElector;
var tblElector;
var tblSearchElector;

var electores = {
    details: {
        elector: []
    },
    add_elector: function (item) {
        this.details.elector.push(item);
        this.list_elector();
    },
    list_elector: function () {
        tblElector = $('#tblElector').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            data: this.details.elector,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {data: "id"},
                {data: "ci"},
                {data: "nombre"},
                {data: "apellido"},
                {data: "id"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
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
                // var tr = $(row).closest('tr');
                // tr.find('input[name="newstock"]')
                //     .TouchSpin({
                //         min: 0,
                //         max: 10000000,
                //         verticalbuttons: true,
                //     })
                //     .keypress(function (e) {
                //         return validate_form_text('numbers', e, null);
                //     });
            },
            initComplete: function (settings, json) {

            },
        });
    },
    get_elector_ids: function () {
        var ids = [];
        $.each(this.details.elector, function (i, item) {
            ids.push(item.id);
        });
        return ids;
    },
};

$(function () {

    input_searchElector = $('input[name="searchElector"]');

    input_searchElector.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_elector',
                    'term': request.term,
                    'ids': JSON.stringify(electores.get_elector_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                    console.log(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.newstock = ui.item.stock;
            electores.add_elector(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearElector').on('click', function () {
        input_searchElector.val('').focus();
    });

    $('#tblElector tbody')
        .on('change', 'input[name="newstock"]', function () {
            var tr = tblElector.cell($(this).closest('td, li')).index();
            electores.details.Elector[tr.row].newstock = parseInt($(this).val());
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblElector.cell($(this).closest('td, li')).index();
            electores.details.Elector.splice(tr.row, 1);
            electores.list_elector();
        });

    $('.btnSearchElector').on('click', function () {
        tblSearchElector = $('#tblSearchElector').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_elector',
                    'term': input_searchElector.val(),
                    'ids': JSON.stringify(electores.get_elector_ids()),
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
        $('#myModalSearchElector').modal('show');
    });

    $('#tblSearchElector tbody')
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchElector.cell($(this).closest('td, li')).index();
            var row = tblSearchElector.row(tr.row).data();
            row.newstock = row.stock;
            electores.add_elector(row);
            tblSearchElector.row(tblSearchElector.row(tr.row).node()).remove().draw();
        });

    $('.btnRemoveAllElector').on('click', function () {
        if (electores.details.Elector.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            electores.details.Elector = [];
            electores.list_elector();
        }, function () {

        });
    });

    electores.list_elector();

    $('.btnCreate').on('click', function () {
        if (electores.details.elector.length === 0) {
            message_error('Debe tener al menos un producto en su detalle');
            return false;
        }
        submit_with_ajax('Notificación', '¿Estas seguro de realizar la siguiente acción?', pathname,
            {
                'action': 'create',
                'electores': JSON.stringify(electores.details.elector)
            },
            function (request) {
                location.href = pathname;
            }
        );
    });
})