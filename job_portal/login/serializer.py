from django.conf import settings
from rest_framework import serializers
from .models import ChatMessage, UserProfile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'bio', 'profile_picture', 'skill']


        
from rest_framework import serializers
from .models import ChatMessage

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)
    sender_profile = serializers.SerializerMethodField()
    receiver_profile = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'sender_username', 'receiver_username', 
                 'message', 'is_read', 'date', 'sender_profile', 'receiver_profile']
        read_only_fields = ['sender', 'date', 'is_read']

    def get_sender_profile(self, obj):
        if hasattr(obj.sender, 'user_profile'):
            return {
                'profile_picture': obj.sender.user_profile.profile_picture.url if obj.sender.user_profile.profile_picture else None
            }
        return None

    def get_receiver_profile(self, obj):
        if hasattr(obj.receiver, 'user_profile'):
            return {
                'profile_picture': obj.receiver.user_profile.profile_picture.url if obj.receiver.user_profile.profile_picture else None
            }
        return None

    def create(self, validated_data):
        # Ensure sender is set from the authenticated user
        sender = self.context['request'].user
        validated_data['sender'] = sender
        return super().create(validated_data)



