from rest_framework import serializers

from ..models import Subject


class GetSubjectSerializer(serializers.ModelSerializer):

    teachers = serializers.SerializerMethodField()
    subject_class = serializers.SerializerMethodField()

    def get_teachers(self, subject):
        teachers = subject.teachers.all()
        return [teacher.get_full_name() for teacher in teachers]

    def get_subject_class(self, subject):
        return subject.subject_class.name

    class Meta:
        model = Subject
        fields = '__all__'


class CreateSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['name', 'coefficient', 'code']
