from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from rest_framework import status

class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer 

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)  

        if serializer.is_valid():
            user = serializer.save()  


            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)


            return Response({
                'data': serializer.data,
                'message': f'Hi {user.first_name}',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request):    
        print("Request Data:", request.data)  # Log request data
        email = request.data.get('email')
        password = request.data.get('password')
        print("Email:", email, "Password:", password)

        
        # Authenticate the user
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            # Generate JWT token for authenticated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': f'Hi {user.first_name}'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'detail': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)
