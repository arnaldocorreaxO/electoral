var input_daterange;
var current_date;
var tblReport;
var columns = [];
var select_seccional;
var select_barrio;
var select_manzana;




function initTable() {
    tblReport = $('#tblReport').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        
    });

    $.each(tblReport.settings()[0].aoColumns, function (key, value) {
        columns.push(value.sWidthOrig);
    });
}

function generateReport(all) {
    var parameters = {
        'action': 'search_report',
        'seccional': select_seccional.val(),
        'barrio': select_barrio.val(),
        'manzana': select_manzana.val(),
        // 'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        // 'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (all) {
        // parameters['start_date'] = '';
        // parameters['end_date'] = '';
    }

    tblReport = $('#tblReport').DataTable({        
        destroy: true,
        responsive: true,
        autoWidth: false,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ''
        },
        // order: [[0, 'asc'],[1, 'asc']],
        paging: false,
        ordering: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: "print",
                text: 'Print <i class="fas fa-print"></i>',
                autoPrint: false,
                className: 'btn btn-success btn-flat btn-xs'
            },
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
            {data: "barrio"},
            {data: "manzana"},
            {data: "cant_elector"},
        ],
        columnDefs: [
           {
                targets: [ 0,  ],
                visible: false
            },
            {
                targets: [-2,],
                className: 'text-left',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [-1],
                className: "text-right",
                render: function (data, type, row) {                    
                    return parseInt(data);
                }
            }
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        },

        rowGroup: {
            // startRender: null,
            endRender: function ( rows, group ) {
                var cantElectorxBarrio = rows
                    .data()
                    .pluck('cant_elector')
                    .reduce( function (a, b) {
                        return a + b*1;
                        
                    }, 0);

                return $('<tr/>')
                .append( '<td colspan="1">'+group+'</td>' )
                .append( '<td class="text-right"> Total: '+ cantElectorxBarrio +'</td>' )
            },
             dataSrc: ["barrio",]
        },
        
    });
}


$(function () {

    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');

    select_seccional = $('select[name="seccional"]');
    select_barrio = $('select[name="barrio"]');
    select_manzana = $('select[name="manzana"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            },
        });

    $('.drp-buttons').hide();

    initTable();

    generateReport(false);

    $('.btnSearchReport').on('click', function () {
        generateReport(false);
    });

    $('.btnSearchAll').on('click', function () {
        generateReport(true);
    });
});