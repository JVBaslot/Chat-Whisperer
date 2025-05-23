from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

# Create a router and register the MessageViewSet
router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/messages/', MessageViewSet.as_view({'get': 'get_messages_by_sender_receiver'}), name='messages_by_sender_receiver'),
    path('api/messages-by-sender/', MessageViewSet.as_view({'get': 'get_messages_by_sender'}), name='messages_by_sender'),
    path('api/messages-by-receiver/', MessageViewSet.as_view({'get': 'get_messages_by_receiver'}), name='messages_by_receiver'),
    path('api/conversation-messages/', MessageViewSet.as_view({'get': 'get_conversation_messages'}), name='conversation_messages'),
    path('api/specific-chat/', MessageViewSet.as_view({'get': 'get_specific_chat'}), name='specific_chat'),
    path('api/messages/<int:pk>/delete/', MessageViewSet.as_view({'delete': 'delete_message'}), name='delete_message'),
    path('api/messages/<int:pk>/update/', MessageViewSet.as_view({'put': 'update_message', 'patch': 'update_message'}), name='update_message'),
]
