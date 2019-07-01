from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from . import views

user_api_patterns = [
    path('register/', views.Register.as_view()),
    path('<uuid:pk>/', views.ManipulateUserView.as_view()),
    path('enrichment/', views.get_info),
    path('token/', jwt_views.TokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
]

urlpatterns = [
    path('users/', include(user_api_patterns))
]
