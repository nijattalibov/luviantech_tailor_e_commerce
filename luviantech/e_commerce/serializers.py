from rest_framework.serializers import ValidationError,ModelSerializer
from rest_framework import serializers
from .models import Product, Order, OrderItem
from datetime import datetime

class AddProductSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        quantity = serializers.IntegerField()
        
        def validate(self,attr):
            product = Product.objects.filter(id=attr["id"]).first()
            if product is None:
                raise ValidationError({
                    'success': False,
                    'success': 'Product does not exist'
                })
            
            if attr["quantity"] <= 0 :
                raise ValidationError({
                    'success': False,
                    'success': 'Quantity should be more than 0'
                })
            return attr

        def create(self, validated_data):  
            user = self.context['request'].user
            product = Product.objects.filter(id=validated_data["id"]).first()
            order = Order.objects.filter(user=user).order_by("-id").first()
            found_order = None
            if order is None:
                found_order = Order.objects.create(
                    user = user,
                    date_ordered = datetime.now(),
                    complete = False
                )
            else:
                if order.complete == True:
                    found_order = Order.objects.create(
                        user = user,
                        date_ordered = datetime.now(),
                        complete = False
                    )
                else:
                    found_order = order

            order_item = OrderItem.objects.filter(order=found_order, product=product).first()
            found_order_item = None
            if order_item is None:
                found_order_item = OrderItem()
            else:
                found_order_item = order_item
            found_order_item.product = product
            found_order_item.quantity = validated_data["quantity"]
            found_order_item.date_added = datetime.now()
            found_order_item.order = found_order
            found_order_item.save()

            return {
                "success" : True,
                "message" : "Product added",
                "product_id" : product.id
            } 
       
class OrderItemSerializer(ModelSerializer):
        class Meta:
            model=OrderItem
            fields=['id','order','product','quantity','date_added']

class OrderSerializer(ModelSerializer):
        class Meta:
            model=Order
            fields=['id','user','date_ordered','complete']

        def update(self, instance, validated_data):
            instance.complete = True
            instance.save()
            return {
                "success" : True,
                "message" : "Checkout. Order completed",
                "order_id" : instance.id
            } 
        