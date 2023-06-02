from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from ..models import Department
from .serializers import CreateDepartmentSerializer, GetDepartmentSerializer


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_department(request):
    serializer = CreateDepartmentSerializer(data=request.data)
    if serializer.is_valid():
        department = serializer.save()
        return Response(GetDepartmentSerializer(department).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_department(request, department_id):
    try:
        department = Department.objects.get(pk=department_id)
    except Department.DoesNotExist:
        msg = f'Department not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetDepartmentSerializer(department)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_departments(request):
    departments = Department.objects.all()
    serializer = GetDepartmentSerializer(departments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_department(request, department_id):
    try:
        department = Department.objects.get(pk=department_id)
    except Department.DoesNotExist:
        msg = f'Department not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    department.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_department(request, department_id):
    try:
        department = Department.objects.get(pk=department_id)
    except Department.DoesNotExist:
        msg = f'Department not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = CreateDepartmentSerializer(department, data=request.data)

    if serializer.is_valid():
        new_department = serializer.save()
        return Response(GetDepartmentSerializer(new_department).data)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
