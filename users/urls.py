from django.urls import path, include

from . import views

user_api_patterns = [
    path('register/', views.Register.as_view()),
    path('<uuid:pk>/', views.ManipulateUserView.as_view()),
    path('enrichment/', views.get_info),
]

urlpatterns = [
    path('users/', include(user_api_patterns))
]
