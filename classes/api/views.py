from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from knox.auth import TokenAuthentication

from years.models import Year
from .serializers import CreateClassSerializer, GetClassSerializer
from ..models import Class


@api_view(http_method_names=['POST'])
@permission_classes([IsAdminUser, IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_class(request, year_id):
    try:
        year = Year.objects.get(pk=year_id)
    except Year.DoesNotExist:
        msg = "Year not found. You can't assign a class to an unknown year."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not year.is_active:
        msg = "You can't assign a class to an inactive year."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    serializer = CreateClassSerializer(data=request.data)

    if serializer.is_valid():
        name = serializer.validated_data['name']
        if Class.objects.filter(name=name, year=year).exists():
            msg = f'{name} already exists for the year {year.name}.'
            return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            created_class = serializer.save(year=year)
            response_serializer = GetClassSerializer(created_class)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes([IsAdminUser, IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_class(request, class_id):
    try:
        _class = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = "Class not found."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)
    serializer = GetClassSerializer(_class)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
@permission_classes([IsAdminUser, IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_classes(request):
    try:
        current_year = Year.objects.get(is_active=True)
    except Year.DoesNotExist:
        msg = 'No current active year.'
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    classes = Class.objects.all()
    response_data = {'current_year': current_year.name, 'classes': []}
    for c in classes:
        students = c.student_set.all()
        boys = students.filter(gender='Male').count()
        girls = students.filter(gender='Female').count()
        data = {
            'id': c.pk,
            'name': c.name,
            'boys': boys,
            'girls': girls,
            'total': students.count()
        }
        response_data['classes'].append(data)
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['DELETE'])
@permission_classes([IsAdminUser, IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_class(request, class_id):
    try:
        _class = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = "Class not found."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not _class.year.is_active:
        msg = "You can't delete a class for an inactive year."
        return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    _class.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['PUT'])
@permission_classes([IsAdminUser, IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_class(request, class_id, new_year_id):
    try:
        _class = Class.objects.get(pk=class_id)
    except Class.DoesNotExist:
        msg = "Class not found."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    try:
        new_year = Year.objects.get(pk=new_year_id)
    except Year.DoesNotExist:
        msg = "Year not found. You can't assign a class to an unknown year."
        return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)

    if not new_year.is_active:
        msg = f"You can't update a class for an inactive year."
        return Response({'error': msg}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CreateClassSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        theme = serializer.validated_data.get('theme')
        if Class.objects.filter(name=name, year=new_year, theme=theme).exists():
            msg = f'{name} already exists for the year {new_year.name}.'
            return Response({'error': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            _class.name = name
            _class.year = new_year
            if theme:
                _class.theme = theme
            _class.save()
            response_serializer = GetClassSerializer(_class)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
