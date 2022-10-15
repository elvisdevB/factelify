var vents = {
    dataT:{
        id:"comprobante",
        version:"1.0.0",
        infoTributaria:{
            ambiente:"1",
            tipoEmision:"1",
            razonSocial:"",
            nombreComercial:"",
            ruc:"",
            codDoc:"01",
            estab:"001",
            ptoEmi:"0001",
            secuencial:"0000000001",
            dirMatriz:""
        },
        infoFactura: {
            fechaEmision:"",
            dirEstablecimiento:"",
            contribuyenteEspecial:"",
            obligadoContabilidad:"",
            tipoIdentificacionComprador:"",
            guiaRemision:"",
            razonSocialComprador:"",
            identificacionComprador:"",
            direccionComprador:"",
            totalSinImpuestos:0.00,
            totalDescuento:0.00,
            totalImpuesto:[],
            propina:0.0,
            importeTotal:0.00,
            moneda:"",
            pagos:[],
            valorRetIva:0.00,
            valorRetRenta:0.00
        },
        detalle:[],
        campoAdicional:[]
    },

    calcular_factura:function(){

        var subtotal = 0.00;
        var totalDescuento = 0.00
        var iva = $('input[name = "iva"]').val();
        var descuento = $('input[name="descuento"').val();
        var propina = $('input[name="propina"]').val();

        //Calculo de TotalSinImpuestos del cada Producto
        $.each(this.dataT.detalle, function (pos, dict) {
            dict.precioTotalSinImpuestos = dict.cantidad * parseFloat(dict.precio)
            dict.precioTotalSinImpuestos = dict.precioTotalSinImpuestos - (parseFloat(dict.descuento) * parseFloat(dict.cantidad))
            subtotal += dict.precioTotalSinImpuestos;
            totalDescuento = (parseFloat(dict.descuento) * parseFloat(dict.cantidad));
        });

        this.dataT.infoFactura.totalSinImpuestos = subtotal;
        this.dataT.infoFactura.totalDescuento = totalDescuento + parseFloat($('input[name="descuento"]').val());
        this.dataT.infoFactura.importeTotal = subtotal + parseFloat($('input[name="propina"]').val())

        $('input[name="totalSinImpuestos"]').val(this.dataT.infoFactura.totalSinImpuestos.toFixed(2));
        $('input[name="totalDescuento"]').val(this.dataT.infoFactura.totalDescuento.toFixed(2));
        $('input[name="total"]').val(this.dataT.infoFactura.importeTotal.toFixed(2));
    
    },
    add: function(item){
        this.dataT.detalle.push(item);
        this.list();

    },
    list: function () {
        this.calcular_factura();

        tblProductos = $('#listProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.dataT.detalle,
            columns: [
                { "data": "id" },
                { "data": "descripcion" },
                { "data": "precio" },
                { "data": "cantidad" },
                { "data": "descuento" },
                { "data": "precioTotalSinImpuestos" },
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

//Funciones para el calculo de valores de la Factura

$(function (){
    $('.select2').select2({
        theme: 'bootstrap4',
        lagunge: 'es'
    });

    //Boton del Iva
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

    //Boton para la Propina
    $("input[name='propina']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.10,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    }).on('change', function () {
        vents.calcular_factura();
    }).val(0.0);

    //Boton del Descuento
    $("input[name='descuento']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.10,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    }).on('change', function () {
        vents.calcular_factura();
    }).val(0.00);


    //Busqueda de Productos
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
            console.clear()
            ui.item.cantidad = 1;
            ui.item.precioTotalSinImpuestos = 0.00;

            console.log(vents.dataT)

            vents.add(ui.item)

            $(this).val('');
        }
    });

    //Eliminar todos los items del Detalle
    $('.btnRemoveAll').on('click', function () {

        if (vents.dataT.detalle.length === 0) return false;
        alert_action("Notificacion", "¿ Estas seguro de Eliminar todos los Items de tu detalle?", function () {
            vents.dataT.detalle = [];
            vents.list();
        });
    });

    //Detalle de Producto
    $('#listProductos tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            vents.dataT.detalle.splice(tr.row, 1);
            vents.list();
        })
        .on('change', 'input[name = "cant"]', function () {
            var cant = parseInt($(this).val());
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            vents.dataT.detalle[tr.row].cantidad = cant;
            vents.calcular_factura();
            $('td:eq(5)', tblProductos.row(tr.row).node()).html('$' + vents.dataT.detalle[tr.row].precioTotalSinImpuestos.toFixed(2));
        });
    
    //Btn limpiar
    $('.btnClenar').on('click', function (){
        $('input[name="search"]').val('').focus();
    });
    

    //Funcion para agregar datos
    //event submit
    $('#formAdd').on('submit', function (e) {
        e.preventDefault();

        if(vents.dataT.detalle.length === 0){
            message_error('Debe al menos tener un item en su Detalle de venta');
            return false;
        }

        vents.dataT.infoTributaria.razonSocial = $('input[name="razonSocial"]').val();
        vents.dataT.infoTributaria.nombreComercial = $('input[name="nombreComercial"]').val();
        vents.dataT.infoTributaria.ruc = $('select[name="ruc"]').val();
        vents.dataT.infoTributaria.dirMatriz = $('input[name="dirMatriz"]').val();
        vents.dataT.infoFactura.propina = $('input[name="propina"]').val();

        var fecha = $('input[name="fecha_emision"]').val();
        fecha = fecha.replace(/-/g,"/");
        vents.dataT.infoFactura.fechaEmision = fecha;
        vents.dataT.infoFactura.dirEstablecimiento = $('input[name="direccionComprador"]').val();
        vents.dataT.infoFactura.contribuyenteEspecial = $('input[name="contribuyenteEspecial"]').val();
        vents.dataT.infoFactura.obligadoContabilidad = $('select[name="obligadoContabilidad"]').val();
        vents.dataT.infoFactura.tipoIdentificacionComprador = $('select[name="tipoIdentificacionComprador"]').val();


        
        

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.dataT));


        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/facturacion/add/';
        }); 
    });


    vents.list();
});