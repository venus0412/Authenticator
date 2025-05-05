from django.urls import path, include
from .views import register_user, user_profile, get_room_by_room_id

urlpatterns = [
    path('register/', register_user, name='register'),
    path('profile/', user_profile, name='profile'),
    path('api/room/<uuid:room_id>/', get_room_by_room_id),
]