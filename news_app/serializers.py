from rest_framework import serializers
from django.contrib.auth.models import User
from .models import News

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'content', 'author', 'author_name', 'date_created', 'date_updated']
        read_only_fields = ['author', 'date_created', 'date_updated']
        
    def validate_content(self, value):
        if len(value) < 50:
            raise serializers.ValidationError("Минимум 50 символов.")
        return value
