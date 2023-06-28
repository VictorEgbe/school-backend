from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from knox.auth import TokenAuthentication


@api_view(http_method_names=('GET',))
@permission_classes((IsAuthenticated, IsAdminUser))
@authentication_classes((TokenAuthentication, ))
def dashboard(request):
    pass
