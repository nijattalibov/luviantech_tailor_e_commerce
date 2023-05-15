from django.shortcuts import render
from django.conf import settings
from authentication.tasks import send_email_task
from authentication.utils import generate_otp, send_otp_email
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegisterSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime

# API Views
class Registration(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # set user password and deactivate 
        user.set_password(serializer.data.get('password', None))
        user.is_active = False

        # generate OTP code
        otp_code = generate_otp()

        # save OTP code to user object and deactivate 
        user.otp_code = otp_code
    
        user.save()

        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp_code}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        
        # send OTP code to user's email
        send_email_task.delay(subject, message, from_email, recipient_list)

        return Response({
            'success': True,
            'message': 'Register successful. Please enter OTP code.'
            })

class LoginOtp(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp_code')

        user = CustomUser.objects.filter(username = username).first()
        if user is None:
            return Response({
                'success': False,
                'error': 'Invalid username'
                },status=status.HTTP_401_UNAUTHORIZED)
        
        if user.is_active:
            return Response({
                'success': False,
                'error': 'User already activated'
                },status=status.HTTP_401_UNAUTHORIZED)
        
        if user.otp_code != int(otp_code):
            return Response({
                'success': False,
                'error': 'Invalid OTP code'
                },status=status.HTTP_401_UNAUTHORIZED)
        
        # set user as authenticated and as active
        user.is_active = True
        user.save()

        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))

        login(request, user)

        return Response({
            'success': True,
            'message': 'Login successful',
            'access_token' : access_token,
            'refresh_token' : refresh_token,
            'username': user.username,
            'email': user.email
            },status=status.HTTP_200_OK)
    
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request,username=username, password=password)
        if user is None:
            return Response({
                'success': False,
                'error': 'Invalid username or password'
                },status=status.HTTP_401_UNAUTHORIZED)

        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))

        login(request, user)

        return Response({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'username': user.username,
            'email': user.email
            },status=status.HTTP_200_OK)
    
class Logout(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        # Log the user out of their session
        logout(request)

        # Get the refresh token from the request
        refresh_token = request.data.get('refresh')

        # Invalidate the refresh and access tokens
        try:
            # Blacklist the refresh token
            RefreshToken(refresh_token).blacklist()

            return Response({
                'success': True,
                'message' :'Logout successful'
                },status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            # Handle any errors
            return Response({
                'success': False,
                'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

class CheckAccessToken(APIView):
    def get(self, request):
        access_token = request.GET.get('access')
        if access_token is None:
            access_token = ""
        try:
            token = JWTAuthentication().get_validated_token(access_token)
            # Token is valid
            return Response({
                    'success': True,
                    'message': 'Access token is valid.'
                    }, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            # Token is invalid or expired
            return Response({
                    'success': False,
                    'message': 'Access token has expired.'
                    }, status=status.HTTP_401_UNAUTHORIZED)   

class CheckRefreshToken(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            token = RefreshToken(refresh_token)
            # Decode the token to extract the payload
            token_data = token.payload
            # Extract the expiration timestamp from the payload
            expiration_timestamp = token_data.get('exp')
            
            # Check if the expiration timestamp is in the past
            is_expired = datetime.utcnow() > datetime.fromtimestamp(expiration_timestamp)
            
            if is_expired:
                return Response({
                    'success': False,
                    'message': 'Refresh token has expired.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'success': True,
                    'message': 'Refresh token is valid.'
                    }, status=status.HTTP_200_OK)
        except:
            return Response({
                'success': False,
                'message': 'Invalid refresh token.'
                }, status=status.HTTP_400_BAD_REQUEST)


