from rest_framework import permissions
from rest_framework.generics import ListAPIView

from account.models import Group
from api.serializers.group import GroupSerializer


class GroupListAPI(ListAPIView):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (permissions.IsAdminUser, )