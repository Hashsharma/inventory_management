# urls.py

from django.urls import path
from .views import register,  login
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
