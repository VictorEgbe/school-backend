from rest_framework import serializers

from ..models import Department


class GetDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class CreateDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'
