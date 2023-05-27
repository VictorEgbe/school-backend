from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from knox.auth import TokenAuthentication

from years.models import Year
from ..models import Term
from .serializers import (
    CreateTermSerializer,
    GetTermSerializer,
    UpdateTermSerializer
)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def create_term(request, year_id):
    try:
        year = Year.objects.get(pk=year_id)
    except Year.DoesNotExist:
        msg = "Year not found. You can't assign a term to an unknown year."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = CreateTermSerializer(data=request.data)
    if serializer.is_valid():
        term = serializer.save(year=year)
        return Response(term.get_response_data(), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def get_term(request, term_id):
    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = "Term not found."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)
    serializer = GetTermSerializer(term)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def get_terms(request):
    terms = Term.objects.all()
    serializer = GetTermSerializer(terms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def update_term(request, term_id, year_id):
    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = "Term not found. You can't update an unknown term."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        year = Year.objects.get(pk=year_id)
    except Year.DoesNotExist:
        msg = "Year not found. You can't assign a term to an unknown year."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateTermSerializer(data=request.data)

    if serializer.is_valid():
        name = serializer.validated_data['name']
        if Term.objects.filter(name=name, year=year).exists():
            msg = f'{name} already exists for the year {year.name}'
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
        else:
            term.name = name
            term.year = year
            term.save()
            return Response(term.get_response_data(), status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def delete_term(request, term_id):
    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = "Term not found."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    term.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def deactivate_term(request, term_id):
    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = "Term not found."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    term.is_active = False
    term.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
