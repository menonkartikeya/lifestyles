from .models import *
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class foodSerializer(serializers.ModelSerializer):

    class Meta:
        model = food
        fields = '__all__'

class RegSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['username','mobno','password','gender']
        extra_kwargs = {'password': {'write_only': True}}


class otpSerializer(serializers.ModelSerializer):

    class Meta:
        model = otpstore
        fields = ['otp','mobno']


class loginSerializer(serializers.Serializer):
    mobno = serializers.IntegerField()

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

class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['fitness']


class StreakSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['streaks']

class StepsSerializer(serializers.ModelSerializer):
    step_count = serializers.IntegerField()

    class Meta:
        model = MyUser
        fields = ['steps','step_count']
    
    def update(self, instance, validated_data):
        st = validated_data['step_count']
        d = datetime.date.today()
        obj = instance.steps.filter(date=d)
        if not obj:
            ob = step.objects.create(date=d,step_count=st)
            instance.steps.add(ob)
        else:
            for o in obj:
                o.step_count = st
                o.save()
        instance.save()
        return instance

class liveSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['lives']



# Steps - Only POST
# Streak - GET (number , points)
# Live Api - GET (live fields, employee name, employee image, roomid,)
# exercise plan update - (day name)