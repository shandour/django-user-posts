import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    upvoted_by = models.ManyToManyField(User, related_name='liked_posts')
    downvoted_by = models.ManyToManyField(User, related_name='disliked_posts')

    def __str__(self):
        return f'Post {self.pk} by {self.user.email}'

    @property
    def score(self):
        return self.upvoted_by.count() - self.downvoted_by.count()

    @property
    def likes(self):
        return self.upvoted_by.count()

    @property
    def dislikes(self):
        return self.downvoted_by.count()
