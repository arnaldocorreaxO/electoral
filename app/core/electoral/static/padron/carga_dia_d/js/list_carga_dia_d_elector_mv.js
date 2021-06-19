var tblData;
var input_term;
var columns = [];

function initTable() {
    
    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        order: [[0, 'asc']],
        paging: false,
        ordering: false,
        searching: false,    
        info:     false   ,
    });
    // Establece width para exportar en PDF pdfmake
    $.each(tblData.settings()[0].aoColumns, function (key, value) {
        columns.push(value.sWidthOrig);
    });

    $('#data tbody tr').each(function (idx) {
        // $(this).children("td:eq(0)").html(idx + 1);
        // console.log(idx+1);
    });
}

function getData(all) {
    var parameters = {
        'action': 'search',
        'term' : input_term.val(),
    };


    tblData = $('#data').DataTable({
        
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
        order: [[0, 'asc']],
        paging: false,
        ordering: false,
        searching: false,    
        info:     false   ,
        columns: [
            // {data: "mesa"},
            // {data: "orden"},
            {data: "ci"},
            {data: "fullname"},          
            {data: "id"},
        ],
        columnDefs: [
       
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    // buttons += '<a class="btn btn-info btn-xs btn-flat" data-toggle="tooltip" title="Detalles" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<b>' + row.mesa +'</b> - ' + '<b>' + row.orden +'</b>';
                    buttons += '<br><a href="/electoral/carga_dia_d/update/' + row.id + '/edit_mv/S/" data-toggle="tooltip" title="Editar registro" class="btn btn-dark btn-lg btn-flat"><i class="fas fa-plus"></i></a>';
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



function getData2(all) {
      
    var local_votacion = localStorage.getItem("local_local_votacion");
    var mesa = localStorage.getItem("local_mesa");

    $('select[name="local_votacion"]').val(local_votacion);
    $('select[name="mesa"]').val(mesa);
    
    var parameters = {
        'action': 'search_pasoxmv',
        'local_votacion': local_votacion,
        'mesa': mesa,

    };

    if (all) {
        parameters['local_votacion'] = '';        
        parameters['mesa'] = '';        
    }


    tblData = $('#data2').DataTable({
        
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
        order: [[0, 'asc'],[1, 'asc']],
        paging: true,
        ordering: true,
        searching: true,       
        columns: [
            {data: "mesa"},
            {data: "orden"},
            {data: "ci"},
            {data: "fullname"},          
            {data: "id"},
        ],
        columnDefs: [
       
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    // buttons += '<a class="btn btn-info btn-xs btn-flat" data-toggle="tooltip" title="Detalles" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<a href="/electoral/carga_dia_d/update/' + row.id + '/edit_mv/N/" data-toggle="tooltip" title="Deshacer registro" class="btn btn-danger btn-flat"><i class="fas fa-trash"></i></a>';
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

    
    // BTN DEFAULT 
    input_term.keypress(function(e){
      if(e.keyCode==13)
      $('.btnSearch').click();
    });


    $('.drp-buttons').hide();

    initTable();
    getData2(false);

    $('.btnSearch').on('click', function () {
        getData(false);
    });

    $('.btnSearchMesa').on('click', function () {
        getData2(false);
    });

    $('.btnSearchAllMesa').on('click', function () {
        getData2(true);
    });

    $('select[name="mesa"]').on('change', function () {  
        localStorage.setItem("local_mesa", $(this).val());;        
        getData2(false);
        
    });
    $('select[name="local_votacion"]').on('change', function () {        
        localStorage.setItem("local_local_votacion", $(this).val());;          
        getData2(false);
        
    });
   
});
