from django.urls import path

from account import views

urlpatterns = [
    path('sign-up/', views.register_account, name="register_account"),
    path('login/', views.login_account, name="login_account"),
    path('logout/', views.logout_account, name="logout_account"),
]