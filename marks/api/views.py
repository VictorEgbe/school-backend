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
from sequences.models import Sequence

from .serializers import GetMarkSerializer, CreateMarkSerializer, CreateOrUpdateMarkSerializer
from ..models import Mark


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_or_update_mark(request, class_id, subject_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        msg = 'Subject not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        _class = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = 'Class not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not subject.subject_class.year.is_active:
        msg = 'You can only fill marks for subjects in the active year.'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    if not subject in _class.subject_set.all():
        msg = 'The student does not belong to that class'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    try:
        sequence = Sequence.objects.get(is_active=True)
    except Sequence.DoesNotExist:
        msg = 'There are no active sequence at this moment. Please contact the admin.'
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not sequence.term.year.is_active:
        msg = 'You can only submit marks for an active year.'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    teachers = subject.teachers.all()
    teacher_teaches_subject = request.user.id in [t.id for t in teachers]

    if teacher_teaches_subject or request.user.is_superuser:
        serializer = CreateOrUpdateMarkSerializer(data=request.data)
        if serializer.is_valid():
            class_list = serializer.validated_data['class_list']

            for student_info in class_list:

                student_id = student_info['student_id']
                subject_score = student_info['value']

                try:
                    float(subject_score)
                except (ValueError, TypeError):
                    msg = f'"{subject_score}" is not a valid score...'
                    return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

                if float(subject_score) < 0 or float(subject_score) > 20:
                    msg = f'{subject_score} is not a valid score.'
                    return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

                if len(str(float(subject_score)).split('.')[1]) > 2:
                    msg = f'{subject_score} is not a valid score.Too many decimal digits.'
                    return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

                try:
                    student = Student.objects.get(student_id=student_id)
                except Student.DoesNotExist:
                    msg = 'Student not found'
                    return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

                try:
                    mark = Mark.objects.get(
                        student=student, subject=subject, sequence=sequence)
                    mark.value = subject_score
                    mark.save()

                except Mark.DoesNotExist:
                    if request.user.is_superuser:
                        mark = Mark.objects.create(
                            subject=subject,
                            student=student,
                            sequence=sequence,
                            teacher=teachers.first(),
                            value=subject_score,
                            is_filled=True,
                        )
                    else:
                        teacher = Teacher.objects.get(pk=request.user.pk)
                        Mark.objects.create(
                            subject=subject,
                            student=student,
                            sequence=sequence,
                            teacher=teacher,
                            is_filled=True,
                            value=subject_score
                        )

            return Response(status=status.HTTP_201_CREATED)
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
            'sequence': mark.sequence.name,
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


@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_mark(request, mark_id):
    try:
        mark = Mark.objects.get(pk=mark_id)
    except Mark.DoesNotExist:
        msg = 'The mark you want to update was not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    teachers = mark.subject.teachers.all()
    teacher_teaches_subject = request.user.id in [t.id for t in teachers]

    if teacher_teaches_subject or request.user.is_superuser:
        serializer = CreateMarkSerializer(mark, data=request.data)

        if serializer.is_valid():
            updated_mark = serializer.save()
            return Response(GetMarkSerializer(updated_mark).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        msg = 'You can only fill marks for a subject you teach.'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)
