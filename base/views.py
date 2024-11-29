from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Todo
from .serializers import TodoSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

# Create your views here.

from django.core.mail import send_mail
from django.conf import settings

class UserRegistrationViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            subject = 'Welcome to Our Platform'
            message = render_to_string(
                'welcome_email.html', 
                {'user': user, 'current_year': timezone.now().year}
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
    )
            
            response = Response({
                "user": UserSerializer(user).data,
                "message": "User created successfully",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

            # Add token to response cookies
            response.set_cookie(
                'access_token',
                str(refresh.access_token),
                httponly=True,
                samesite='Strict'
            )
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
            return Todo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        todo = serializer.save(user=self.request.user)

        # Render the todo created email template
        subject = 'New Todo Created'
        message = render_to_string(
            'email/todo_created_email.html',
            {'user': self.request.user, 'todo': todo, 'current_year': timezone.now().year}
        )

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=False,
        )

    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
            todo = self.get_object()
            todo.completed = not todo.completed
            todo.save()
            return Response({'status': 'todo updated'})
    @action(detail=False, methods=['get'])
    def by_category(self, request):
            category = request.query_params.get('category', None)
            if category is None:
                return Response(
                    {'error': 'Category parameter is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            todos = self.get_queryset().filter(category=category)
            serializer = self.get_serializer(todos, many=True)
            return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def categories(self, request):
            # Get unique categories for the user's todos
            categories = self.get_queryset().values_list('category', flat=True).distinct()
            # Filter out None/null values and return as list
            categories = [cat for cat in categories if cat]
            return Response(categories)
    
class UserRegistrationViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response = Response({
                "user": UserSerializer(user).data,
                "message": "User created successfully",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
            # Add token to response cookies
            response.set_cookie(
                'access_token',
                str(refresh.access_token),
                httponly=True,
                samesite='Strict'
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            user_data = UserSerializer(user).data
            response.data['user'] = user_data
        return response

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        subject = 'Welcome to Our Platform'
        message = render_to_string(
                'welcome_email.html', 
                {'user': user, 'current_year': timezone.now().year}
        )

        send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
        )
        return Response({
                "user": UserSerializer(user).data,
            "message": "User created successfully",
            "tokens": {
                    "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
