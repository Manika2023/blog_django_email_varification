from django.urls import path,include
from . import views
urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout_View,name="logout_view"),
    path('token/',views.token_send,name="token_send"),
    path('success/',views.success,name="success"),
    path('verify/<auth_token>',views.verify,name="verify"),
    path('error/',views.error_page,name="error"),  
]