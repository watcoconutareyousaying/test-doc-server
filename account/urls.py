from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import RegisterView, LogoutView, RegisterTemplateView, login_view, UserProfileView


urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="api-register"),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterTemplateView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),

]
