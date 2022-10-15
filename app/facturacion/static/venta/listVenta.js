var tblSale;

$(function () {
    tblSale = $('#data').DataTable({
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
            {"data":"id_cliente"},
            {"data":"fecha_emision"},
            {"data":"subtotal"},
            {"data":"total"},
            {"data":"butons"},
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="/facturacion/delete/'+row.id+'/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>' + 
                    '<a rel="details" class="btn btn-success btn-xs btn-float"><i class="fas fa-search"></i></a>'+
                    '<a href="/facturacion/volante/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-float"><i class="fas fa-file-pdf"></i></a>';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            console.log(data);

            $('#tableDetalle').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        "action":"search_details_prod",
                        'id': data.id
                    },
                    dataSrc:""
                },
                columns:[
                    {"data":"id_producto.nombre"},
                    {"data":"id_producto.id_categoria"},
                    {"data":"cantidad"},
                    {"data":"subtotal"},
                ],
                columnDefs:[
                    {
                        targets : [-1],
                        class : "text-center",
                        render: function (data, type, row){
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets : [-1],
                        class : "text-center",
                        render: function (data, type, row){
                            return data;
                        }
                    },
                ],
                initComplete: function(settings, json){
        
                }
            });

            $('#miModalDetalle').modal('show');
             

    });
});