"""Views for recipe api"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe apis"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    #the modelviewset provides .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy() methods
    #if we use it as it is, it will let us manage all the recipes in the system. to avoid this, we override the
    #get_queryset method
    def get_queryset(self):
        """retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self): #we override this function when we want to use different serializer classes based on the action
        """Return serializer class for the request"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

class TagViewSet(mixins.UpdateModelMixin, 
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin, 
                 viewsets.GenericViewSet):
    """View to manage tags api"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    