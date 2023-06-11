from rest_framework import serializers

from ..models import Mark


class GetMarkSerializer(serializers.ModelSerializer):

    teacher = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()
    sequence = serializers.SerializerMethodField()

    def get_teacher(self, mark):
        return mark.teacher.get_full_name()

    def get_student(self, mark):
        return mark.student.name

    def get_class_name(self, mark):
        return mark.student.student_class.name

    def get_subject(self, mark):
        return mark.subject.name

    def get_sequence(self, mark):
        return mark.sequence.name

    class Meta:
        model = Mark
        fields = '__all__'


class CreateMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mark
        fields = ['value']


class MarkDictField(serializers.DictField):
    child = serializers.CharField()


class MarkListField(serializers.ListField):
    child = MarkDictField(allow_empty=False)


class CreateOrUpdateMarkSerializer(serializers.Serializer):
    '''class_list should be with two keys: student_id and subject_score'''
    '''e.g {"student_id": "QIS3452", "subject_score": 12.5}'''

    class_list = MarkListField(allow_empty=False)
