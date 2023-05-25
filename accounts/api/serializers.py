from django.contrib.auth import authenticate
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


from ..models import User


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'phone',
            'password',
            'password2',
            'first_name',
            'last_name',
            'gender',
            'email'
        ]
        extra_kwargs = {'password': {'write_only': True},
                        'style': {'input_type': 'password'}}

    def validate_password(self, password):
        password2 = self.initial_data.get('password2')
        if not password == password2:
            msg = 'Passwords must match.'
            raise serializers.ValidationError(msg, code='authorization')
        return password

    def save(self):
        password = self.validated_data.get('password')
        user = User()
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.gender = self.validated_data.get('gender')
        user.email = self.validated_data.get('email')
        user.phone = self.validated_data.get('phone')
        user.set_password(password)
        user.save()
        return user


class SignInSerializer(serializers.Serializer):
    phone = PhoneNumberField(region='CM')
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        password = attrs.get('password', '')
        user = authenticate(request=self.context.get(
            'request'), phone=phone, password=password)
        if not user or (not user.is_active):
            msg = 'Wrong phone number or password'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'phone',
            'username',
            'first_name',
            'last_name',
            'gender',
            'email',
            'image'
        ]


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
