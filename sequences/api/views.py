from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from classes.models import Class
from years.models import Year
from .serializers import CreateSequenceSerializer, GetSequenceSerializer
from ..models import Sequence


@api_view(http_method_names=['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_sequence(request):

    if Sequence.objects.filter(is_active=True).exists():
        msg = "You can not create an new sequence while another is active."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    active_year = Year.objects.get(is_active=True)
    active_classes = active_year.class_set.all()

    if active_classes.count() < 1:
        msg = f"There are no classes for the current active year. Please create classes first."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        serializer = CreateSequenceSerializer(data=request.data)
        if serializer.is_valid():

            name = serializer.validated_data['name']

            if Sequence.objects.filter(name=name, sequence_class__year__is_active=True, is_active=True).exists():
                msg = f"{name} for all forms created already."
                return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

            for sequence_class in active_classes:
                Sequence.objects.create(
                    name=name, sequence_class=sequence_class)

            sequences = Sequence.objects.filter(
                sequence_class__year__is_active=True)
            response_serializer = GetSequenceSerializer(sequences, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        else:
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


@api_view(http_method_names=['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_sequence(request):

    sequences = Sequence.objects.filter(is_active=True)

    if sequences.count() < 1:
        msg = f'Sequence not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    for sequence in sequences:

        if not sequence.sequence_class.year.is_active:
            msg = f"You can not delete a sequence in an active year."
            return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            if not sequence.is_active:
                msg = 'You can not delete an inactive sequence.'
                return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

            sequence.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_sequence(request):

    sequences = Sequence.objects.filter(is_active=True)

    if sequences.count() < 1:
        msg = f'Sequence not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    serializer = CreateSequenceSerializer(data=request.data)

    if serializer.is_valid():

        name = serializer.validated_data.get('name')

        if Sequence.objects.filter(name=name, sequence_class__year__is_active=True).exists():
            msg = f"{name} already exists."
            return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            for sequence in sequences:
                sequence.name = name
                sequence.save()

        sequences = Sequence.objects.all()
        response_serializer = GetSequenceSerializer(sequences, many=True)

        return Response(response_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def deactivate_sequence(request):

    sequences = Sequence.objects.filter(is_active=True)

    if sequences.count() < 1:
        msg = f'Sequence not found.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    for sequence in sequences:

        if not sequence.sequence_class.year.is_active:
            msg = f"You can only deactivate a sequence in an active year."
            return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:

            if not sequence.is_active:
                msg = 'You can only deactivate an active sequence.'
                return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

            sequence.is_active = False
            sequence.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
