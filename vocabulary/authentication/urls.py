from django.urls.conf import path
from authentication.apiviews import UserRegistrationAPIView, UsernameAPIView, UserAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from authentication.views import SignupView, LoginView
from django.contrib.auth import views as auth_views


app_name = 'authentication'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='login'),
    
    # path('login/', auth_views.LoginView.as_view(template_name="authentication/login.html"), name='login'),

    # REST urls
    path('api/signup/', UserRegistrationAPIView.as_view(), name='api-signup'),
    path('api/fetch-username/', UsernameAPIView.as_view(), name='api-fetch-username'),
    path('api/fetch-user/', UserAPIView.as_view(), name='api-fetch-user'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]