var tblData;
var input_daterange;
var columns = [];

// function initTable() {
    
//     tblData = $('#data').DataTable({
//         responsive: true,
//         autoWidth: false,
//         destroy: true,
//         // deferRender: true,
//         // processing: true,
//         // serverSide: true,
//     });

//     $.each(tblData.settings()[0].aoColumns, function (key, value) {
//         columns.push(value.sWidthOrig);
//     });

//     $('#data tbody tr').each(function (idx) {
//         $(this).children("td:eq(0)").html(idx + 1);
//         console.log(idx+1);
//     });
// }

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

    tblData = $('#data').DataTable({
        
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        processing: true,
        serverSide: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            // dataSrc: ""
        },
        order: [[0, 'asc']],
        paging: true,
        ordering: true,
        searching: true,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = columns;
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: current_date}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        columns: [
            {data: "position"},
            {data: "ci"},
            {data: "apellido"},
            {data: "nombre"},
            {data: "barrio.denominacion"},
            {data: "manzana.denominacion"},
            {data: "nro_casa"},
            {data: "fecha_nacimiento"},
            // {data: "fecha_afiliacion"},
            {data: "edad"},
            {data: "id"},
        ],
        columnDefs: [
          
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    // buttons += '<a class="btn btn-info btn-xs btn-flat" data-toggle="tooltip" title="Detalles" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<a href="/electoral/elector/update/' + row.id + '/" data-toggle="tooltip" title="Editar registro" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a>';
                    buttons += '<a href="/electoral/elector/delete/' + row.id + '/" rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
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

    var link_add = document.querySelector('a[href="/electoral/elector/add/"]');
    var link_upd = document.querySelector('a[href=""]');
    link_add.style.display = 'none';
    link_upd.style.display = 'none';

    current_date = new moment().format('YYYY-MM-DD');
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
            getData(true);
        });

    $('.drp-buttons').hide();

    // initTable();
    getData(false);

    $('.btnSearch').on('click', function () {
        getData(false);
    });

    $('.btnSearchAll').on('click', function () {
        getData(true);
    });
});
