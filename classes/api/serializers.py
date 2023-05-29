from rest_framework import serializers

from ..models import Class


class CreateClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ['name', 'theme']


class GetClassSerializer(serializers.ModelSerializer):

    year = serializers.SerializerMethodField()

    def get_year(self, obj):
        return obj.year.name

    class Meta:
        model = Class
        fields = '__all__'
