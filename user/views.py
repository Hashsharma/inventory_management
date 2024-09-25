from django.shortcuts import render

# Create your views here.


# views.py

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

# User Registration View
@api_view(['POST'])
def register(request):
    email = request.POST.get('email')
    if User.objects.filter(email=email).exists():
        return Response({'error': 'User already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_data = serializer.data.copy()
        user_data.pop('password')  # Remove the password
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username', '')
    password = request.data.get('password')

    # Check if username is provided, otherwise use email
    if not username:
        email = request.data.get('email', '')

        if not email:
            return Response({'error': 'Please provide a valid username or email'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(email=email).first()
        if user:
            username = user.username
        else:
            return Response({'error': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check password
    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }, status=status.HTTP_200_OK)