from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from knox.auth import TokenAuthentication

from years.models import Year
from terms.models import Term
from sequences.models import Sequence
from students.models import Student
from departments.models import Department
from teachers.models import Teacher
from accounts.models import User
from classes.models import Class


@api_view(http_method_names=('GET',))
@permission_classes((IsAuthenticated, IsAdminUser))
@authentication_classes((TokenAuthentication, ))
def dashboard(request):
    try:
        current_year = Year.objects.get(is_active=True)
    except Year.DoesNotExist:
        msg = 'There is no information at this moment.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        current_term = current_year.term_set.get(is_active=True)
    except Term.DoesNotExist:
        msg = 'You have not created an active term yet.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        current_sequence = Sequence.objects.get(is_active=True)
    except Sequence.DoesNotExist:
        msg = 'You have not created an active sequence yet.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    students = Student.objects.count()
    teachers = Teacher.objects.count()
    departments = Department.objects.count()
    admins = User.objects.filter(is_staff=True)
    class_students = []
    for _class in Class.objects.filter(year=current_year):
        total_students_in_class = _class.student_set.all()
        boys = total_students_in_class.filter(gender='Male').count()
        girls = total_students_in_class.filter(gender='Female').count()
        data = {'name': _class.name, 'total': total_students_in_class.count(),
                'boys': boys, 'girls': girls}
        class_students.append(data)

    departments_info = []
    for department in Department.objects.all():
        name = department.name
        number_of_teachers = department.teacher_set.count()
        data = {'name': name, 'numberOfTeachers': number_of_teachers}
        departments_info.append(data)

    response_data = {
        'currentYear': current_year.name,
        'currentTerm': current_term.name,
        'currentSequence': current_sequence.name,
        'students': students,
        'teachers': teachers,
        'admins': admins.count(),
        'departments': departments,
        'classStudents': class_students,
        'departmentsInfo': departments_info
    }

    return Response(response_data, status=status.HTTP_200_OK)
