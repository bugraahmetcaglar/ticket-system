from django.conf.urls import url
from django.urls import path

from adminpanel.views import views, groups, users

urlpatterns = [
    # Main View
    path('login/', views.login_admin, name="login_admin"),
    path('logout/', views.logout_admin, name="logout_admin"),
    path('unread-tickets/', views.admin_unread_tickets, name="admin_unread_tickets"),
    path('ticket/detail/<int:ticketNumber>', views.admin_ticket_detail, name="admin_ticket_detail"),
    path('reply/<int:ticketNumber>/', views.admin_add_reply, name="admin_add_reply"),
    path('ticket/delete/<int:ticketNumber>', views.admin_delete_ticket, name="admin_delete_ticket"),
    path('', views.admin_all_tickets, name="admin_index"),
    path('all-tickets/', views.admin_all_tickets, name="admin_all_tickets"),
    path('add-ticket-to-group/', views.admin_add_ticket_to_group, name="admin_add_ticket_to_group"),

    # User
    path('users/group/add/', users.admin_add_account_group, name="admin_add_account_group"),
    path('users/group/', users.admin_account_groups, name="admin_account_groups"),
    path('users/new/', users.admin_add_account, name="admin_add_account"),
    path('users/add-group-to-user/', users.admin_add_group_to_user, name="admin_add_group_to_user"),
    path('users/', users.admin_users, name="admin_users"),

    url(r'^edit-account/(?P<username>[\w-]+)/$', users.admin_edit_account, name="admin_edit_account"),
    url(r'^block-account/(?P<username>[\w-]+)/$', users.admin_block_account, name="admin_block_account"),

    # Group
    path('groups/', groups.admin_all_groups, name="admin_all_groups"),
    path('add-group/', groups.admin_add_group, name="admin_add_group"),
    path('edit-group/<slug:slug>', groups.admin_edit_group, name="admin_edit_group"),
    path('delete-group/<slug:slug>', groups.admin_delete_group, name="admin_delete_group"),

]