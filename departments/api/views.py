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
    department_teachers = department.teacher_set.all()
    teachers_data = []
    for teacher in department_teachers:
        info = {
            'id': teacher.id,
            'name': teacher.get_full_name(),
            'image': teacher.get_image_url(),
            'isHOD': teacher.is_hod
        }
        teachers_data.append(info)

    response_data = {
        'department': serializer.data,
        'teachers': teachers_data
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_departments_info(request):
    departments = Department.objects.all()
    response_data = []
    for department in departments:
        teachers = department.teacher_set.all()
        data = {
            'id': department.pk,
            'name': department.name,
            'teachers': [],
            'numberOfTeachers': teachers.count()
        }
        for teacher in teachers:
            teacher_info = {
                'id': teacher.pk,
                'fullName': teacher.get_full_name(),
                'image': teacher.get_image_url()
            }
            data['teachers'].append(teacher_info)
        response_data.append(data)

    return Response(response_data, status=status.HTTP_200_OK)


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
        if serializer.validated_data.get('HOD_name'):
            new_HOD_name = serializer.validated_data.get('HOD_name')
            department_teachers = department.teacher_set.all()
            for t in department_teachers:
                t.is_hod = False
                t.save()

            HOD = [t for t in department_teachers if t.get_full_name() ==
                   new_HOD_name][0]
            HOD.is_hod = True
            HOD.save()

        new_department = serializer.save()
        new_serializer = GetDepartmentSerializer(new_department)
        department_teachers = new_department.teacher_set.all()
        teachers_data = []
        for teacher in department_teachers:
            info = {
                'id': teacher.id,
                'name': teacher.get_full_name(),
                'image': teacher.get_image_url(),
                'isHOD': teacher.is_hod
            }
            teachers_data.append(info)

        response_data = {
            'department': new_serializer.data,
            'teachers': teachers_data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
