$(document).ready(function(){
    // Add product to cart, increase cart total count and disable button
    $(".add-product-to-cart").click(function(e){
        quantity = 1
        let clicked_button = $(this);
        let data={
            "id":clicked_button.attr("data-product"),
            "quantity":quantity
        }

        // Add product to cart
        let request = apiAddProduct(data);
        request.done(function (data) {
            if (data["success"] == true) {
                // Increase cart total count
                let count = parseInt($("#cart-total").text());
                $("#cart-total").text(count+quantity);
                
                // Disable button
                clicked_button.prop("disabled", true);
                clicked_button.addClass("makedisable");

                Swal.fire(data["message"])
            } else {
                Swal.fire(data["error"])
            }
        }).fail(function (data) {
            Swal.fire(data["responseText"])
        })
    });


    // Add PLUS-MINUS product to cart
    $(".chg-quantity").click(function(e){
        let clicked_button = $(this);
        let action = clicked_button.attr("data-action");
        let product_price = clicked_button.closest('.cart-row').find('.product-price');
        let product_total_price = clicked_button.closest('.cart-row').find('.product-total-price');
        let quantity_element = clicked_button.closest('.cart-row').find('.cart_quantity');
        let cart_total_element = $("#cart-total");
        let cart_items_count_element = $(".cart_items_count");
        let cart_items_total_price_element = $(".cart_items_total_price");
        
        let quantity = parseInt(quantity_element.text());
        let cart_items_count = parseInt(cart_items_count_element.text());
        let cart_items_total_price = parseFloat(cart_items_total_price_element.text())
        if (action === "add_plus"){
            quantity = quantity + 1 
            cart_items_count = cart_items_count + 1
            cart_items_total_price = cart_items_total_price + parseFloat(product_price.text());
        }else if(action === "add_minus"){
            quantity = quantity - 1
            cart_items_count = cart_items_count - 1
            cart_items_total_price = cart_items_total_price - parseFloat(product_price.text());
        }

        if(quantity === 0){
            Swal.fire("Minimum quantity is 1")
            return
        }
        
        let data={
            "id":clicked_button.attr("data-product"),
            "quantity":quantity
        }

        // Add product to cart
        let request = apiAddProduct(data);
        request.done(function (data) {
            if (data["success"] == true) {
                cart_total_element.text(cart_items_count);
                cart_items_count_element.text(cart_items_count);
                cart_items_total_price_element.text(cart_items_total_price);
                quantity_element.text(quantity);
                product_total_price.text(parseFloat(product_price.text())*quantity);
                Swal.fire(data["message"])
            } else {
                Swal.fire(data["error"])
            }
        }).fail(function (data) {
            Swal.fire(data["responseText"])
        })
    });

    // Remove order item
    $(".remove_order_item").click(function(e){
        let clicked_button = $(this);
        let checkout = $(".checkout")
        let product_price = clicked_button.closest('.cart-row').find('.product-price');
        let product_total_price = clicked_button.closest('.cart-row').find('.product-total-price');
        let quantity_element = clicked_button.closest('.cart-row').find('.cart_quantity');
        let cart_total_element = $("#cart-total");
        let cart_items_count_element = $(".cart_items_count");
        let cart_items_total_price_element = $(".cart_items_total_price");
        let quantity = parseInt(quantity_element.text());
        let cart_items_count = parseInt(cart_items_count_element.text()) - quantity;
        let cart_items_total_price = parseFloat(cart_items_total_price_element.text()) - parseFloat(product_total_price.text());
        

        let id = clicked_button.attr("data-orderitem");
        let request = apiRemoveOrderItem(id);
        request.done(function (data) {
            if (data["success"] == true) {
                cart_total_element.text(cart_items_count);
                cart_items_count_element.text(cart_items_count);
                cart_items_total_price_element.text(cart_items_total_price);
                clicked_button.closest('.cart-row').remove();
                if(cart_items_count === 0){
                    checkout.remove();
                }
                Swal.fire(data["message"])
            } else {
                Swal.fire(data["error"])
            }
        }).fail(function (data) {
            Swal.fire(data["responseText"])
        })
    });

    // Checkout order
    $(".checkout").click(function(e){
        let clicked_button = $(this);
        let id = clicked_button.attr("data-order");
        let request = apiCompleteOrder(id);
        request.done(function (data) {
            if (data["success"] == true) {
                Swal.fire(data["message"])
                setTimeout(function() {
                    window.location.href = "/e_commerce/";
                  }, 1500);
            }else{
                Swal.fire(data["error"])
            }
        }).fail(function (data) {
            Swal.fire(data["responseText"])
        })
    })

    let request = apiCheckAccessToken();
    request.done(function (data) {
        console.log(data);
        if (data["success"] == false) {
            $.cookie("access_token", null);
            $.cookie("refresh_token", null);
            $.cookie("username", null);
            $(location).attr('href', '/e_commerce/login');
        }
    }).fail(function (data) {
        $.cookie("access_token", null);
        $.cookie("refresh_token", null);
        $.cookie("username", null);
        $(location).attr('href', '/e_commerce/login');
    })
})

