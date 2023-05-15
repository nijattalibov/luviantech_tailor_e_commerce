$(document).ready(function(){
    var cookie_expire_time = 30  // in minutes
    // Register
    $("#register").click(function(e){
        e.preventDefault();
        let username = $("#reg_username").val()
        let email = $("#reg_email").val()
        let password = $("#reg_password").val()
        let data = {
            "username" : username,
            "email" : email,
            "password" : password
        }
        let request = apiRegister(data);
        request.done(function (data) {
            if (data["success"] == true) {
                $( ".tab-pane" ).each(function() {
                    $( this ).removeClass( "active" );
                    $( this ).removeClass( "show" );
                });
                $( "#pills-otp" ).addClass( "active" ).addClass( "show" );
            } else {
                Swal.fire(data["error"])
            }
        }).fail(function (data) {
            Swal.fire(data["responseText"])
        })
    });
    
    // Login OTP
    $("#login_otp").click(function(e){
        e.preventDefault();
        let username = $("#reg_username").val()
        let otp_code = $("#otp_code").val()
        let data={
            "username":username,
            "otp_code":otp_code
        }
        let request = apiLoginOTP(data);
        request.done(function (data) {
            if (data["success"] == true) {
                // Burada redirect olacaq esas sehifeye
                let access_token = data["access_token"];
                let refresh_token = data["refresh_token"];
                let username = data["username"];
                $.cookie('access_token', access_token, { expires: cookie_expire_time });
                $.cookie('refresh_token', refresh_token, { expires: cookie_expire_time });
                $.cookie('username', username, { expires: cookie_expire_time });
                $(location).attr('href', '/e_commerce/');
            } else {
                Swal.fire(data["error"])
            }
        }).fail(function (data) {
            Swal.fire(data["responseText"])
        })
    });
  
    // Login
    $("#login").click(function(e){
        e.preventDefault();
        let username = $("#username").val()
        let password = $("#password").val()
        let data={
            "username":username,
            "password":password
        }
        let request = apiLogin(data);
        request.done(function (data) {
            if (data["success"] == true) {
                // Redirect to product page
                let access_token = data["access_token"];
                let refresh_token = data["refresh_token"];
                let username = data["username"];
                $.cookie('access_token', access_token, { expires: cookie_expire_time });
                $.cookie('refresh_token', refresh_token, { expires: cookie_expire_time });
                $.cookie('username', username, { expires: cookie_expire_time });
                $(location).attr('href', '/e_commerce/');
            } else {
                Swal.fire(data["error"])
            }
        }).fail(function (data) {
            Swal.fire(data["responseText"])
        })
    });
    
    // Check Access token
    let request = apiCheckAccessToken();
    request.done(function (data) {
        if (data["success"] == true) {
            $(location).attr('href', '/e_commerce/');
        }
    })
  });