from rest_framework import serializers

from ..models import Mark


class GetMarkSerializer(serializers.ModelSerializer):

    teacher = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()

    def get_teacher(self, mark):
        return mark.teacher.get_full_name()

    def get_student(self, mark):
        return mark.student.name

    def get_class_name(self, mark):
        return mark.student.student_class.name

    def get_subject(self, mark):
        return mark.subject.name

    class Meta:
        model = Mark
        fields = '__all__'


class CreateMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mark
        fields = ['value']
