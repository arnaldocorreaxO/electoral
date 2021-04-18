var tblPaymentsCtasCollect, tblCtasCollect, ctascollect;
var date_current;
var input_daterange;

function getData(all) {
    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (all) {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
    }

    tblCtasCollect = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columns: [
            {data: "sale.nro"},
            {data: "sale.client"},
            {data: "date_joined"},
            {data: "end_date"},
            {data: "debt"},
            {data: "saldo"},
            {data: "state"},
            {data: "state"},
        ],
        columnDefs: [
            {
                targets: [-1],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<a rel="payments" data-toggle="tooltip" title="Pagos" class="btn bg-blue btn-xs btn-flat"><i class="fas fa-dollar-sign"></i></a> ';
                    buttons += '<a href="/pos/frm/ctas/collect/delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    if (!$.isEmptyObject(row.sale.client)) {
                        return row.sale.client.user.full_name;
                    }
                    return 'Consumidor final';
                }
            },
            {
                targets: [2, 3],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [4, 5],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + data;
                }
            },
            {
                targets: [-2],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    if (data) {
                        return '<span class="badge badge-danger">Adeuda</span>';
                    }
                    return '<span class="badge badge-success">Pagado</span>';
                }
            }
        ],
        initComplete: function (settings, json) {
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
}

$(function () {

    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            getData(false);
        });

    $('.drp-buttons').hide();

    getData(false);

    $('.btnSearch').on('click', function () {
        getData(false);
    });

    $('.btnSearchAll').on('click', function () {
        getData(true);
    });

    $('#data tbody')
        .on('click', 'a[rel="payments"]', function () {
            $('.tooltip').remove();
            var tr = tblCtasCollect.cell($(this).closest('td, li')).index(),
                row = tblCtasCollect.row(tr.row).data();
            tblPaymentsCtasCollect = $('#tblPayments').DataTable({
                // responsive: true,
                // autoWidth: false,
                destroy: true,
                searching: false,
                scrollX: true,
                scrollCollapse: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: function (d) {
                        d.action = 'search_pays';
                        d.id = row.id;
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "pos"},
                    {data: "date_joined"},
                    {data: "valor"},
                    {data: "desc"},
                    {data: "valor"},
                ],
                columnDefs: [
                    {
                        targets: [2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data;
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash fa-1x"></i></a>';
                        }
                    }
                ],
                rowCallback: function (row, data, index) {

                },
            });
            $('#myModalListPay').modal('show');
        });

    $('#tblPayments tbody')
        .on('click', 'a[rel="delete"]', function () {
            $('.tooltip').remove();
            var tr = tblPaymentsCtasCollect.cell($(this).closest('td, li')).index(),
                row = tblPaymentsCtasCollect.row(tr.row).data();
            submit_with_ajax('Notificación',
                '¿Estas seguro de eliminar el registro?',
                pathname,
                {
                    'id': row.id,
                    'action': 'delete_pay'
                },
                function () {
                    tblCtasCollect = tblCtasCollect.ajax.reload();
                    tblPaymentsCtasCollect.ajax.reload();
                }
            );
        });
});
