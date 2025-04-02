from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser
from .serializers import UserRegisterSerializer, UserAuthSerializer, UserConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


class AuthAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Invalid credentials or user not confirmed'})


@api_view(['GET','POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id, 'confirmation_code': user.confirmation_code})

@api_view(['GET'])
def user_detail_api_view(request):
    user = request.user
    return Response({'username': user.username, 'is_active': user.is_active})



@api_view(['POST'])
def confirm_user_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    user = CustomUser.objects.get(username=username)
    user.is_active = True
    user.confirmation_code = None
    user.save()

    return Response({'message': 'User successfully confirmed!'}, status=status.HTTP_200_OK)
