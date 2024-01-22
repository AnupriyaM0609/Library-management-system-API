from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from .backends import EmailUsernameAuthenticationBackend

from .models import User
from libraryadmin.models import Booklog
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

# Create your views here.

class UserRegistrationAPIView(CreateAPIView):
    """
    API to register
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserLoginAPIView(CreateAPIView):
    """
    API to login
    """
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]    

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={"request" : request})
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        
        if not user:
            raise ValidationError("Invalid username or password")

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)
        

class UserRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    """
    API to view,update and delete
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        serializer = self.get_serializer(instance)

        if instance.id==user.id or user.user_type=='admin':
            return Response(serializer.data)
        raise ValidationError('Authenticated person can only update their profile')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        user = self.request.user
        
        if instance.id==user.id or user.user_type=='admin':
            retunrn_book = Booklog.objects.filter(user=instance.id, return_date__isnull=True)
            if retunrn_book:
                raise ValidationError("You can't delete your profile with out returing the books")
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError('Authenticated person can only delete their profile')
    
    
class UserListApiView(ListAPIView):
    """
    List a queryset.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset()).order_by('joining_date')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        if user.user_type=='admin':
            return Response(serializer.data)
        raise ValidationError('Only admin can access ')
