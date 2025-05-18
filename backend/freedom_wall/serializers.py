from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    is_anonymous = serializers.BooleanField(write_only=True, required=False, default=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author_name', 'created_at', 'updated_at', 'is_anonymous']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author
        elif obj.user:
            return obj.user.name
        return "Anonymous"
    
    def create(self, validated_data):
        is_anonymous = validated_data.pop('is_anonymous', True)
        request = self.context.get('request')
        
        if not is_anonymous and request and request.user.is_authenticated:
            validated_data['user'] = request.user
            # Use user's name as author if they're not posting anonymously
            validated_data['author'] = request.user.name
        else:
            # For anonymous posts, don't link to user account
            validated_data['user'] = None
            validated_data['author'] = "Anonymous"
            
        return super().create(validated_data)
