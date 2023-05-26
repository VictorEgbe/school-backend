from rest_framework import serializers

from ..models import Year


class CreateYearSerializer(serializers.ModelSerializer):

    class Meta:
        model = Year
        fields = ['name', 'theme', 'is_active']
