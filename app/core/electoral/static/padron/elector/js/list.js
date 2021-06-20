var tblData;
var input_daterange;
var columns = [];

function initTable() {
    
    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        // deferRender: true,
        // processing: true,
        // serverSide: true,
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
    if (all=='all'){
        input_term.val("");
        select_ciudad.val("").change();
        select_seccional.val("").change();
        select_barrio.val("").change();
        select_manzana.val("").change();
        select_mesa.val("").change();
    }

    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        'term': input_term.val(),
        'ciudad': select_ciudad.val(),
        'seccional': select_seccional.val(),
        'barrio': select_barrio.val(),
        'manzana': select_manzana.val(),
        'mesa': select_mesa.val(),
        
    };

    if (all!='bday') {
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
        order: [[4, 'asc'],[5, 'asc'],[6, 'asc'],[2, 'asc']],
        
        paging: true,
        pageLength : 10,
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
            // {data: "position"},
            {data: "id"},         
            {data: "ci"},
            {data: "fullname"},
            // {data: "nombre"},
            {data: "tipo_voto.cod"},
            {data: "barrio.denominacion"},
            {data: "manzana.denominacion"},
            {data: "nro_casa"},            
            {data: "edad"},
            {data: "id"},
        ],
        columnDefs: [
          
            {
                targets: [0],
                class: 'text-center',
                render: function (data, type, row) {
                   
                   var badge_pc = '<span class="badge badge-warning">' + ' PC ' + '</span>';
                   var badge_mv = '<span class="badge badge-success">' + ' SI ' + '</span>';
                   var badge_no = '<span class="badge badge-danger"> NO </span>';
                   var badges = badge_no; /*Default*/
                    
                        if (row.pasoxpc =='S') {
                            badges = badge_pc  + badge_no;
                        }
                        if (row.pasoxmv =='S') {
                            badges = badge_mv;
                            if (row.pasoxpc =='S') {
                                badges = badge_pc  + badge_mv;
                            }
                        }     
                        if (row.tipo_voto.id == 11){
                           return '<span class="badge badge-secondary">'+ row.tipo_voto.cod +'</span>';
                        }                  
                     
                     return badges;
                }         
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {                   

                        if (row.tipo_voto.id == 1) {
                            return '<span class="badge badge-danger">' + data + '</span>'
                        }
                        if (row.tipo_voto.id == 2) {
                            return '<span class="badge badge-info">' + data + '</span>'
                        }
                        if (row.tipo_voto.id == 3) {
                            return '<span class="badge badge-dark">' + data + '</span>'
                        }
                        if (row.tipo_voto.id == 4) {
                            return '<span class="badge badge-success">' + data + '</span>'
                        }
                        // Ausentes
                        if (row.tipo_voto.id == 13){
                            return '<span class="badge badge-warning">'+ data +'</span>';
                         }   
                        //  Fallecidos
                         if (row.tipo_voto.id == 11){
                            return '<span class="badge badge-secondary">'+ data +'</span>';
                         }   
                        //Otros
                        return data;
                        
                }         
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';                    
                    buttons += '<button type="button" class="btn btn-warning js-update" data-url="/electoral/elector/update/' + row.id + '/"><i class="fas fa-edit"></i></button>';
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

// INIT LOAD
$(function () {  

    var link_add = document.querySelector('a[href="/electoral/elector/add/"]');
    var link_upd = document.querySelector('a[href=""]');
    link_add.style.display = 'none';
    link_upd.style.display = 'none';

    input_term = $('input[name="term"]');
    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');    
    select_ciudad = $('select[name="ciudad"]');
    select_seccional = $('select[name="seccional"]');
    select_barrio = $('select[name="barrio"]');
    select_manzana = $('select[name="manzana"]');
    select_mesa = $('select[name="mesa"]');


    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            getData('filter');
        });

    $('.drp-buttons').hide();

    initTable();
    getData('filter');

    $('.btnSearch').on('click', function () {
        getData('bday');
    });

    $('.btnFilter').on('click', function () {
        getData('filter');
    });

    $('.btnSearchAll').on('click', function () {
        getData('all');
    });

    // BTN DEFAULT 
    input_term.keypress(function(e){
        if(e.keyCode==13)
        $('.btnFilter').click();
      });


    // Agregamos una linea vacia a los select
    
    select_ciudad.append($("<option>", {
        value: '',
        text: 'Todas'
      }));
    
    select_seccional.append($("<option>", {
        value: '',
        text: 'Todas'
      }));
    
    select_barrio.append($("<option>", {
        value: '',
        text: 'Todos'
      }));
    
    select_manzana.append($("<option>", {
        value: '',
        text: 'Todas'
      }));

    select_mesa.append($("<option>", {
        value: '',
        text: 'Todas'
      }));


     select_ciudad.val("").change();
     select_seccional.val("").change();
     select_barrio.val("").change();
     select_manzana.val("").change();
     select_mesa.val("").change();

});



// VENTANAS MODAL 
$(function () {

    /* Functions */
  
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
       
                $("#modal-elector").modal("show");                                             

        },
        success: function (data) {    
            // console.log('SUCEEEEEEEEEEEEEEEEEEEEEEEEESS')        
            
            if (!data.hasOwnProperty('error')) {   
                $("#modal-elector .modal-content").html(data.html_form);                                           
                return false;
            }
            message_error(data.error);
        }
      });
    };
  
    var saveForm = function () {
        // Habilitamos antes de submit
        var select_seccional = $('#frmForm #id_seccional')
        var select_local_votacion = $('#frmForm #id_local_votacion')
        select_seccional.prop("disabled", false);
        select_local_votacion.prop("disabled", false);


        var form = $(this);
        
            $.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                type: form.attr("method"),
                dataType: 'json',
                success: function (request) {
                    // console.log(request);
                    if (!request.hasOwnProperty('error')) {   
                        tblData.draw('page');
                        $("#modal-elector").modal("hide");
                        select_seccional.prop("disabled", true);
                        select_local_votacion.prop("disabled", true);                                                
                        return false;
                    }
                    message_error(request.error);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    message_error(errorThrown + ' ' + textStatus);
                }
            });
        return false;
    };
  
  
    /* Binding */
  
    // // Create book
    // $(".js-create-elector").click(loadForm);
    // $("#modal-elector").on("submit", ".js-elector-create-form", saveForm);
  
    // Update Elector
    $("#data").on("click", ".js-update", loadForm);
    $("#modal-elector").on("submit", ".js-update-form", saveForm);
  
  });