from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets

from core import models


class SuplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Suplier
        fields = ['id', 'title']

class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bonus
        fields = ('id', 'two_word_desc', 'bonus_desc', 'suplier')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']



class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=100)


class FilterSerializer(serializers.Serializer):
    # Choices
    sorting = serializers.ChoiceField(default='dep_min_to_max', choices=models.Bonus._FILTER_LIST['sorting'])
    suplier_type = serializers.ChoiceField(default='all', choices=models.Bonus._FILTER_LIST['type'])

    # Checkboxes
    nodep = serializers.BooleanField(default=False)
    ca_license_bool = serializers.BooleanField(default=False)

    # Range sliders
    wager_range_start = serializers.IntegerField(required=False, default=0)
    wager_range_end = serializers.IntegerField(required=False, default=200)

    bonus_range_start = serializers.IntegerField(required=False, default=0)
    bonus_range_end = serializers.IntegerField(required=False, default=100000)

    deposit_range_start = serializers.IntegerField(required=False, default=0)
    deposit_range_end = serializers.IntegerField(required=False, default=100000)

    def save(self):

        self.validated_data['wager-js-range-slider'] = f"{self.validated_data['wager_range_start']};{self.validated_data['wager_range_end']}"
        del self.validated_data['wager_range_start']
        del self.validated_data['wager_range_end']
        
        self.validated_data['bonus-js-range-slider'] = f"{self.validated_data['bonus_range_start']};{self.validated_data['bonus_range_end']}"
        del self.validated_data['bonus_range_start']
        del self.validated_data['bonus_range_end']

        self.validated_data['deposit-js-range-slider'] = f"{self.validated_data['deposit_range_start']};{self.validated_data['deposit_range_end']}"
        del self.validated_data['deposit_range_start']
        del self.validated_data['deposit_range_end']

        # make 'type' attribute readable for filtering
        self.validated_data['type'] = self.validated_data['suplier_type']
        del self.validated_data['suplier_type']

        return dict(self.validated_data)