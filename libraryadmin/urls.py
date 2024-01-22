from django.urls import path
from rest_framework import routers
from .views import BookListCreateApiView, BookRetrieveUpdateDestroyAPIView, BookLogCreateApiView, BookLogUpdatepiView

router = routers.DefaultRouter()

# router.register('book/', BookModelViewSet, basename='book')
urlpatterns = [
    path("book-register/", BookListCreateApiView.as_view(), name="book-register"),
    path("book-update/<int:id>/", BookRetrieveUpdateDestroyAPIView.as_view(), name="book-update"),
    path('booklog-create/', BookLogCreateApiView.as_view(), name='booklog-create'),
    path("booklog-update/<int:id>/", BookLogUpdatepiView.as_view(), name="booklog-update"),
]
urlpatterns += router.urls