from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from core import models
from api import serializers

# REST API Views

class SearchView(APIView):
    def get(self, request, *args, **kwars):
        queryset = models.Bonus.objects.all()
        serializer = serializers.BonusSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.SearchSerializer(data=request.data)
    
        if serializer.is_valid():
    
            search_query = serializer.validated_data.get('search')
            bonuses = models.Bonus.get_searched_bonuses(search_query)
            serialized_bonuses = serializers.BonusSerializer(bonuses, many=True)
            
            return Response(serialized_bonuses.data)

        return Response(serializer.errors)

class FilterView(APIView): 
    def get(self, request, *args, **kwars):
        queryset = models.Bonus.objects.all()
        serializer = serializers.BonusSerializer(queryset, many=True)
    
        return Response(serializer.data)
        # TODO Rewrite get() methods for both classes. Response should be like ...
        # TODO      .... {'message':'It supports only POST method. Send your search query by POST. e.g. 'search':'TTR Casino'}

    def post(self, request, *args, **kwargs):
        serializer = serializers.FilterSerializer(data=request.data)
        if serializer.is_valid():
    
            filtering_feed = serializer.save()            
            bonuses = models.Bonus.filtering(filtering_feed)
            serialized_bonuses = serializers.BonusSerializer(bonuses, many=True)

            return Response(serialized_bonuses.data)

        return Response(serializer.errors)



class BonusViewSet(viewsets.ModelViewSet):
    queryset = models.Bonus.objects.all()
    serializer_class = serializers.BonusSerializer

class SuplierViewSet(viewsets.ModelViewSet):
    queryset = models.Suplier.objects.all()
    serializer_class = serializers.SuplierSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
