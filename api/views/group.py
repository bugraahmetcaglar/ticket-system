from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from account.models import Group
from api.serializers.group import GroupSerializer


class GroupListAPI(ListAPIView):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (permissions.IsAdminUser, )


class GroupCreateView(CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(operation_summary="Create a new group")
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