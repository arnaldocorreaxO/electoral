var tblData;
var input_term;
var columns = [];

function initTable() {
    
    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
    });

    $.each(tblData.settings()[0].aoColumns, function (key, value) {
        columns.push(value.sWidthOrig);
    });

    $('#data tbody tr').each(function (idx) {
        $(this).children("td:eq(0)").html(idx + 1);
        console.log(idx+1);
    });
}

function getData(all) {
    var parameters = {
        'action': 'search',
        'term' : input_term.val(),
        // 'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        // 'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };
    // alert(input_term.val());
    // // if (all) {
    // //     parameters['start_date'] = '';
    // //     parameters['end_date'] = '';
    // // }

    tblData = $('#data').DataTable({
        
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        // serverSide: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        order: [[0, 'asc']],
        paging: true,
        ordering: true,
        searching: true,
        // dom: 'Bfrtip',
        // buttons: [
        //     {
        //         // extend: 'excelHtml5',
        //         // text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
        //         // titleAttr: 'Excel',
        //         // className: 'btn btn-success btn-flat btn-xs'
        //     },
        //     {
        //         // extend: 'pdfHtml5',
        //         // text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
        //         // titleAttr: 'PDF',
        //         // className: 'btn btn-danger btn-flat btn-xs',
        //         // download: 'open',
        //         // orientation: 'landscape',
        //         // pageSize: 'LEGAL',
        //         // customize: function (doc) {
        //         //     doc.styles = {
        //         //         header: {
        //         //             fontSize: 18,
        //         //             bold: true,
        //         //             alignment: 'center'
        //         //         },
        //         //         subheader: {
        //         //             fontSize: 13,
        //         //             bold: true
        //         //         },
        //         //         quote: {
        //         //             italics: true
        //         //         },
        //         //         small: {
        //         //             fontSize: 8
        //         //         },
        //         //         tableHeader: {
        //         //             bold: true,
        //         //             fontSize: 11,
        //         //             color: 'white',
        //         //             fillColor: '#2d4154',
        //         //             alignment: 'center'
        //         //         }
        //         //     };
        //         //     doc.content[1].table.widths = columns;
        //         //     doc.content[1].margin = [0, 35, 0, 0];
        //         //     doc.content[1].layout = {};
        //         //     doc['footer'] = (function (page, pages) {
        //         //         return {
        //         //             columns: [
        //         //                 {
        //         //                     alignment: 'left',
        //         //                     text: ['Fecha de creación: ', {text: current_date}]
        //         //                 },
        //         //                 {
        //         //                     alignment: 'right',
        //         //                     text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
        //         //                 }
        //         //             ],
        //         //             margin: 20
        //         //         }
        //         //     });

        //         // }
        //     }
        // ],
        columns: [
            // {data: "position"},
            {data: "ci"},
            {data: "apellido" + ', ' +"nombre"},
            // {data: "nombre"},
            // {data: "barrio.denominacion"},
            // {data: "manzana.denominacion"},
            // {data: "nro_casa"},
            // {data: "fecha_nacimiento"},
            // // {data: "fecha_afiliacion"},
            // {data: "edad"},
            {data: "id"},
        ],
        columnDefs: [
            {
                // targets: [2],
                // class: 'text-center',
                // render: function (data, type, row) {
                //     // if (row.payment_condition.id === 'credito') {
                //     //     return '<span class="badge badge-warning">' + row.payment_condition.name + '</span>';
                //     // }
                //     // return '<span class="badge badge-success">' + row.payment_condition.name + '</span>';
                //     return data;
                // }
            },
            {
                // targets: [3, 4, 5],
                // class: 'text-center',
                // render: function (data, type, row) {
                //     return data;
                // }
            },
            {
                // targets: [-2],
                // class: 'text-center',
                // render: function (data, type, row) {
                //     // return '$' + parseFloat(data).toFixed(2);
                //     return data;
                // }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    // buttons += '<a class="btn btn-info btn-xs btn-flat" data-toggle="tooltip" title="Detalles" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<a href="/electoral/carga_dia_d/update/' + row.id + '/" data-toggle="tooltip" title="Editar registro" class="btn btn-dark btn-flat"><i class="fas fa-plus"></i></a>';
                    // buttons += '<a href="/electoral/elector/delete/' + row.id + '/" rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
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

    current_date = new moment().format('YYYY-MM-DD');
    input_term = $('input[name="term"]');

    // $('#data tbody')
    //     .on('click', 'a[rel="detail"]', function () {
    //         $('.tooltip').remove();
    //         var tr = tblData.cell($(this).closest('td, li')).index();
    //         var row = tblData.row(tr.row).data();
    //         $('#tblDetails').DataTable({
    //             // responsive: true,
    //             // autoWidth: false,
    //             destroy: true,
    //             ajax: {
    //                 url: pathname,
    //                 type: 'POST',
    //                 data: {
    //                     'action': 'search_detproducts',
    //                     'id': row.id
    //                 },
    //                 dataSrc: ""
    //             },
    //             scrollX: true,
    //             scrollCollapse: true,
    //             columns: [
    //                 {data: "product.name"},
    //                 {data: "product.category.name"},
    //                 {data: "price"},
    //                 {data: "cant"},
    //                 {data: "subtotal"},
    //                 {data: "dscto"},
    //                 {data: "total_dscto"},
    //                 {data: "total"},
    //             ],
    //             columnDefs: [
    //                 {
    //                     targets: [-1, -2, -4, -6],
    //                     class: 'text-center',
    //                     render: function (data, type, row) {
    //                         return '$' + parseFloat(data).toFixed(2);
    //                     }
    //                 },
    //                 {
    //                     targets: [-3],
    //                     class: 'text-center',
    //                     render: function (data, type, row) {
    //                         return parseFloat(data).toFixed(2) + '%';
    //                     }
    //                 },
    //                 {
    //                     targets: [-5],
    //                     class: 'text-center',
    //                     render: function (data, type, row) {
    //                         return data;
    //                     }
    //                 }
    //             ]
    //         });

    //         var invoice = [];
    //         invoice.push({'id': 'Cliente', 'name': row.client.user.full_name});
    //         invoice.push({'id': 'Forma de Pago', 'name': row.payment_condition.name});
    //         invoice.push({'id': 'Método de Pago', 'name': row.payment_method.name});
    //         invoice.push({'id': 'Subtotal', 'name': '$' + row.subtotal});
    //         invoice.push({'id': 'Iva', 'name': row.iva + ' %'});
    //         invoice.push({'id': 'Total Iva', 'name': '$' + row.total_iva});
    //         invoice.push({'id': 'Descuento', 'name': row.dscto + ' %'});
    //         invoice.push({'id': 'Total Descuento', 'name': '$' + row.total_dscto});
    //         invoice.push({'id': 'Total a pagar', 'name': '$' + row.total});
    //         if (row.payment_method.id === 'efectivo') {
    //             invoice.push({'id': 'Efectivo', 'name': '$' + row.cash});
    //             invoice.push({'id': 'Vuelto', 'name': '$' + row.change});
    //         } else if (row.payment_method.id === 'tarjeta_debito_credito') {
    //             invoice.push({'id': 'Número de tarjeta', 'name': row.card_number});
    //             invoice.push({'id': 'Titular de tarjeta', 'name': row.titular});
    //             invoice.push({'id': 'Monto a debitar', 'name': '$' + row.amount_debited});
    //         } else if (row.payment_method.id === 'efectivo_tarjeta') {
    //             invoice.push({'id': 'Efectivo', 'name': '$' + row.cash});
    //             invoice.push({'id': 'Número de tarjeta', 'name': row.card_number});
    //             invoice.push({'id': 'Titular de tarjeta', 'name': row.titular});
    //             invoice.push({'id': 'Monto a debitar', 'name': '$' + row.amount_debited});
    //         }

    //         $('#tblInvoice').DataTable({
    //             responsive: true,
    //             autoWidth: false,
    //             destroy: true,
    //             data: invoice,
    //             paging: false,
    //             ordering: false,
    //             info: false,
    //             columns: [
    //                 {data: "id"},
    //                 {data: "name"},
    //             ],
    //             columnDefs: [
    //                 {
    //                     targets: [0, 1],
    //                     class: 'text-left',
    //                     render: function (data, type, row) {
    //                         return data;
    //                     }
    //                 },
    //             ]
    //         });

    //         $('.nav-tabs a[href="#home"]').tab('show');

    //         $('#myModalDetails').modal('show');
    //     })

    // input_daterange
    //     .daterangepicker({
    //         language: 'auto',
    //         startDate: new Date(),
    //         locale: {
    //             format: 'YYYY-MM-DD',
    //         }
    //     })
    //     .on('apply.daterangepicker', function (ev, picker) {
    //         getData(false);
    //     });

    $('.drp-buttons').hide();

    initTable();
    getData(false);

    $('.btnSearch').on('click', function () {
        getData(false);
    });

    $('.btnSearchAll').on('click', function () {
        getData(true);
    });
});
