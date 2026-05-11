var tblData;
var input_daterange;
var columns = [];

function initTable() {
    
    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
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
        select_local_votacion.val("").change();       
        select_mesa.val("").change();
        select_seccional.val("").change();
        select_operador.val("").change();

        select_ciudad.val("").change();
        select_barrio.val("").change();
        select_manzana.val("").change();
        select_tipo_voto.val("").change();

        select_pasoxpc.val("").change();
        select_pasoxmv.val("").change();
        input_term.val("");
    }

    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),

        'local_votacion': select_local_votacion.val(),
        'mesa': select_mesa.val(),
        'seccional': select_seccional.val(),
        'operador': select_operador.val(),
        
        'ciudad': select_ciudad.val(),        
        'barrio': select_barrio.val(),
        'manzana': select_manzana.val(),       
        'tipo_voto': select_tipo_voto.val(),     
                
        'pasoxpc': select_pasoxpc.val(),
        'pasoxmv': select_pasoxmv.val(),
        'term': input_term.val(),
        
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
        paging: true,
        ordering: true,
        searching: true,
        // stateSave: true,      //Salva la seleccion de longitud de pagina lengthMenu  
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
        pagingType: "full_numbers",
        pageLength: 10,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            // dataSrc: ""
        },
        // order: [[4, 'asc'],[5, 'asc'],[6, 'asc'],[2, 'asc']],
        
        
        dom: 'Blfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                className: 'btn btn-success btn-flat btn-xs',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8],
                    format: {
                        body: function (data, row, column, node) {
                            // 1. Si la celda tiene un INPUT (como Nro Casa), extraemos su valor actual
                            if ($(node).find('input').length > 0) {
                                return $(node).find('input').val();
                            }
                            
                            // 2. Si la celda tiene nuestro sistema de edición (Select2)
                            // Extraemos SOLO el texto del div que se muestra al usuario
                            if ($(node).find('.div-edit-display').length > 0) {
                                return $(node).find('.div-edit-display').text().trim();
                            }

                            // 3. Si la celda tiene Badges (Votó / No Votó)
                            // Extraemos el texto de los badges
                            if ($(node).find('.badge').length > 0) {
                                return $(node).find('.badge').text().trim();
                            }

                            // 4. Para la cédula (Columna 1), quitamos los puntos para que Excel lo trate como número
                            if (column === 1) {
                                return data.replace(/\./g, '');
                            }

                            // Por defecto, limpiar cualquier tag HTML sobrante
                            return typeof data === 'string' ? data.replace(/<[^>]+>/g, '').trim() : data;
                        }
                    }
                }
            },

            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5, 6, 7, 8],
                    format: {
                        body: function (data, row, column, node) {
                            // 1. Si la celda tiene un INPUT (como Nro Casa), extraemos su valor actual
                            if ($(node).find('input').length > 0) {
                                return $(node).find('input').val();
                            }
                            
                            // 2. Si la celda tiene nuestro sistema de edición (Select2)
                            // Extraemos SOLO el texto del div que se muestra al usuario
                            if ($(node).find('.div-edit-display').length > 0) {
                                return $(node).find('.div-edit-display').text().trim();
                            }

                            // 3. Si la celda tiene Badges (Votó / No Votó)
                            // Extraemos el texto de los badges
                            if ($(node).find('.badge').length > 0) {
                                return $(node).find('.badge').text().trim();
                            }

                            // 4. Para la cédula (Columna 1), quitamos los puntos para que Excel lo trate como número
                            if (column === 1) {
                                return data.replace(/\./g, '');
                            }

                            // Por defecto, limpiar cualquier tag HTML sobrante
                            return typeof data === 'string' ? data.replace(/<[^>]+>/g, '').trim() : data;
                        }
                    }
                },
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
            {data: "ciudad"},
            {data: "barrio"},
            {data: "manzana"},
            {data: "nro_casa"},            
            {data: "edad"},
            {data: "id"},
        ],
        columnDefs: [
          
            {
                targets: [0],
                class: 'text-center',
                render: function (data, type, row) {
                    // 1. Asignación de Pesos (Lógica de prioridad)
                    var peso = 0;
                    var texto_excel = "";

                    if (row.tipo_voto && row.tipo_voto.id == 11) {
                        peso = 11;
                        texto_excel = "F";
                    } else {
                        // Determinamos el estado de PC y MV
                        var pc_si = (row.pasoxpc == 'S');
                        var mv_si = (row.pasoxmv == 'S');

                        if (pc_si && mv_si) { peso = 15; texto_excel = "PC SI / MV SI"; }
                        else if (pc_si && !mv_si) { peso = 14; texto_excel = "PC SI / MV NO"; }
                        else if (!pc_si && mv_si) { peso = 13; texto_excel = "PC NO / MV SI"; }
                        else { peso = 12; texto_excel = "PC NO / MV NO"; }
                    }

                    // 2. Retornos para procesos internos
                    if (type === 'sort') return peso; // Ordena por el número que pediste
                    if (type === 'export') return texto_excel; // Texto limpio para Excel

                    // 3. Lógica visual para la pantalla (Badges con <br>)
                    if (peso === 11) {
                        return '<span class="badge badge-secondary" style="width: 60px;">' + row.tipo_voto.cod + '</span>';
                    }

                    var badge_pc = (row.pasoxpc == 'S') 
                        ? '<span class="badge badge-warning" style="width: 60px;">PC SI</span>' 
                        : '<span class="badge badge-danger" style="width: 60px;">PC NO</span>';
                    
                    var badge_mv = (row.pasoxmv == 'S') 
                        ? '<span class="badge badge-success" style="width: 60px;">MV SI</span>' 
                        : '<span class="badge badge-danger" style="width: 60px;">MV NO</span>';

                    return '<div class="text-center">' + badge_pc + '<br>' + badge_mv + '</div>';
                }     
            },
            {
                targets: [1], // Índice del campo Nro de Cédula
                render: function (data, type, row) {
                    if (type === 'display' && data) {
                        // Formatea el número con puntos (ej: 5.962.221)
                        return data.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
                    }
                    return data;
                },
                className: "text-end" // Opcional: alinear a la derecha suele verse mejor para números
            },
           {
                targets: [3], // TIPO VOTO
                class: 'text-center',
                render: function (data, type, row) {
                    // 1. Extraer los datos básicos
                    var id_actual = (row.tipo_voto && row.tipo_voto.id) ? row.tipo_voto.id : '';
                    var texto_actual = data ? data : '---'; 

                    // 2. RETORNO PARA ORDENAR O FILTRAR (Texto plano)
                    // Esto evita el "VOTANTEVOTANTE" en Excel y arregla el orden alfabético
                    if (type === 'sort' || type === 'filter') {
                        return texto_actual;
                    }

                    // 3. Lógica visual para la pantalla (Badges)
                    var badgeClass = 'badge-light'; 
                    if (id_actual) {
                        if (id_actual == 1) badgeClass = 'badge-danger';
                        else if (id_actual == 2) badgeClass = 'badge-info';
                        else if (id_actual == 3) badgeClass = 'badge-dark';
                        else if (id_actual == 4) badgeClass = 'badge-success';
                        else if (id_actual == 13) badgeClass = 'badge-warning';
                        else if (id_actual == 11) badgeClass = 'badge-secondary';
                    }

                    // 4. Retorno del HTML para la tabla
                    return '<div class="div-edit-display" style="cursor:pointer;">' +
                                '<span class="badge ' + badgeClass + '">' + texto_actual + '</span>' +
                        '</div>' +
                        '<div class="div-edit-input" style="display:none;">' +
                                '<select class="form-control select2-inline" data-id="' + row.id + '" data-field="tipo_voto">' +
                                    '<option value="' + id_actual + '" selected>' + texto_actual + '</option>' +
                                '</select>' +
                        '</div>';
                }
            },
                {
                    targets: [4], // CIUDAD
                    class: 'text-center',
                    render: function (data, type, row) {
                        var display = row.ciudad_denominacion ? row.ciudad_denominacion : '---';
                        // SI ES PARA ORDENAR O EXPORTAR, DEVOLVEMOS SOLO TEXTO
                        if (type === 'sort' || type === 'filter') {
                            return display;
                        }
                        return '<div class="div-edit-display" style="cursor:pointer;">' + display + '</div>' +
                            '<div class="div-edit-input" style="display:none;">' +
                            '<select class="form-control select2-inline" data-id="' + row.id + '" data-field="ciudad">' +
                            '<option value="' + (row.ciudad ? row.ciudad.id : '') + '" selected>' + display + '</option></select></div>';
                    }
                },
                {
                    targets: [5], // BARRIO
                    class: 'text-center',
                    render: function (data, type, row) {
                        var display = row.barrio_fullname ? row.barrio_fullname : '---';
                        // SI ES PARA ORDENAR O EXPORTAR, DEVOLVEMOS SOLO TEXTO
                        if (type === 'sort' || type === 'filter') {
                            return display;
                        }
                        return '<div class="div-edit-display" style="cursor:pointer;">' + display + '</div>' +
                            '<div class="div-edit-input" style="display:none;">' +
                            '<select class="form-control select2-inline" data-id="' + row.id + '" data-field="barrio">' +
                            '<option value="' + (row.barrio ? row.barrio.id : '') + '" selected>' + display + '</option></select></div>';
                    }
                },
                {
                    targets: [6], // MANZANA
                    class: 'text-center',
                    render: function (data, type, row) {
                        var display = row.manzana_fullname ? row.manzana_fullname : '---';
                        // SI ES PARA ORDENAR O EXPORTAR, DEVOLVEMOS SOLO TEXTO
                        if (type === 'sort' || type === 'filter') {
                            return display;
                        }
                        return '<div class="div-edit-display" style="cursor:pointer;">' + display + '</div>' +
                            '<div class="div-edit-input" style="display:none;">' +
                            '<select class="form-control select2-inline select2-manzana" data-id="' + row.id + '" data-field="manzana">' +
                            '<option value="' + (row.manzana ? row.manzana.id : '') + '" selected>' + display + '</option></select></div>';
                    }
                },
                {
                    targets: [7], // NRO CASA
                    class: 'text-center',
                    render: function (data, type, row) {
                            var display = row.nro_casa ? row.nro_casa : '---';
                            // SI ES PARA ORDENAR O EXPORTAR, DEVOLVEMOS SOLO TEXTO
                            if (type === 'sort' || type === 'filter') {
                                return display;
                            }
                        return '<input type="text" class="form-control form-control-sm quick-edit-text" ' +
                            'data-id="' + row.id + '" data-field="nro_casa" value="' + (data ? data : '') + '">';
                    }
                },
          {
                targets: [-1], // Columna de Opciones
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<div class="btn-group">';
                    
                    // El botón de Info cambia de color dinámicamente
                    buttons += '<button type="button" class="btn ' + row.btn_class + ' btn-md" ' +
                            'data-toggle="tooltip" data-html="true" data-placement="left" ' +
                            'title="' + row.tooltip_votos + '">' +
                            '<i class="fas fa-info-circle"></i></button>';

                    // Botón Editar (Warning / Amarillo de Bootstrap)
                    buttons += '<button type="button" class="btn btn-warning btn-md js-update" ' +
                            'data-url="/electoral/elector/update/' + row.id + '/"><i class="fas fa-edit"></i></button>';
                    
                    buttons += '</div>';
                    return buttons;
                }
            }
        ],
        drawCallback: function (settings) {
            $('[data-toggle="tooltip"]').tooltip();
        },       
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
    
    select_local_votacion = $('select[name="local_votacion"]');
    select_mesa = $('select[name="mesa"]');   
    select_seccional = $('select[name="seccional"]');
    select_operador = $('select[name="operador"]');

    select_ciudad = $('select[name="ciudad"]');   
    select_barrio = $('select[name="barrio"]');
    select_manzana = $('select[name="manzana"]');
    select_tipo_voto = $('select[name="tipo_voto"]');
     
    select_pasoxpc = $('select[name="pasoxpc"]');
    select_pasoxmv = $('select[name="pasoxmv"]');


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

    select_local_votacion.append($("<option>", {
        value: '',
        text: 'Todos'
      }));

    select_mesa.append($("<option>", {
        value: '',
        text: 'Todas'
      }));

    select_seccional.append($("<option>", {
        value: '',
        text: 'Todas'
      }));
    
    select_operador.append($("<option>", {
    value: '',
    text: 'Todos'
    }));

    select_ciudad.append($("<option>", {
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

    select_tipo_voto.append($("<option>", {
        value: '',
        text: 'Todos'
      }));

     select_local_votacion.val("").change();     
     select_mesa.val("").change();
     select_seccional.val("").change();
     select_operador.val("").change();

     select_ciudad.val("").change();     
     select_barrio.val("").change();
     select_manzana.val("").change();
     select_tipo_voto.val("").change();

     $(function () {
    // --- EVENTOS DE LA TABLA ---

    // 1. Activar edición al hacer clic en el display (Badge/Texto)
    $('#data tbody').on('click', '.div-edit-display', function () {
        var cell = $(this).closest('td');
        var row = $(this).closest('tr');
        
        $(this).hide();
        cell.find('.div-edit-input').show();

        var selectElement = cell.find('select');
        var fieldName = selectElement.data('field');

        // Inicializar Select2
        selectElement.select2({
            theme: 'bootstrap4',
            width: '100%',
            allowClear: true,
            placeholder: '',
            dropdownAutoWidth: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: function (params) {
                    return {
                        'action': 'search_select2',
                        'field': fieldName,
                        'term': params.term,
                        // Si es manzana, enviamos el ID del barrio de la misma fila para filtrar
                        'barrio_id': (fieldName === 'manzana') ? row.find('select[data-field="barrio"]').val() : '',
                        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                    };
                },
                processResults: function (data) {
                    return { results: data };
                }
            }
        }).select2('open');
    });

    // 2. Evento: Selección de una opción
    $('#data tbody').on('select2:select', '.select2-inline', function (e) {
        var id = $(this).data('id');
        var field = $(this).data('field');
        var value = e.params.data.id;
        
        cerrarYGuardar($(this), id, field, value);
    });

    // 3. Evento: Limpiar campo (clic en la "X")
    $('#data tbody').on('select2:clearing', '.select2-inline', function (e) {
        var id = $(this).data('id');
        var field = $(this).data('field');
        
        cerrarYGuardar($(this), id, field, '');
    });

    // 4. Evento: Cierre sin cambios (clic fuera)
    $('#data tbody').on('select2:close', '.select2-inline', function () {
        var cell = $(this).closest('td');
        // Pequeño delay para no interferir con los eventos de click/select
        setTimeout(function() {
            if (cell.find('.div-edit-input').is(':visible')) {
                destruirSelect2(cell);
            }
        }, 150);
    });
});

// --- FUNCIONES DE APOYO ---

function destruirSelect2(cell) {
    var select = cell.find('select');
    if (select.data('select2')) {
        select.select2('destroy');
    }
    cell.find('.div-edit-input').hide();
    cell.find('.div-edit-display').show();
}

function cerrarYGuardar(elemento, id, field, value) {
    var cell = elemento.closest('td');
    
    // 1. Destruir visualmente primero para evitar el lag de la UI
    destruirSelect2(cell);
    
    // 2. Ejecutar Ajax
    saveInlineUpdate(id, field, value);
}


// 3. Guardar cambios en inputs de texto (Nro Casa) al perder el foco o Enter
$('#data tbody').on('change', '.quick-edit-text', function () {
    var id = $(this).data('id');
    var field = $(this).data('field');
    var value = $(this).val();
    saveInlineUpdate(id, field, value);
});

function saveInlineUpdate(id, field, value) {
    // 1. Guardamos la posición actual del scroll del navegador
    var scrollPos = $(window).scrollTop();

    $.ajax({
        url: pathname,
        type: 'POST',
        data: {
            'action': 'quick_update',
            'id': id,
            'field': field,
            'value': value,
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function (response) {
            if (!response.hasOwnProperty('error')) {
                // 2. El segundo parámetro 'false' mantiene la página (ej. pág 10)
                tblData.ajax.reload(function() {
                    // 3. Restauramos la posición del scroll después de que los datos carguen
                    $(window).scrollTop(scrollPos);
                    
                    // Si es barrio, seguimos con el foco automático a manzana
                    if (field === 'barrio' && value !== '') {
                        var currentRow = $('#data').find('select[data-id="' + id + '"]').closest('tr');
                        setTimeout(function() {
                            currentRow.find('td:eq(6) .div-edit-display').click();
                        }, 200);
                    }
                }, false); 
            } else {
                alert(response.error);
            }
        }
    });
};

     

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

  