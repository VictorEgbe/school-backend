from rest_framework import serializers

from ..models import Student


class GetStudentSerializer(serializers.ModelSerializer):

    student_class = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    def get_student_class(self, student):
        return student.student_class.name

    def get_age(self, student):
        return student.get_age()

    class Meta:
        model = Student
        fields = '__all__'


class CreateStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'name',
            'date_of_birth',
            'gender',
            'image',
            'student_phone',
            'parent_name',
            'parent_phone',
        ]

    # def save(self, **kwargs):
    #     student_class = kwargs['student_class']
    #     student_id = kwargs['student_id']

    #     student = Student.objects.create(
    #         student_class=student_class,
    #         student_id=student_id,
    #         **self.validated_data
    #     )
    #     return student
