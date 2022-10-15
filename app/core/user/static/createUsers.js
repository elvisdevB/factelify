
var datosUsuario = {
    data:{
        first_name : '',
        last_name:'',
        email:'',
        username:'',
        password:'',
        img:''
    }


}

$(function (){
    $('#usuarioFormulario').on('submit', function (e){
        e.preventDefault();
        
        datosUsuario.data.first_name = $('input[name="first_name"]').val();
        datosUsuario.data.last_name = $('input[name="last_name"]').val();
        datosUsuario.data.email = $('input[name="email"]').val();
        datosUsuario.data.username = $('input[name="username"]').val();
        datosUsuario.data.password = $('input[name="password"]').val();        

        var parameters = new FormData(this);
        parameters.append('datosUsuario', JSON.stringify(datosUsuario.data));

        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/user/listar';
        }); 
    });


});