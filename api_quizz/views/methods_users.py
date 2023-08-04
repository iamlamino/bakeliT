from django.contrib.auth import logout
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, login
from api_quizz.serializers import *
from rest_framework import generics,  status
from api_quizz.serializers import *
from rest_framework.response import Response
from ..models import User
# list user


class UserAPIView(generics.CreateAPIView):
    """
    GET api/v1/users/
    POST api/v1/users/
    """
    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.all().order_by('-date_joined')
        if not user:
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, many=True)

        return Response({
            "status": "success",
            "message": "user successfully retrieved.",
            "count": user.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        # user = request.data
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
