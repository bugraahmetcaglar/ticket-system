from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, get_object_or_404, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.views import current_user_group
from api.serializers.ticket import TicketSerializer
from track.models import Ticket, TicketReply


class TicketListAPI(ListAPIView):

    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = (permissions.BasePermission, )


class TicketDetailAPI(APIView):
    permission_classes = (permissions.BasePermission, )

    @swagger_auto_schema(operation_summary="Get ticket by given ticketNumber")
    def get(self, request, ticketNumber=None, format=None):
        ticketNumber = self.kwargs.get("ticketNumber")
        obj = get_object_or_404(Ticket, ticketNumber=ticketNumber)
        response = {
            "id": obj.id,
            "creator": {
                "first_name": obj.creator.first_name,
                "last_name": obj.creator.last_name,
                "email": obj.creator.email,
                "username": obj.creator.username,
                "date_joined": obj.creator.date_joined,
                "last_login": obj.creator.last_login,
            },
            "isActive": obj.isActive,
            "createdDate": obj.createdDate,
            "updatedDate": obj.updatedDate,
            "message": obj.message,
            "isRead": obj.isRead,
            "result": {
                "success": "True",
                "status": status.HTTP_200_OK,
                "error": None,
                "message": None,
            }
        }
        return Response(response)


class TicketDeleteAPI(DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(operation_summary="Get ticket by given ticketNumber")
    def delete(self, request, ticketNumber=None, *args, **kwargs):
        ticketNumber = self.kwargs.get("ticketNumber")
        obj = get_object_or_404(Ticket, ticketNumber=ticketNumber)
        obj.isActive = False
        obj.save()
        response = {
            "isActive": obj.isActive,
            "result": {
                "success": "True",
                "status": status.HTTP_200_OK,
                "error": None,
                "message": "Successfully deleted",
            }
        }
        return Response(response)


class TicketReplyAPI(APIView):
    permission_classes = (permissions.BasePermission,)

    @swagger_auto_schema(operation_summary="Get ticket replies by given ticketNumber")
    def get(self, request, ticketNumber=None, format=None):
        ticketNumber = self.kwargs.get("ticketNumber")
        obj = get_object_or_404(Ticket, ticketNumber=ticketNumber)
        # replies = TicketReply.objects.filter(ticketId__ticketNumber=ticketNumber)
        response = {
            "isActive": obj.isActive,
            "result": {
                "success": "True",
                "status": status.HTTP_200_OK,
                "error": None,
                "message": None,
            }
        }
        return Response(response)