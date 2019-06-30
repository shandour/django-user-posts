from django.urls import path, include

from . import views

post_api_patterns = [
    path('', views.DisplayPosts.as_view()),
    path('<uuid:pk>/', views.ManipulatePostView.as_view()),
    path('react/', views.react_to_post),
]

urlpatterns = [
    path('posts/', include(post_api_patterns))
]
