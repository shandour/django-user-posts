from django.urls import path, include

from users.urls import urlpatterns as user_patterns
from posts.urls import urlpatterns as post_patterns

api_patterns = user_patterns + post_patterns

urlpatterns = [
    path('api/', include(api_patterns)),
]
