from rest_framework.serializers import ModelSerializer

from account.models import Group


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('title', 'slug', 'isActive')

    def create(self, validated_data):
        group = Group.objects.update_or_create(**validated_data)
        Group.objects.create(
            title=validated_data['title'],
            slug=validated_data['slug'],
            isActive=validated_data['isActive'],
        )
        return group