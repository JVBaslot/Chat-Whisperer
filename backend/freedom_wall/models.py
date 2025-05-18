from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # Anonymous post when user is null
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='wall_posts',
        null=True,
        blank=True
    )
    # Keep author field for anonymous posts or display name
    author = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
