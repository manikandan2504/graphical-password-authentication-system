from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register),

    path('login/', views.login_view),

    path('dashboard/', views.dashboard),

    path('logout/', views.logout_view),

    path('verify-otp/', views.verify_otp),

    path('forgot/', views.forgot_password),
]