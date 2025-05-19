from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Post operations
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def perform_update(self, serializer):
        # Only allow post owners to update their posts
        if self.request.user.is_authenticated:
            instance = self.get_object()
            if instance.user == self.request.user or self.request.user.is_staff:
                serializer.save()
                return None  # Return None to indicate success
            else:
                return Response({"detail": "You do not have permission to edit this post."}, 
                               status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Authentication required."}, 
                       status=status.HTTP_401_UNAUTHORIZED)
    
    def perform_destroy(self, instance):
        # Only allow post owners or staff to delete posts
        if instance.user == self.request.user or self.request.user.is_staff:
            instance.delete()
        else:
            return Response({"detail": "You do not have permission to delete this post."}, 
                           status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, methods=['get'])
    def user_posts(self, request):
        user_id = request.query_params.get('user_id', None)
        if user_id is None:
            return Response({"detail": "User ID is required."}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        posts = Post.objects.filter(user_id=user_id)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete_post(self, request, pk=None):
        post = self.get_object()
        if post.user == request.user or request.user.is_staff:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this post."}, 
                           status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=True, methods=['put', 'patch'])
    def update_post(self, request, pk=None):
        post = self.get_object()
        if post.user == request.user or request.user.is_staff:
            serializer = self.get_serializer(post, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # Even if is_anonymous is True, we still save the user_id
            # The serializer will handle displaying "Anonymous" for the author field
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"detail": "You do not have permission to update this post."}, 
                           status=status.HTTP_403_FORBIDDEN)
