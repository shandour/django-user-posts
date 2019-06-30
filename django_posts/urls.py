from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from users.urls import urlpatterns as user_patterns
from posts.urls import urlpatterns as post_patterns

api_patterns = user_patterns + post_patterns

urlpatterns = [
    path('api/', include(api_patterns)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]
