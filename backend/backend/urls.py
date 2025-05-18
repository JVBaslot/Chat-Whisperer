from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('users.urls')),
    path('admin/', admin.site.urls),
     path('chat/', include('chat.urls')),
 
     path('freedom-wall/', include('freedom_wall.urls')),
]
