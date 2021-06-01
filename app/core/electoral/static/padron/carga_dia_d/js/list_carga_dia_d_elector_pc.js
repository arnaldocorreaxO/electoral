var tblData;
var input_term;
var columns = [];

function initTable() {
    
    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        // serverSide: true,
    });

    // $.each(tblData.settings()[0].aoColumns, function (key, value) {
    //     columns.push(value.sWidthOrig);
    // });

    // $('#data tbody tr').each(function (idx) {
    //     $(this).children("td:eq(0)").html(idx + 1);
    //     console.log(idx+1);
    // });
}



function getData(all) {
    var parameters = {
        'action': 'search_pasoxpc',

    };


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
            // dataSrc: "data"
        },
        order: [[4, 'desc']],
        paging: true,
        ordering: true,
        searching: true,       
        columns: [
            {data: "mesa"},
            {data: "orden"},
            {data: "ci"},
            {data: "fullname"},          
            {data: "fec_modificacion"},          
            {data: "id"},
        ],
        columnDefs: [
       
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    // buttons += '<a class="btn btn-info btn-xs btn-flat" data-toggle="tooltip" title="Detalles" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<a href="/electoral/carga_dia_d/update/' + row.id + '/edit_pc/N/" data-toggle="tooltip" title="Deshacer registro" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
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

function addElector(id) {
    $.ajax({
        url: pathname,
        data: {
            'action': 'edit_pasoxpc',
            'id': id,
            // 'ids': JSON.stringify(electores.get_elector_ids()),
        },
        dataType: "json",
        type: "POST",
        beforeSend: function () {

        },
        success: function (request) {
            // console.log(request);
            getData() ;
            
            if (!request.hasOwnProperty('error')) {
                message_info(request.info);
                return false;
            }
            message_warning(request.error);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown + ' ' + textStatus);
        }
    });
    
}

$(function () {


    input_searchElector = $('input[name="searchElector"]');

    input_searchElector.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_elector',
                    'term': request.term,
                    // 'ids': JSON.stringify(electores.get_elector_ids()),
                },
                dataType: "json",
                type: "POST",
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                    // console.log(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            addElector(ui.item.id)
            // console.log(ui.item);
            $(this).val('').focus();
        }
    });

    current_date = new moment().format('YYYY-MM-DD');
    input_term = $('input[name="term"]');

    
    // BTN DEFAULT 
    input_term.keypress(function(e){
      if(e.keyCode==13)
      $('.btnSearch').click();
    });


    $('.drp-buttons').hide();

    initTable();
    getData(false);


    $('.btnClearElector').on('click', function () {
        input_searchElector.val('').focus();
    });
    $('.btnSearchElector').on('click', function () {
        getData(false);
    });
});
