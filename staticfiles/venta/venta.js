var tblProductos;

var vents = {
    items: {
        id_cliente: '',
        fecha_emision: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        productos: []
    },

    //Calcular Factura
     calcular_factura: function () {
        var subTotal = 0.00;
        var iva = $('input[name = "iva"]').val();
        $.each(this.items.productos, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            subTotal += dict.subtotal;
        });
        this.items.subtotal = subTotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalculado"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
        
        
    }, 

    add: function (item) {
        this.items.productos.push(item);
        //this.dataT.detalle.push(item)
        this.list();
    },

    //Listar detalle 

    list: function () {
        this.calcular_factura();

        tblProductos = $('#listProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
            columns: [
                { "data": "id" },
                { "data": "nombre"},
                { "data": "precio"},
                { "data": "cantidad"},
                { "data": "descuento"},
                { "data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger" style="color:white"><i class="fas fa-trash-alt"></i></a>';
                    }
                },

                {
                    targets: [-4],
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },

                {
                    targets: [-3],
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete=off value=' + row.cantidad + '></input>';
                    }
                },
                {
                    targets: [-2],
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },

                {
                    targets: [-1],
                    class: "text-center",
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                }
                
            ],

            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find("input[name='cant']").TouchSpin({
                    min: 1,
                    max: 10000000,
                    step: 1
                });
            },


            initComplete: function (settings, json) {

            }
        });
    },

};

$(function () {
    $('.select2').select2({
        theme: 'bootstrap4',
        lagunge: 'es'
    });

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calcular_factura();
    }).val(0.12);


    $('input[name="search"]').autocomplete({
        source: function (request, responde) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_productos',
                    'term': request.term
                },
                dataType: 'json'
            }).done(function (data) {
                responde(data)
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
                //select_productos.html(options)
            });
        },
        delay: 200,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
  
            ui.item.cantidad = 1;
            ui.item.subtotal = 0.00;


            //Añadir productos
            vents.add(ui.item)

            $(this).val('');
        }
    });



    $('.btnRemoveAll').on('click', function () {

        if (vents.items.productos.length === 0) return false;
        alert_action("Notificacion", "¿ Estas seguro de Eliminar todos los Items de tu detalle?", function () {
            vents.items.productos = [];
            vents.list();
        });


    });

    $('#listProductos tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            vents.items.productos.splice(tr.row, 1);
            vents.list();
        })
    
        .on('change', 'input[name = "cant"]', function () {
            var cant = parseInt($(this).val());
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            vents.items.productos[tr.row].cantidad = cant;
            vents.calcular_factura();
            $('td:eq(5)', tblProductos.row(tr.row).node()).html('$' + vents.items.productos[tr.row].subtotal.toFixed(2));
        });
    
    
    //Btn limpiar
    $('.btnClenar').on('click', function (){
        $('input[name="search"]').val('').focus();
    });



    //event submit
    $('#formAdd').on('submit', function (e) {
        e.preventDefault();

        if(vents.items.productos.length === 0){
            message_error('Debe al menos tener un item en su Detalle de venta');
            return false;
        }
        vents.items.id_cliente = $('select[name="id_cliente"]').val();
        vents.items.fecha_emision = $('input[name="fecha_emision"]').val();
        



        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));


        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/facturacion/list/';
        }); 
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("MMM Do YY"),
    });




    vents.list();
});