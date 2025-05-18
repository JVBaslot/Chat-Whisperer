from rest_framework import viewsets, status
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from cryptography.fernet import Fernet
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        # Initialize the Fernet cipher with the encryption key
        self.cipher = Fernet(settings.ENCRYPTION_KEY)
        super().__init__(*args, **kwargs)

    def perform_create(self, serializer):
        sender = self.request.user
        receiver = serializer.validated_data['receiver']
        message_content = serializer.validated_data['content']

        # Encrypt the message content before saving
        encrypted_content = self.cipher.encrypt(message_content.encode()).decode()

        # Save the encrypted message to the database
        serializer.save(sender=sender, receiver=receiver, content=message_content)

    @action(detail=False, methods=['get'], url_path='messages')
    def get_messages_by_sender_receiver(self, request):
        sender_id = request.query_params.get('sender_id')
        receiver_id = request.query_params.get('receiver_id')

        if not sender_id or not receiver_id:
            return Response({'detail': 'Both sender_id and receiver_id parameters are required'}, status=400)

        try:
            sender_id = int(sender_id)  # Ensure the sender_id is valid (integer)
            receiver_id = int(receiver_id)  # Ensure the receiver_id is valid (integer)
        except ValueError:
            return Response({'detail': 'Invalid sender_id or receiver_id format'}, status=400)

        # Retrieve messages for the given sender and receiver IDs
        messages = Message.objects.filter(sender__id=sender_id, receiver__id=receiver_id)

        # Decrypt the message content
        decrypted_messages = []
        for message in messages:
            decrypted_content = self.cipher.decrypt(message.content.encode()).decode()
            decrypted_message = {
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'content': decrypted_content,
                'timestamp': message.timestamp,
            }
            decrypted_messages.append(decrypted_message)

        return Response(decrypted_messages)

    @action(detail=False, methods=['get'], url_path='conversation-messages')
    def get_conversation_messages(self, request):
        sender_id = request.query_params.get('sender_id')
        receiver_id = request.query_params.get('receiver_id')

        if not sender_id or not receiver_id:
            return Response({'detail': 'Both sender_id and receiver_id parameters are required'}, status=400)

        try:
            sender_id = int(sender_id)  # Ensure the sender_id is valid (integer)
            receiver_id = int(receiver_id)  # Ensure the receiver_id is valid (integer)
        except ValueError:
            return Response({'detail': 'Invalid sender_id or receiver_id format'}, status=400)

        # Retrieve messages for the given sender and receiver IDs
        messages = Message.objects.filter(sender__id=sender_id, receiver__id=receiver_id)

        # Directly return the message content without decryption
        message_data = []
        for message in messages:
            message_data.append({
                'sender': message.sender.name,
                'receiver': message.receiver.name,
                'content': message.content,  # No decryption, just raw content
                'timestamp': message.timestamp,
            })

        return Response(message_data)

    @action(detail=False, methods=['get'], url_path='messages-by-sender')
    def get_messages_by_sender(self, request):
        sender_id = request.query_params.get('sender_id')
        if not sender_id:
            return Response({'detail': 'sender_id parameter is required'}, status=400)

        try:
            sender_id = int(sender_id)  # Ensure the sender_id is valid (integer)
        except ValueError:
            return Response({'detail': 'Invalid sender_id format'}, status=400)

        # Retrieve messages for the given sender ID
        messages = Message.objects.filter(sender__id=sender_id)

        # Decrypt the message content
        decrypted_messages = []
        for message in messages:
            decrypted_content = self.cipher.decrypt(message.content.encode()).decode()
            decrypted_message = {
                'sender': message.sender.name,
                'receiver': message.receiver.name,
                'content': decrypted_content,
                'timestamp': message.timestamp,
            }
            decrypted_messages.append(decrypted_message)

        return Response(decrypted_messages)

    @action(detail=False, methods=['get'], url_path='messages-by-receiver')
    def get_messages_by_receiver(self, request):
        receiver_id = request.query_params.get('receiver_id')
        if not receiver_id:
            return Response({'detail': 'receiver_id parameter is required'}, status=400)

        try:
            receiver_id = int(receiver_id)  # Ensure the receiver_id is valid (integer)
        except ValueError:
            return Response({'detail': 'Invalid receiver_id format'}, status=400)

        # Retrieve messages for the given receiver ID
        messages = Message.objects.filter(receiver__id=receiver_id)

        # Decrypt the message content
        decrypted_messages = []
        for message in messages:
            decrypted_content = self.cipher.decrypt(message.content.encode()).decode()
            decrypted_message = {
                'sender': message.sender.name,
                'receiver': message.receiver.name,
                'content': decrypted_content,
                'timestamp': message.timestamp,
            }
            decrypted_messages.append(decrypted_message)

        return Response(decrypted_messages)

    @action(detail=False, methods=['get'], url_path='specific-chat')
    def get_specific_chat(self, request):
        sender_id = request.query_params.get('sender_id')
        receiver_id = request.query_params.get('receiver_id')

        if not sender_id or not receiver_id:
            return Response({'detail': 'Both sender_id and receiver_id parameters are required'}, status=400)

        try:
            sender_id = int(sender_id)
            receiver_id = int(receiver_id)
        except ValueError:
            return Response({'detail': 'Invalid sender_id or receiver_id format'}, status=400)

        # Retrieve messages for the given sender and receiver IDs
        messages = Message.objects.filter(
            sender__id=sender_id, receiver__id=receiver_id
        ).order_by('timestamp')

        # Decrypt the message content
        decrypted_messages = []
        for message in messages:
            decrypted_content = self.cipher.decrypt(message.content.encode()).decode()
            decrypted_message = {
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'content': decrypted_content,
                'timestamp': message.timestamp,
            }
            decrypted_messages.append(decrypted_message)

        return Response(decrypted_messages)
        
    @action(detail=True, methods=['delete'], url_path='delete-message')
    def delete_message(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
            
            # Check if the user is authorized to delete this message
            if message.sender != request.user:
                return Response(
                    {'detail': 'You are not authorized to delete this message'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Delete the message
            message.delete()
            return Response(
                {'detail': 'Message deleted successfully'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Message.DoesNotExist:
            return Response(
                {'detail': 'Message not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    @action(detail=True, methods=['put', 'patch'], url_path='update-message')
    def update_message(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
            
            # Check if the user is authorized to update this message
            if message.sender != request.user:
                return Response(
                    {'detail': 'You are not authorized to update this message'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Get the new content from the request
            new_content = request.data.get('content')
            if not new_content:
                return Response(
                    {'detail': 'Content is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Encrypt the new content
            encrypted_content = self.cipher.encrypt(new_content.encode()).decode()
            
            # Update the message
            message.content = encrypted_content
            message.save()
            
            return Response(
                {'detail': 'Message updated successfully'}, 
                status=status.HTTP_200_OK
            )
        except Message.DoesNotExist:
            return Response(
                {'detail': 'Message not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
