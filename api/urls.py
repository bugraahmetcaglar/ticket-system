from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views.account import AccountLoginAPIView, AccountRegistrationView, AccountDetailAPI, AccountUpdateView
from api.views.group import GroupListAPI
from api.views.ticket import TicketDetailAPI, TicketListAPI, TicketReplyAPI, TicketDeleteAPI

router = routers.SimpleRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Ticket",
      default_version='v1',
      description="Ticket API DOC",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="info@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

app_name = "api"

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='')),
    url(r'^swagger', include(router.urls)),

    # Account
    url(r'^api/v1/Account/Login/$', AccountLoginAPIView.as_view(), name="account-login-api"),
    url(r'^api/v1/Account/Register/$', AccountRegistrationView.as_view(), name="account-register-api"),
    url(r'^api/v1/Account/Update/$', AccountUpdateView.as_view(), name="account-update-api"),

    url(r'^api/v1/Group/List/$', GroupListAPI.as_view(), name="group-list-api"),

    url(r'^api/v1/Ticket/List/$', TicketListAPI.as_view(), name="ticket-list-api"),
    url(r'^api/v1/Ticket/(?P<ticketNumber>[\w-]+)/$', TicketDetailAPI.as_view(), name="ticket-detail-api"),
    url(r'^api/v1/Ticket/Delete/(?P<ticketNumber>[\w-]+)/$', TicketDeleteAPI.as_view(), name="ticket-delete-api"),
    url(r'^api/v1/Ticket/Reply/(?P<ticketNumber>[\w-]+)/$', TicketReplyAPI.as_view(), name="ticket-reply-api"),

]
urlpatterns += router.urls
