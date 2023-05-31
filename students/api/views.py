from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from classes.models import Class
from ..models import Student
from .matricule import generate_student_id
from .serializers import CreateStudentSerializer, GetStudentSerializer


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def create_student(request, class_id):
    try:
        student_class = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = "Class not found. You can't assign a student to an unknown class."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not student_class.year.is_active:
        msg = "You can only assign students to a class in the current active academic year."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    serializer = CreateStudentSerializer(data=request.data)

    if serializer.is_valid():
        print('ok')
        student_id = generate_student_id(Student.objects.all())
        student = Student(**serializer.validated_data)
        student.student_class = student_class
        student.student_id = student_id
        student.save()
        return Response(student.get_response_data(), status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def get_all_students_in_class(request, class_id):
    try:
        c = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = f'Class not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetStudentSerializer(c.student_set.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def get_student(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        msg = f'Student not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetStudentSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def get_all_students_in_school(request):
    students = Student.objects.filter(student_class__year__is_active=True)
    serializer = GetStudentSerializer(students, many=True)
    data = {
        'count': students.count(),
        'students': serializer.data
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def delete_student(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        msg = f'Student not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not student.student_class.year.is_active:
        msg = 'You can only delete students from the current academic year'
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def update_student(request, student_id, new_class_id):
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        msg = f'Student not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        c = Class.objects.get(pk=new_class_id)
    except Class.DoesNotExist:
        msg = f'Class not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not c.year.is_active:
        msg = 'You can only edit students in the current academic year.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = CreateStudentSerializer(student, data=request.data)
        if serializer.is_valid():
            student = serializer.save(student_class=c)
            response_serializer = GetStudentSerializer(student)
            return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def get_classes_students_stats(request):
    classes_stats = []
    for c in Class.objects.filter(year__is_active=True):
        classes_stats.append(
            {
                'class': c.name,
                'Boys': c.student_set.filter(gender='Male').count(),
                'Girls': c.student_set.filter(gender='Female').count()
            }
        )

    return Response(classes_stats, status=status.HTTP_200_OK)
