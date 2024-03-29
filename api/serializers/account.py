from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework_jwt.settings import api_settings

from account.models import Account

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


# Registration
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = Account
        fields = ('username', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = Account.objects.create_user(**validated_data)
        Account.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            data_joined=profile_data['data_joined'],
            is_active=profile_data['is_active'],
        )
        return user


class AccountUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = Account
        fields = ('profile',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        user = Account.objects.update_or_create(**validated_data)
        Account.objects.update(
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        try:
            get_object_or_404(Account, username=username)
        except:
            raise serializers.ValidationError(
                {"data": {
                    "success": "False",
                    "status": status.HTTP_404_NOT_FOUND,
                    "error": "True",
                    "message": "Kullanıcı bulunamadı.",
                }}
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                'Kullanıcı eşleşmedi'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name')
