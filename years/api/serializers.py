from rest_framework import serializers

from ..models import Year


class CreateYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = Year
        fields = ['name', 'theme']


class GetYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = Year
        fields = ['id', 'name', 'theme', 'is_active']
