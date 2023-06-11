from rest_framework import serializers


class AbsenceDictField(serializers.DictField):
    child = serializers.CharField()


class AbsenceListField(serializers.ListField):
    child = AbsenceDictField(allow_empty=False)


class CreateOrUpdateAbsentSerializer(serializers.Serializer):

    '''class_list should be with three keys: student_id, is_absent and reason'''
    '''eg {"student_id": "QIS3452", "is_absent": "false", "reason":"Sickness"}'''

    class_list = AbsenceListField(allow_empty=False)
    date = serializers.DateField()
