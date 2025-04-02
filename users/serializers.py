from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserRegisterSerializer(UserBaseSerializer):
    confirmation_code = serializers.CharField(max_length=6, read_only=True)

    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('User already exists!')
        return username

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data, is_active=False)
        user.generate_confirmation_code()
        return user


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        code = data.get('confirmation_code')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise ValidationError({'username': 'User not found!'})

        if user.confirmation_code != code:
            raise ValidationError({'confirmation_code': 'Invalid confirmation code!'})

        return data
