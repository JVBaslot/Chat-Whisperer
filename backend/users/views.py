from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def user_counts(request):
    total_users = User.objects.count()
    total_admins = User.objects.filter(is_superuser=True).count()
    return Response({
        'total_users': total_users,
        'total_admins': total_admins,
    })

@api_view(['GET'])
def get_users(request):
    """List all users"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_detail(request, pk):
    """Get a specific user by id"""
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_user(request):
    """Create a new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Handle password separately since it needs to be set with set_password
        password = request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    """Update an existing user"""
    try:
        user = User.objects.get(pk=pk)
        
        # Only allow users to update their own info unless they're admin
        if user != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        # For existing user updates, only allow updating is_superuser and is_staff
        update_data = {}
        if 'is_superuser' in request.data:
            update_data['is_superuser'] = request.data['is_superuser']
        if 'is_staff' in request.data:
            update_data['is_staff'] = request.data['is_staff']
            
        serializer = UserSerializer(user, data=update_data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, pk):
    """Delete a user"""
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)