from rest_framework.serializers import ModelSerializer

from account.models import Group


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('title', 'slug', 'createdDate', 'updatedDate', 'isActive')

    def create(self, validated_data):
        group = Group.objects.update_or_create(**validated_data)
        Group.objects.create(
            title=validated_data['title'],
            slug=validated_data['slug'],
            createdDate=validated_data['createdDate'],
            updatedDate=validated_data['updatedDate'],
            isActive=validated_data['isActive'],
        )
        return group