from django.shortcuts import get_object_or_404
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
from teachers.models import Teacher
from students.models import Student
from subjects.models import Subject

from .serializers import GetMarkSerializer, CreateMarkSerializer
from ..models import Mark


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_mark(request, student_id, subject_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        msg = 'Subject not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        msg = 'Student not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not subject.subject_class.year.is_active:
        msg = 'You can only fill marks for subjects in the active year.'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    if not subject in student.student_class.subject_set.all():
        msg = 'The student does not belong to that class'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    teachers = subject.teachers.all()
    teacher_teaches_subject = request.user.id in [t.id for t in teachers]

    if teacher_teaches_subject or request.user.is_superuser:
        serializer = CreateMarkSerializer(data=request.data)
        if serializer.is_valid():
            if Mark.objects.filter(student=student, subject=subject).exists():
                msg = f'Marks already filled for {student.name} in {subject.name}'
                return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                if request.user.is_superuser:
                    mark = serializer.save(
                        subject=subject,
                        student=student,
                        teacher=teachers.first(),
                        value=serializer.validated_data.get('value')
                    )
                else:
                    teacher = Teacher.objects.get(pk=request.user.pk)
                    mark = serializer.save(
                        subject=subject,
                        student=student,
                        teacher=teacher,
                        is_filled=True,
                        value=serializer.validated_data.get('value')
                    )
                response_serializer = GetMarkSerializer(mark)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        msg = 'You can only fill marks for a subject you teach.'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_marks_for_student(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        msg = 'Student not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    marks = student.mark_set.all()
    data = {'student': student.name, 'scores': []}
    for mark in marks:
        d = {
            'subject': mark.subject.name,
            'value': mark.value,
            'taught_by': mark.teacher.get_full_name(),
        }
        data.get('scores').append(d)

    return Response(data)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_all_marks_for_students_in_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)

    students = class_obj.student_set.all()
    marks = []
    for student in students:
        details = {
            'student_details': {'mat': student.student_id, 'name': student.name},
            'score_details': []
        }
        student_marks = student.mark_set.all()
        for mark in student_marks:
            d = {
                'subject': mark.subject.name,
                'value': mark.value,
                'taught_by': mark.teacher.get_full_name(),
            }
            details['score_details'].append(d)
        marks.append(details)
    return Response(marks)
