from rest_framework import serializers

from ..models import Sequence


class CreateSequenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sequence
        fields = ['name']


class GetSequenceSerializer(serializers.ModelSerializer):

    sequence_class = serializers.SerializerMethodField()

    def get_sequence_class(self, sequence):
        return sequence.sequence_class.name

    class Meta:
        model = Sequence
        fields = '__all__'
