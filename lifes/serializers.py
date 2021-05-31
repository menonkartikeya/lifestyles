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
        fields = ['password', 'password2','mobno']
        extra_kwargs = {'password': {'write_only': True}}
    
    def save(self):
        user = MyUser(
                    mobno=self.validated_data['mobno'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['first_name','last_name','pic','email','height','weight','target','age','bio','location','address']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.pic = validated_data.get('pic', instance.pic)
        instance.email = validated_data.get('email', instance.email)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.target = validated_data.get('target', instance.target)
        instance.age = validated_data.get('age', instance.age)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

class DietSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['diets']

