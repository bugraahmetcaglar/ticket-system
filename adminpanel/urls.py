from django.urls import path

from adminpanel.views import views, groups, users

urlpatterns = [
    path('giris/', views.login_admin, name="login_admin"),
    path('cikis/', views.logout_admin, name="logout_admin"),

    path('kullanicilar/grup/ekle/', users.admin_add_account_group, name="admin_add_account_group"),
    path('kullanicilar/grup/', users.admin_account_groups, name="admin_account_groups"),
    path('kullanicilar/yeni/', users.admin_add_account, name="admin_add_account"),
    path('kullanicilar/', users.admin_users, name="admin_users"),

    path('', views.admin_index, name="admin_index"),
    path('gruplar', groups.groups_index, name="groups_index"),
    path('grup-ekle', groups.add_group, name="add_group"),
    path('grup-duzenle/<slug:slug>', groups.edit_group, name="edit_group"),
    path('grup-sil/<slug:slug>', groups.delete_group, name="delete_group"),
]