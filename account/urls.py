from django.urls import path

from account import views

urlpatterns = [
    path('kayit-ol/', views.register_account, name="register_account"),
    path('giris/', views.login_account, name="login_account"),
    path('cikis/', views.logout_account, name="logout_account"),
]