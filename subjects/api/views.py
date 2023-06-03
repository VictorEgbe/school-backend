from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from .serializers import (
    GetSubjectSerializer,
    CreateSubjectSerializer
)
from ..models import Subject
from teachers.models import Teacher
from classes.models import Class


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_subjects_in_a_class(request, class_id):
    try:
        class_obj = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = 'Class not Found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    subjects = Subject.objects.filter(subject_class=class_obj)
    serializer = GetSubjectSerializer(subjects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_single_subject_in_a_class(request, subject_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        msg = 'Subject not Found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetSubjectSerializer(subject)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_subjects_by_a_teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not Found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    subjects = teacher.subject_set.all()
    serializer = GetSubjectSerializer(subjects, many=True)
    # TODO: Add teacher's info along with the response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_subject_in_class(request, class_id, teacher_id):
    try:
        class_obj = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = 'Class not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not class_obj.year.is_active:
        msg = 'You can only create a subject in the current active year'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    serializer = CreateSubjectSerializer(data=request.data)
    if serializer.is_valid():
        subject = serializer.save(teachers=[teacher], subject_class=class_obj)
        return Response(GetSubjectSerializer(subject).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_subject(request, subject_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        msg = 'Subject not Found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not subject.subject_class.year.is_active:
        msg = "You can only delete a subject from the current active year"
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    subject.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_subject(request, subject_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        msg = 'Subject not Found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not subject.subject_class.year.is_active:
        msg = "You can only update a subject from the current active year"
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    serializer = CreateSubjectSerializer(subject, data=request.data)
    if serializer.is_valid():
        updated_subject = serializer.save()
        return Response(GetSubjectSerializer(updated_subject).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_teacher_to_subject(request, subject_id, teacher_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        msg = 'Subject not Found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not subject.subject_class.year.is_active:
        msg = "You can only add a teacher in a subject from the current active year"
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    subject.teachers.add(teacher)
    subject.save()
    serializer = GetSubjectSerializer(subject)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def remove_teacher_to_subject(request, subject_id, teacher_id):
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        msg = 'Subject not Found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not subject.subject_class.year.is_active:
        msg = "You can only remove a teacher in a subject from the current active year"
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        msg = 'Teacher not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    subject.teachers.remove(teacher)
    subject.save()
    serializer = GetSubjectSerializer(subject)
    return Response(serializer.data, status=status.HTTP_200_OK)
