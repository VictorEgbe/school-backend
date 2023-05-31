from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
