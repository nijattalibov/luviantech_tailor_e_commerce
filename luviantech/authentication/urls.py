from django.urls import path,re_path

from authentication.views import Registration, LoginOtp, Login, Logout, CheckRefreshToken, CheckAccessToken


app_name = 'authentication'

urlpatterns = [
    path('register', Registration.as_view(), name='register'),
    path('login_otp', LoginOtp.as_view(), name='login_otp'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('check_refresh_token', CheckRefreshToken.as_view(), name='check_refresh_token'),
    path('check_access_token', CheckAccessToken.as_view(), name='check_access_token'),
]
