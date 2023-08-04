from rest_framework import generics, permissions, status
from api_quizz.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.generic import View

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    """
    POST api/v1/login/
    """
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        if not email or not password:
            return Response(data={"message": "Both email and password are required to connect"}, status=400)
        else:
            try:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    # Redirect to a success page.
                    serializer = TokenSerializer(
                        data={"token": jwt_encode_handler(jwt_payload_handler(user))})
                    if serializer.is_valid():
                        token = serializer.data
                        response_data = {
                            'id': user.id,
                            'token': token,
                            'firstName': user.firstName,
                            'lastName': user.lastName,
                            'email': user.email,
                        }
                        return Response(response_data)
                else:
                    return Response(data={"message": "Votre email ou mot de passe est incorrect"}, status=401)
            except User.DoesNotExist:
                return Response(data={"message": "Votre email n'existe pas"}, status=401)


class LogoutView(generics.CreateAPIView):
    def get(self, request):
        logout(request)
        return Response(data={"deconnected": "success"}, status=200)
