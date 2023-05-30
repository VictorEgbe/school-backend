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
        # student = serializer.save(student_class=student_class, student_id=student_id)
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
    pass


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def get_student(request, student_id, class_id):
    pass


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def get_all_students_in_school(request):
    pass


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def delete_student(request, student_id):
    pass


@api_view(http_method_names=['UPDATE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser, IsAuthenticated])
def update_student(request, student_id, new_class_id):
    pass
