from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import user_counts
from . import api, views

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', api.get_all_users, name='get_all_users'),
    path('user-counts/', views.user_counts, name='user-counts'),
    path('users/create/', views.create_user, name='create-user'),
    path('users/<int:pk>/', views.get_user_detail, name='user-detail'),
    path('users/<int:pk>/update/', views.update_user, name='update-user'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete-user'),
]