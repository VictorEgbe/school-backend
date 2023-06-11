from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from knox.auth import TokenAuthentication

from sequences.models import Sequence
from students.models import Student
from terms.models import Term
from ..models import Absence
from .serializers import CreateOrUpdateAbsentSerializer


@api_view(http_method_names=('POST', ))
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, IsAdminUser))
def create_or_update_absences(request):
    try:
        sequence = Sequence.objects.get(is_active=True)
    except Sequence.DoesNotExist:
        msg = 'There is no active sequence. Please create one.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not sequence.term.is_active:
        msg = f'You can only create absences in an active term.'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    if not sequence.term.year.is_active:
        msg = f'You can only create absences in an active year.'
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    serializer = CreateOrUpdateAbsentSerializer(data=request.data)

    if serializer.is_valid():

        date = serializer.validated_data.get('date')
        class_list = serializer.validated_data.get('class_list')

        for student_info in class_list:
            student_id = student_info['student_id']
            reason = student_info.get('reason', '')

            is_absent = student_info['is_absent'] == "true"
            not_absent = student_info['is_absent'] == "false"

            try:
                student = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                msg = 'Student not found'
                return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

            try:
                absence = Absence.objects.get(student=student, date=date)
                if reason and is_absent:
                    absence.reason = reason
                    absence.save()

                if not_absent:
                    absence.delete()

            except Absence.DoesNotExist:

                if not_absent:
                    pass
                elif is_absent:
                    Absence.objects.create(
                        student=student,
                        date=date,
                        sequence=sequence,
                        reason=reason
                    )
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=('GET', ))
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, IsAdminUser))
def get_total_sequence_absences(request, student_id, sequence_id):

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        msg = 'Student not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        sequence = Sequence.objects.get(pk=sequence_id)
    except Sequence.DoesNotExist:
        msg = 'Sequence not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    absences = Absence.objects.filter(student=student, sequence=sequence)
    data = {
        'Student': student.name,
        'student_id': student.student_id,
        'number_of_absences': absences.count(),
        'sequence': sequence.name,
        'term': sequence.term.name,
        'year': sequence.term.year.name
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(http_method_names=('GET', ))
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, IsAdminUser))
def get_total_term_absences(request, student_id, term_id):

    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = 'Term not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        student = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        msg = 'Student not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    absences = Absence.objects.filter(student=student, sequence__term=term)
    data = {
        'Student': student.name,
        'student_id': student.student_id,
        'number_of_absences': absences.count(),
        'term': term.name,
        'year': term.year.name
    }

    return Response(data, status=status.HTTP_200_OK)
