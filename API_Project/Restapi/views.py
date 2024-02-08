from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from datetime import datetime, timedelta

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Authentication successful, generate tokens
        payload = {
            'username': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=1) 
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        token_ = f'Bearer {token}'
        refresh_payload = {
            'username': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=4)  
        }
        refresh_token = jwt.encode(refresh_payload, 'secret', algorithm='HS256')

        return Response({
            'token': token_,
            'refresh_token': refresh_token
        })
        
      
class TokenRefreshAPIView(APIView):
    def post(self, request):
        expired_token = request.data.get('expired_token')
        refresh_token = request.data.get('refresh_token')

        try:
            decoded_refresh_token = jwt.decode(refresh_token, 'secret', algorithms=['HS256'])
            username = decoded_refresh_token['username']
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


        new_payload = {
            'username': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=1)  # Set the expiration time for the new access token
        }
        new_token = jwt.encode(new_payload, 'secret', algorithm='HS256').decode('utf-8')
        new_token_ = f'Bearer {new_token}'


        new_refresh_payload = {
            'username': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=4)  # Set the expiration time for the new refresh token
        }
        new_refresh_token = jwt.encode(new_refresh_payload, 'secret', algorithm='HS256')

        return Response({
            'token': new_token_,
            'refresh_token': new_refresh_token
        })
