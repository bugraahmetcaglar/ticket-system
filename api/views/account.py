from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from api.serializers.account import RegisterSerializer, LoginSerializer


class AccountRegistrationView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_summary="Registration a new user")
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': None,
        }

        return Response(response, status=status_code)


class AccountLoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_summary="Login account")
    def post(self, request, username=None, password=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': None,
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class AccountDetailAPI(APIView):
    permission_classes = (permissions.IsAdminUser, )

    @swagger_auto_schema(operation_summary="Get account by given username")
    def get(self, request, username=None, format=None):
        username = self.kwargs.get("username")
        obj = get_object_or_404(Account, username=username)
        response = {
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "email": obj.email,
            "username": obj.username,
            "date_joined": obj.date_joined,
            "last_login": obj.last_login,
            "is_active": obj.is_active,
            "result": {
                "success": "True",
                "status": status.HTTP_200_OK,
                "error": None,
                "message": None,
            }
        }
        return Response(response)