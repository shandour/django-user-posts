import clearbit
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status, generics
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import HTTPError

from .serializers import UserSerializer, RegistrationSerializer
from .utils import process_clearbit_response


User = get_user_model()


class Register(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request):
        print(request.data)
        return super().post(request)


class ManipulateUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if (
            request.method != 'GET'
            and not request.user == obj
        ):
            raise PermissionDenied(
                _('Only owners can edit or delete their account.')
            )


@api_view(['GET'])
def get_info(request):
    domain = request.query_params.get('domain')
    email = request.query_params.get('email')
    company = request.query_params.get('company')

    if not email and not domain:
        return Response(
            {'errors': 'Please specify email or domain.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    clearbit_class = clearbit.Enrichment
    if company:
        clearbit_class = clearbit.Company

    try:
        if email:
            resp = clearbit_class.find(email=email, stream=True)
        elif domain:
            resp = clearbit_class.find(domain=domain, stream=True)
    except HTTPError:
        return Response(
            {'errors': 'Error while processing your request.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        process_clearbit_response(resp),
        status=status.HTTP_200_OK,
    )
