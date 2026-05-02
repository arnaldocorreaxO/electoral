var tblGroups;

function getData() {
    var parameters = {
        'action': 'search',
    };

    tblGroups = $('#data').DataTable({
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
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<a rel="search" data-toggle="tooltip" title="Ver permisos" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/security/group/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat" data-toggle="tooltip" title="Editar"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/security/group/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat" data-toggle="tooltip" title="Eliminar"><i class="fas fa-trash"></i></a> ';
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

    $('#data tbody').on('click', 'a[rel="search"]', function () {
        $('.tooltip').remove();
        var tr = tblGroups.cell($(this).closest('td, li')).index(),
            row = tblGroups.row(tr.row).data();
        $('#tblModules').DataTable({
            // responsive: true,
            // autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_modules',
                    'id': row.id,
                },
                dataSrc: ""
            },
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {"data": "name"},
                {"data": "icon"},
                {"data": "image"},
                {"data": "moduletype"},
                {"data": "is_vertical"},
                {"data": "is_visible"},
                {"data": "is_active"},
            ],
            columnDefs: [
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img class="img-fluid mx-auto d-block" src="' + data + '" width="20px" height="20px">';
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!$.isEmptyObject(row.moduletype)) {
                            return row.moduletype.name;
                        }
                        return 'Ninguno';
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<i class="' + data + '" aria-hidden="true"></i>';
                    }
                },
                {
                    targets: [4, 5, 6],
                    class: 'text-center',
                    orderable: false,
                    data: null,
                    render: function (data, type, row) {
                        if (data) {
                            return '<i class="fa fa-check" aria-hidden="true"></i>';
                        }
                        return '<i class="fa fa-times" aria-hidden="true"></i>';
                    }
                },
            ]
        });
        $('#tblPermissions').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_permissions',
                    'id': row.id
                },
                dataSrc: ""
            },
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "codename"},
            ],
        });
        $('.nav-tabs a[href="#home"]').tab('show');
        $('#myModalGroup').modal('show');
    });
});