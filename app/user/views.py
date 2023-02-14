"""
views for user api
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user import serializers

class CreateUserView(generics.CreateAPIView): #create api view handles post requests for creating objects in the db
    """"Create a new user in the system"""
    serializer_class = serializers.UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage autheticated user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrieve and return the autheticated user"""
        return self.request.user


class CreateAuthToken(ObtainAuthToken):
    """create a new auth token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
