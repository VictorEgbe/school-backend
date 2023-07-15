from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from accounts.models import User
from departments.models import Department

from .serializers import (
    CreateTeacherSerializer,
    GetTeacherSerializer,
    GetAllTeachersSerializer,
    UpdateTeacherSerializer,
    TeacherChangePasswordSerializer,
)
from ..models import Teacher


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_teacher(request, department_id):
    try:
        department = Department.objects.get(pk=department_id)
    except Department.DoesNotExist:
        msg = 'Department not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = CreateTeacherSerializer(data=request.data)

    if serializer.is_valid():
        teacher = Teacher()
        teacher.first_name = serializer.validated_data.get('first_name')
        teacher.last_name = serializer.validated_data.get('last_name')
        teacher.email = serializer.validated_data.get('email')
        teacher.gender = serializer.validated_data.get('gender')
        teacher.phone = serializer.validated_data.get('phone')
        teacher.set_password(serializer.validated_data.get('password'))
        teacher.department = department

        date_of_birth = serializer.validated_data.get('date_of_birth')
        username = serializer.validated_data.get('username')
        image = serializer.validated_data.get('image')
        address = serializer.validated_data.get('address')
        if date_of_birth:
            teacher.date_of_birth = date_of_birth

        if username:
            teacher.username = username

        if image:
            teacher.image = image

        if address:
            teacher.address = address

        teacher.save()
        return Response(GetTeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_teachers(request):
    teachers = Teacher.objects.all()
    serializer = GetAllTeachersSerializer(teachers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetTeacherSerializer(teacher)

    classes = []

    for subject in teacher.subject_set.all():
        subject_info = {
            'NameOfClass': subject.subject_class.name,
            'subjectTaught': subject.name
        }
        classes.append(subject_info)

    teachers_of_same_department = []
    for t in Teacher.objects.filter(department=teacher.department).exclude(pk=teacher.pk):
        t_info = {
            'id': t.pk,
            'name': t.get_full_name(),
            'isHOD': t.is_hod,
            'image': t.get_image_url()
        }
        teachers_of_same_department.append(t_info)

    response_data = {
        'teacherInfo': serializer.data,
        'classes': classes,
        'similarTeachers': teachers_of_same_department
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    account = User.objects.get(pk=teacher.pk)
    teacher.delete()
    if account:
        account.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_teacher(request, teacher_id, new_department_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        new_department = Department.objects.get(pk=new_department_id)
    except Department.DoesNotExist:
        msg = 'Department not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateTeacherSerializer(teacher, data=request.data)

    if serializer.is_valid():
        updated_teacher = serializer.save(department=new_department)
        return Response(GetTeacherSerializer(updated_teacher).data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def teacher_password_change(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
        password = serializer.validated_data.get('password1')
        teacher.set_password(password)
        teacher.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
