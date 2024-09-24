from django.contrib.auth.models import User
from rest_framework import serializers
import random


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'first_name', 'email']


    def create(self, validated_data):
        username = validated_data.get('username', '')
        if not username:
            first_name = validated_data.get('first_name', '')
            # Create a simple username from first name or random range
            username = first_name.lower() + str(random.randrange(000000, 999999))


        user = User.objects.create_user(
            username=username,
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            email=validated_data.get('email', '')
        )
        return user

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('password')  # Remove password from the output
    #     return representation