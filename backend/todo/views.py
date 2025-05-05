from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, RoomSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import Room
from rest_framework import viewsets

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user to the database
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_room_by_room_id(request, room_id):
    try:
        room = Room.objects.get(room_id=room_id)
        serializer = RoomSerializer(room)
        data = serializer.data

        # Add room full check
        data['is_full'] = room.guest_count >= room.max_guests  # Adjust if needed

        return Response(data)
    except Room.DoesNotExist:
        return Response({'detail': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer