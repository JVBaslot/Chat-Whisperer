from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/posts/<int:pk>/delete/', PostViewSet.as_view({'delete': 'delete_post'}), name='delete_post'),
    path('api/posts/<int:pk>/update/', PostViewSet.as_view({'put': 'update_post', 'patch': 'update_post'}), name='update_post'),
]
