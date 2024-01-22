from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserRetrieveUpdateDestroyApiView, UserListApiView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-registration/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('user-login/', UserLoginAPIView.as_view(), name='user-login'),
    path('user-update/<int:id>/', UserRetrieveUpdateDestroyApiView.as_view(), name='user-update'),
    path('user-list/', UserListApiView.as_view(), name='user-list')


]