from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from .models import Post
from .serializers import PostSerializer
from .utils import process_reaction
from .constants import REACTION_STATUSES


class DisplayPosts(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.order_by('last_edited')


class ManipulatePostView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if (
            request.method != 'GET'
            and not request.user.posts.filter(pk=obj.pk).exists()
        ):
            raise PermissionDenied(
                _('Only post authors can edit or delete posts')
            )


@api_view(['POST'])
def react_to_post(request):
    post_id = request.data.get('id')
    reaction = request.data.get('reaction')

    if not id or reaction not in REACTION_STATUSES.values():
        return Response({
            'errors': 'Please provide an id and a valid reaction value'
            f'(one of {", ".join(REACTION_STATUSES.values())}).'
        }, status=status.HTTP_400_BAD_REQUEST)

    post = get_object_or_404(Post, pk=post_id)
    process_reaction(post, reaction, request.user)

    return Response()
