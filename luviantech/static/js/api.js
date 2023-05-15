const baseUrl="http://localhost";
var headers ={'Authorization': 'Bearer ' + $.cookie('access_token')}

// Register
function apiRegister(data){
    let url=`${baseUrl}/authentication/register`;
    return $.ajax( url,{
        type: 'POST',
        data: data,
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Login OTP
function apiLoginOTP(data){
    let url=`${baseUrl}/authentication/login_otp`;
    return $.ajax( url,{
        type: 'POST',
        data: data,
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Login
function apiLogin(data){
    let url=`${baseUrl}/authentication/login`;
    return $.ajax( url,{
        type: 'POST',
        data: data,
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Logout
function apiLogout(){
    data={"refresh" : $.cookie('refresh_token')}
    let url=`${baseUrl}/authentication/logout`;
    return $.ajax( url,{
        type: 'POST',
        data: data,
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Check access token
function apiCheckAccessToken(){
    data={"access" : $.cookie('access_token')}
    let url=`${baseUrl}/authentication/check_access_token`;
    return $.ajax( url,{
        type: 'GET',
        data: data,
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Check refresh token
function apiCheckRefreshToken(){
    data={"refresh" : $.cookie('refresh_token')}
    let url=`${baseUrl}/authentication/check_refresh_token`;
    return $.ajax( url,{
        type: 'POST',
        data: data,
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Add product
function apiAddProduct(data){
    let url=`${baseUrl}/e_commerce/add_product`;
    return $.ajax( url,{
        headers:headers,
        type: 'POST',
        data: data,
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Remove Order Item
function apiRemoveOrderItem(id){
    let url=`${baseUrl}/e_commerce/remove_order_item/${id}`;
    return $.ajax( url,{
        headers:headers,
        type: 'DELETE',
        success: function (data,status,xhr) {   
            return data
        }
    });
}

// Complete Order
function apiCompleteOrder(id){
    let url=`${baseUrl}/e_commerce/complete_order/${id}`;
    return $.ajax( url,{
        headers:headers,
        type: 'PUT',
        success: function (data,status,xhr) {   
            return data
        }
    });
}

