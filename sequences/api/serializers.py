from rest_framework import serializers

from ..models import Sequence


class CreateSequenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sequence
        fields = ['name']


class GetSequenceSerializer(serializers.ModelSerializer):

    term = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    def get_term(self, sequence):
        return sequence.term.name

    def get_year(self, sequence):
        return sequence.term.year.name

    class Meta:
        model = Sequence
        fields = '__all__'
