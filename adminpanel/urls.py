from django.conf.urls import url
from django.urls import path

from adminpanel.views import views, groups, users

urlpatterns = [
    path('giris/', views.login_admin, name="login_admin"),
    path('cikis/', views.logout_admin, name="logout_admin"),

    path('users/group/add/', users.admin_add_account_group, name="admin_add_account_group"),
    path('users/group/', users.admin_account_groups, name="admin_account_groups"),
    path('users/new/', users.admin_add_account, name="admin_add_account"),
    path('users/add-group-to-user/', users.admin_add_group_to_user, name="admin_add_group_to_user"),
    path('users/', users.admin_users, name="admin_users"),
    path('tickets/', views.all_tickets, name="all_tickets"),
    path('unread-tickets/', views.unread_tickets, name="unread_tickets"),
    path('ticket/detail/<int:ticketNumber>', views.admin_ticket_detail, name="admin_ticket_detail"),
    path('reply/<int:ticketNumber>/', views.admin_add_reply, name="admin_add_reply"),
    path('ticket/delete/<int:ticketNumber>', views.delete_ticket, name="delete_ticket"),

    url(r'^edit-account/(?P<username>[\w-]+)/$', users.admin_edit_account, name="admin_edit_account"),
    url(r'^block-account/(?P<username>[\w-]+)/$', users.block_account, name="block_account"),

    path('', views.admin_index, name="admin_index"),
    path('groups/', groups.groups_index, name="groups_index"),
    path('add-group/', groups.add_group, name="add_group"),
    path('edit-group/<slug:slug>', groups.edit_group, name="edit_group"),
    path('delete-group/<slug:slug>', groups.delete_group, name="delete_group"),
]