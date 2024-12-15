from rest_framework import serializers
# from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email

        return token
    
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        # Check if the passwords match
        if password != password2:
            raise serializers.ValidationError("Passwords don't match")
        
        # Return the validated data
        return attrs

    def create(self, validated_data):
        # Remove password2 since it's not saved
        validated_data.pop('password2', None)

        # Ensure that 'first_name' and other required fields are in validated_data
        if 'first_name' not in validated_data:
            raise serializers.ValidationError("First name is required")
        
        if 'last_name' not in validated_data:
            raise serializers.ValidationError("Last name is required")

        # Create the user and hash the password automatically using create_user
        user = User.objects.create_user(
            email=validated_data['email'], 
            username=validated_data['username'], 
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Check if email and password are provided
        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = User.objects.filter(email=email).first()
        print(user)

        # Check if the user exists
        if not user:
            raise serializers.ValidationError("User does not exist")

        # Check if the password is correct
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        attrs['user'] = user
        return attrs
