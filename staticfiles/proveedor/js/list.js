$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                "action":"searchdata"
            },
            dataSrc:""
        },
        columns:[
            {"data":"identificacion"},
            {"data":"nombre"},
            {"data":"telefono"},
            {"data":"direccion"},
            {"data":"butons"},
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="/cliente/editar_proveedor/'+row.id+'/" class="btn btn-warning"><i class="fas fa-edit"></i></a>'+
                    '<a href="/cliente/eliminar_proveedor/'+row.id+'/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });
});