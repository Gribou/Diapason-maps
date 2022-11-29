from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# login and logout API views are used for tiles module that allow for data update via API


class StandaloneLoginView(APIView):
    """
    Authentification de l'utilisateur. Fournit les cookies 'csrftoken' et 'sessionid' à utiliser pour les requêtes ultérieures

    Utile pour le accès pour mise à jour automatique (ex : files)
    """

    def post(self, request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None or password is None:
            return Response(
                {
                    'non_field_errors':
                    'Veuillez indiquer nom d\'utilisateur et mot de passe.'
                },
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'non_field_errors': 'Mot de passe invalide.'},
                            status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({'detail': 'Authentifié avec succès.'})


class LogoutView(APIView):
    """
    Déconnexion de l'utilisateur : invalidation des cookies de session
    """

    def post(self, request, format=None):
        logout(request)
