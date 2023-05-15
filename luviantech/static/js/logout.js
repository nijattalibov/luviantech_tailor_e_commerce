$(document).ready(function(){
    // Logout
    $("#logout").click(function(e){
        e.preventDefault();
        let request = apiLogout();
        $.cookie("access_token", null);
        $.cookie("refresh_token", null);
        $.cookie("username", null);
        $(location).attr('href', '/e_commerce/login');
    });
});
