from rest_framework.generics import CreateAPIView
from authentication.serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class RegisterView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        Two arguments:
        username & password
        """
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        if username == "" or password == "":
            return Response({
                    'status': 'Incorrect',
                    'message': 'Utilisateur et Mot de passe obligatoire'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:

            account = authenticate(username=username, password=password)
            if account is not None:
                if account.is_active:
                    serializer = LoginSerializer(account)
                    return Response({
                        'status': 'OK',
                        'message': 'Authentification correct'
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'Incorrect',
                        'message': 'Utilisateur invalide'
                        }, status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({
                    'status': 'Incorrect',
                    'message': 'Utilisateur ou Mot de passe invalide'
                    }, status=status.HTTP_401_UNAUTHORIZED)
