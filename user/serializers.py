from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, OutstandingToken
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
import re

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_id", "first_name", "last_name", "email", "phone_number", "address", "user_type", "joining_date"]
        read_only =('id', 'user_id', "user_type", 'joining_date')
    
    def update(self, instance, validated_data):
    
        user = self.context['request'].user
        if instance.id==user.id or user.user_type=='admin':
            super().update(instance, validated_data)
            return instance

        raise serializers.ValidationError('Permission denied')
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    class Meta:
        model = User
        fields = ["id", "user_id", "first_name", "last_name", "email","password","confirm_password", "phone_number", "address", "user_type", "joining_date"]
        read_only =("id", 'user_id', 'joining_date')
        # extra_kwargs = {
        #     "password": {"write_only": True},
        # }

    def validate(self, attrs):
        password = attrs.get("password")
        # first_name = attrs.get("first_name")
        phone_number = attrs.get("phone_number")
        email = attrs.get("email")
        confirm_password = attrs.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords doesn't match")
        
        self.user = User.objects.filter(phone_number=phone_number)

        if self.user:
            raise ValidationError("User with this credentials already exist")
        
        return attrs 
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserMinSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ["email", "phone_number", "address"]
        read_only =('user_id', 'joining_date')   


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "password", "token", "user",]

    def get_token(self, instance: dict) -> dict:
        """
        Returns refresh and access tokens
        """
        email = instance.get('username')
        user = User.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return {"refresh": str(refresh), "access": access_token}

    def validate(self, attrs: dict):
        email = attrs.get("username")
        password = attrs.get("password")
        self.request = self.context.get("request")
        self.user = User.objects.filter(email=email).first()

        if not self.user:
            raise ValidationError("User with this username does not exist")
        return attrs

    def get_user(self, instance):
        if self.user:
            return UserMinSerializer(self.user, context={"request": self.request}).data  
    