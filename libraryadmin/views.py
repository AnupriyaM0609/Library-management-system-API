from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from .models import Book, Booklog
from .serializers import BookSerializer, BookLogSerializer


# Create your views here.
class BookListCreateApiView(ListCreateAPIView):
    """
    API to list and register
    """
    queryset = Book
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        user = self.request.user
        book = self.request.query_params.get('book', '')
        author = self.request.query_params.get('author', '')
        genre = self.request.query_params.get('genre','')

        if not user.user_type=='admin':
            return Response('Only admin can access')
        
        if book:
            queryset = Book.objects.filter(name__icontains=book)

        elif author:    
            queryset = Book.objects.filter(author__icontains=author) 

        elif genre:
            queryset = Book.objects.filter(book_genre__icontains=genre)  

        else:      
            queryset = Book.objects.all()

        serializer = self.get_serializer(queryset,many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
 

class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API to update and delete
    """
    queryset = Book
    serializer_class = BookSerializer
    lookup_field = 'id'
   
    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        if not user.user_type=='admin':
            return Response('Only admin can access')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

class BookLogCreateApiView(ListCreateAPIView):
    """
    API to register booklog details
    """
    queryset = Booklog.objects.all()
    serializer_class = BookLogSerializer
    
    def list(self, request, *args, **kwargs):
        book_name = self.request.query_params.get('book_name')
        user = self.request.user

        if not user.user_type=='admin':
            return Response('Only admin can access')
        
        if book_name:
            book = Booklog.objects.filter(book__name__icontains=book_name, return_date__isnull=True).values()
            return Response({'data':book})
            
        return super().list(request, *args, **kwargs)
    

class BookLogUpdatepiView(UpdateAPIView): 
    """
    API to return books
    """
    queryset = Booklog.objects.all()
    serializer_class = BookLogSerializer
    lookup_field = 'id'
