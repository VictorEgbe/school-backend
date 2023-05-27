from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)

from knox.auth import TokenAuthentication

from ..models import Year
from .serializers import CreateYearSerializer, GetYearSerializer


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_year(request):
    if Year.objects.filter(is_active=True).exists():
        msg = f"You can't create a new academic year while another is still active."
        return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = CreateYearSerializer(data=request.data)
    if serializer.is_valid():
        year = serializer.save()
        return Response(year.get_response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_year(request, year_id):
    try:
        year = Year.objects.get(id=year_id)
    except Year.DoesNotExist:
        msg = 'Academic year not found'
        return Response({'Error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetYearSerializer(year)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_year(request, year_id):
    try:
        year = Year.objects.get(id=year_id)
    except Year.DoesNotExist:
        msg = 'Academic year not found'
        return Response({'Error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not year.is_active:
        msg = f"You can't update an inactive year."
        return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CreateYearSerializer(year, data=request.data)
    if serializer.is_valid():
        year = serializer.save()
        return Response(year.get_response_data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_year(request, year_id):
    try:
        year = Year.objects.get(id=year_id)
    except Year.DoesNotExist:
        msg = 'Academic year not found'
        return Response({'Error': msg}, status=status.HTTP_404_NOT_FOUND)

    if year.is_active:
        msg = f"You can't delete an academic year while it's active."
        return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)

    year.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_years(request):
    years = Year.objects.all()
    serializer = GetYearSerializer(years, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def deactivate_year(request, year_id):
    try:
        year = Year.objects.get(id=year_id)
    except Year.DoesNotExist:
        msg = 'Academic year not found'
        return Response({'Error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not year.is_active:
        msg = f"You can't deactivate an inactive year."
        return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        year.is_active = False
        year.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
