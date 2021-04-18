var tblUsers;
var user;
var fv;

function getData() {
    tblUsers = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'search'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "full_name"},
            {"data": "username"},
            {"data": "is_active"},
            {"data": "image"},
            {"data": "groups"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img class="img-fluid mx-auto d-block" src="' + data + '" width="20px" height="20px">';
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data) {
                        return '<span class="badge badge-success">Activo</span>';
                    }
                    return '<span class="badge badge-danger">Inactivo</span>';
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.groups, function (key, value) {
                        html += '<span class="badge badge-success">' + value.name + '</span> ';
                    });
                    return html;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                data: null,
                render: function (data, type, row) {
                    var html = '<a href="/user/admin/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    html += '<a rel="search_access" class="btn bg-navy btn-xs btn-flat" data-toggle="tooltip" title="Accesos"><i class="fas fa-user-secret"></i></a> ';
                    html += '<a rel="login_with_user" class="btn bg-indigo btn-xs btn-flat" data-toggle="tooltip" title="Loguearse"><i class="fas fa-globe"></i></a> ';
                    html += '<a rel="reset_password" class="btn bg-teal btn-xs btn-flat" data-toggle="tooltip" title="Resetear clave"><i class="fas fa-unlock-alt"></i></a> ';
                    html += '<a rel="change_password" class="btn bg-maroon btn-xs btn-flat" data-toggle="tooltip" title="Cambio de clave"><i class="fas fa-lock"></i></a> ';
                    html += '<a href="/user/admin/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>'
                    return html;
                }
            },
        ]
    });
}

document.addEventListener('DOMContentLoaded', function (e) {
    var form = document.getElementById('frmChangePasswordByUser');
    fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                password: {
                    validators: {
                        notEmpty: {
                            message: 'El password es requerido'
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            submit_with_ajax('Notificación',
                '¿Estas seguro de cambiar la clave?',
                pathname,
                {
                    'id': user.id,
                    'action': 'change_password',
                    'password': $('input[name="password"]').val()
                },
                function () {
                    location.href = pathname;
                });
        });
});

$(function () {

    getData();

    $('#data tbody')
        .on('click', 'a[rel="search_access"]', function () {
            var tr = tblUsers.cell($(this).closest('td, li')).index(),
                row = tblUsers.row(tr.row).data();
            $('#tblAccessUsers').DataTable({
                destroy: true,
                responsive: true,
                autoWidth: false,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_access',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "id"},
                    {"data": "date_joined"},
                    {"data": "hour"},
                    {"data": "localhost"},
                    {"data": "hostname"},
                ],
                columnDefs: [
                    {orderable: false, targets: ['_all']}
                ]
            });
            $('#myModalAccessUsers').modal('show');
        })
        .on('click', 'a[rel="reset_password"]', function () {
            var tr = tblUsers.cell($(this).closest('td, li')).index(),
                row = tblUsers.row(tr.row).data();
            submit_with_ajax('Notificación',
                '¿Estas seguro de resetear la clave?',
                pathname, {
                    'id': row.id,
                    'action': 'reset_password'
                },
                function () {
                    location.reload();
                }
            );
        })
        .on('click', 'a[rel="login_with_user"]', function () {
            var tr = tblUsers.cell($(this).closest('td, li')).index(),
                row = tblUsers.row(tr.row).data();
            submit_with_ajax('Notificación',
                '¿Estas seguro de iniciar sesión con este usuario?',
                pathname, {
                    'id': row.id,
                    'action': 'login_with_user'
                },
                function () {
                    location.href = '/';
                },
            );
        })
        .on('click', 'a[rel="change_password"]', function () {
            var tr = tblUsers.cell($(this).closest('td, li')).index();
            user = tblUsers.row(tr.row).data();
            $('#myModalChangePasswordByUser').modal('show');
        })

    $('#myModalChangePasswordByUser').on('hidden.bs.modal', function () {
        fv.resetForm(true);
    });
});

