import requests
from e_commerce.models import Order

def add_variable_to_context(request): 
    cart_items=0
    if(request.user.id):
        order = Order.objects.filter(user= request.user, complete = False).first()
        if order is not None:
            cart_items = order.get_cart_items
    return {
        'cart_items':cart_items,
    }
