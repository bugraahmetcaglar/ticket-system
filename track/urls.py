from django.urls import path

from track import views

urlpatterns = [
    path('', views.wwttms_index, name="wwttms_index"),
    path('my-tickets/', views.my_tickets, name="my_tickets"),
    path('my-ticket-detail/<int:ticketNumber>/', views.my_tickets_detail, name="my_tickets_detail"),
    path('reply/<int:ticketNumber>/', views.add_reply, name="add_reply"),
    path('my-ticket/delete/<int:ticketNumber>', views.delete_my_ticket, name="delete_my_ticket"),
]