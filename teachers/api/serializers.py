from rest_framework import serializers

from ..models import Teacher


class GetTeacherSerializer(serializers.ModelSerializer):

    department = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_department(self, teacher):
        return teacher.department.name

    def get_age(self, teacher):
        return teacher.get_age()

    def get_full_name(self, teacher):
        return teacher.get_full_name()

    class Meta:
        model = Teacher
        fields = [
            'id',
            'phone',
            'username',
            'first_name',
            'last_name',
            'gender',
            'email',
            'image',
            'address',
            'date_of_birth',
            'department',
            'age',
            'full_name'
        ]


class CreateTeacherSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = Teacher
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate_password2(self, password2):
        password = self.initial_data.get('password')
        if not password == password2:
            msg = 'Passwords must match.'
            raise serializers.ValidationError(msg, code='authorization')
        return password2
