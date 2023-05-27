from rest_framework import serializers

from ..models import Term


class CreateTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ['name']

    def save(self, **kwargs):

        year = kwargs['year']
        name = self.validated_data['name']

        if Term.objects.filter(name=name, year=year).exists():
            msg = f'{name} already created for the year {year.name}'
            raise serializers.ValidationError({'error': msg})

        term = Term()
        term.year = year
        term.name = name
        term.save()
        return term


class GetTermSerializer(serializers.ModelSerializer):

    year = serializers.SerializerMethodField()

    def get_year(self, term):
        return term.year.name

    class Meta:
        model = Term
        fields = '__all__'


class UpdateTermSerializer(serializers.Serializer):
    name = serializers.CharField()
