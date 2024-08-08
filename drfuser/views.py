from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed, ValidationError
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoginView(APIView): # installed PyJWT package
    def post(self,request):
        email = self.request.data["email"]
        password = self.request.data["password"]

        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed("User not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            "id":user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1), # datetime.utcnow() is a class method returns the current datetime 
                                                                                # whereas datetime.timedelta(minutes=60) creates a duration of 60 minutes
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm="HS256") # encodes the payload into jsonwebtoken using secret key and algorithm

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
                # httponly to true enhance security by preventing client side scripts from accessing the cookie

        response.data={
            "jwt": token
        }

        return response 
    

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("User not found")

        try:
            payload = jwt.decode(token,'secret', algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return response