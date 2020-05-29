from rest_framework.serializers import ModelSerializer

from account.models import Group


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'