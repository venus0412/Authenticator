from rest_framework import serializers
from .models import CustomUser
import re
from .models import Room

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)


    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'password']
    
    #username is required
    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError("Username is required.")
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_password(self, value):
        if len(value) < 12:
            raise serializers.ValidationError("Password must be at least 12 characters long.")
        if not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def create(self, validated_data):
        user = CustomUser(
            first_name = validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # hashes password
        user.save()
        return user
    

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
