from django.contrib.auth import login

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from knox.auth import TokenAuthentication
from knox.models import AuthToken

from ..models import User
from .serializers import (
    SignUpSerializer,
    SignInSerializer,
    UpdateUserSerializer,
    UserChangePasswordSerializer
)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def change_user_password(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if (request.user.pk == user.pk) or (request.user.is_staff):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data.get('password'))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        msg = 'You are not authorized to take that action.'
        return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if (request.user.pk == user.pk) or (request.user.is_staff):
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(user.get_response_data(), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        msg = 'You are not authorized to take that action.'
        return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_users(request):
    users = User.objects.all().order_by('-pk')
    return Response([user.get_response_data() for user in users], status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(user.get_response_data(), status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request=request, user=user)
        instance, token = AuthToken.objects.create(user=user)
        response_data = {
            'user': user.get_response_data(),
            'auth': {
                'token': token,
                'expiry': instance.expiry
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def sign_in(request):
    serializer = SignInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request=request, user=user)
    instance, token = AuthToken.objects.create(user=user)
    response_data = {
        'user': user.get_response_data(),
        'auth': {
            'token': token,
            'expiry': instance.expiry
        }
    }
    return Response(response_data, status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def load_user(request):
    return Response(request.user.get_response_data())
