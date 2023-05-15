from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import TemplateView, ListView
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Order, OrderItem
from .serializers import AddProductSerializer, OrderItemSerializer, OrderSerializer


# Generic Views
class LoginView(TemplateView):
    template_name = "authentication/login.html"

class ProductView(ListView):
    permission_classes = [IsAuthenticated]
    template_name = "e_commerce/products.html"
    context_object_name = "products"
    queryset = Product.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items = list(OrderItem.objects.filter(order__complete=False,order__user=self.request.user).values_list('product_id',flat=True))
        context['order_items'] = order_items
        return context

class OrderView(ListView):
    permission_classes = [IsAuthenticated]
    template_name = "e_commerce/order.html"
    context_object_name = "order"
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user,complete=False).first()
        return queryset


# API Views
class AddProductAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        serializer = AddProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.create(serializer.validated_data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({
                'success': False,
                'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
    
class RemoveOrderItemAPIView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
                'success': True,
                'message': "Order Item deleted"
                }, status=status.HTTP_200_OK)
    
class CompleteOrderAPIView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
   
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Retrieve the serialized data
        serialized_data = serializer.data

        # Return the serialized data as the API response
        return Response({
                "success" : True,
                "message" : "Checkout. Order completed",
                "order_id" : instance.id
            }, status=status.HTTP_201_CREATED)
    