from .models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class foodSerializer(serializers.ModelSerializer):

    class Meta:
        model = food
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = MyUser
        fields = ['email','username','password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
    
    def save(self):
        user = MyUser(email=self.validated_data['email'],
                    username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

# class ProfileSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = MyUser
#         fields = '__all__'

#     def update(self, instance, validated_data):
#         instance.email = validated_data.get('email', instance.email)
#         instance.height = validated_data.get('height', instance.height)
#         instance.weight = validated_data.get('weight', instance.weight)
#         instance.target = validated_data.get('target', instance.target)
#         instance.age = validated_data.get('age', instance.age)
#         instance.bio = validated_data.get('bio', instance.bio)
#         instance.location = validated_data.get('location', instance.location)
#         instance.address = validated_data.get('address', instance.address)
#         instance.save()
#         return instance

