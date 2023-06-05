from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from terms.models import Term
from .serializers import CreateSequenceSerializer, GetSequenceSerializer
from ..models import Sequence


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_sequence(request, term_id):

    if Sequence.objects.filter(is_active=True).exists():
        msg = "You can not create a new sequence while another is active."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = "Term not found."
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)

    if not term.is_active:
        msg = "You can not create a new sequence while another is active."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not term.year.is_active:
        msg = "You can not create a new sequence the current active year."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    serializer = CreateSequenceSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data.get('name')
        sequence = serializer.save(term=term)
        response_serializer = GetSequenceSerializer(sequence)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_sequence(request, sequence_id):
    try:
        sequence = Sequence.objects.get(pk=sequence_id)
    except Sequence.DoesNotExist:
        msg = f'Sequence not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetSequenceSerializer(sequence)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_sequences(request):
    sequences = Sequence.objects.all()
    serializer = GetSequenceSerializer(sequences, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_sequences_term(request, term_id):
    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = "Term not found."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    sequences = term.sequence_set.all()
    serializer = GetSequenceSerializer(sequences, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_sequence(request, sequence_id):
    try:
        sequence = Sequence.objects.get(pk=sequence_id)
    except Sequence.DoesNotExist:
        msg = f'Sequence not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not sequence.is_active:
        msg = "You can only delete active sequences."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not sequence.term.year.is_active:
        msg = "You can only delete sequences in the current active year."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    sequence.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_sequence(request, term_id):
    try:
        sequence = Sequence.objects.get(is_active=True)
    except Sequence.DoesNotExist:
        msg = 'Sequence not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        term = Term.objects.get(pk=term_id)
    except Term.DoesNotExist:
        msg = "Term not found."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not term.is_active:
        msg = "You can not update a sequence in an inactive term."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not term.year.is_active:
        msg = "You can not update a sequence in an inactive year."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    serializer = CreateSequenceSerializer(sequence, data=request.data)
    if serializer.is_valid():
        updated_sequence = serializer.save(term=term)
        return Response(GetSequenceSerializer(updated_sequence).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def deactivate_sequence(request):

    try:
        sequence = Sequence.objects.get(is_active=True)
    except Sequence.DoesNotExist:
        msg = 'Sequence not found'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not sequence.is_active:
        msg = 'You can only deactivate an active sequence.'
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not sequence.term.is_active:
        msg = 'You can only deactivate a sequence in an active term.'
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not sequence.term.year.is_active:
        msg = 'You can only deactivate a sequence in an active year.'
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    sequence.is_active = False
    sequence.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
