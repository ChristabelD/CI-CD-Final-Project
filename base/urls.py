from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    TodoViewSet,     UserRegistrationViewSet,    register_user,    get_user_profile,    update_user_profile,    CustomTokenObtainPairView)

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [path('', include(router.urls)),
               path('register/simple/', register_user, name='register_simple'),
               path('profile/', get_user_profile, name='user_profile'),
               path('profile/update/', update_user_profile, name='update_profile'),
               path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),] 