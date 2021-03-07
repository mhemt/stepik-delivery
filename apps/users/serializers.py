from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        username = validated_data['email'].split('@')[0]
        user = get_user_model().objects.create(
            email=validated_data['email'],
            username=username,
            password=make_password(username),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
        )

        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'address',
        ]
        extra_kwargs = {
            'username': {'required': False},
            'middle_name': {'required': False},
            'phone': {'required': False},
            'address': {'required': False},
        }
