"""
apppppppppppppppp
"""
# from django.contrib import admin
# from django.urls import path
# from . import views

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
     path('', views.index),
     path('about/', views.about),
     path('login/', views.MyTokenObtainPairView.as_view()),
     path('register/', views.register),
     path('logout/', views.logout),
     path('tasks/', views.tasks),  # URL for listing and creating tasks
     path('tasks/<int:id>/', views.tasks), 
  
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)