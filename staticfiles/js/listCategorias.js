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
            {"data":"nombre"},
            {"data":"descripcion"},
            {"data":"butons"},
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="/inventario/categoria/editar/'+row.id+'/" class="btn btn-warning"><i class="fas fa-edit"></i></a>'+
                    '<a href="/inventario/categoria/eliminar/'+row.id+'/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });
});