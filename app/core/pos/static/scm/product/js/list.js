function getData() {
    var parameters = {
        'action': 'search',
    };

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columns: [
            {data: "id"},
            {data: "name"},
            {data: "category.name"},
            {data: "category.inventoried"},
            {data: "image"},
            {data: "price"},
            {data: "pvp"},
            {data: "price_promotion"},
            {data: "stock"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.category.inventoried) {
                        return 'Si';
                    }
                    return 'No';
                }
            },
            {
                targets: [4],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<img src="' + row.image + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-4, -5, -3],
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
                    var buttons = '';
                    buttons += '<a href="/pos/scm/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" data-toggle="tooltip" title="Editar"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/pos/scm/product/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat" data-toggle="tooltip" title="Eliminar"><i class="fas fa-trash"></i></a> ';
                    return buttons;
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
}

$(function () {
    getData();
})