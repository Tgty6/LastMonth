from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserRegisterSerializer(UserBaseSerializer):
    
    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('User already exists!')
        return username

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data, is_active=False)
        return user
