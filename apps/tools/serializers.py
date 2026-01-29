from rest_framework import serializers
from rest_framework.fields import JSONField

from apps.tools.models import City, District


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = "__all__"


class CreateCityWithDistrictSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    districts = JSONField()


class UpdateCityWithDistrictSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    del_districts = JSONField(required=False)
    new_districts = JSONField(required=False)


class ActiveCityAndDistrictsSerializer(serializers.ModelSerializer):
    districts = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = '__all__'

    def get_districts(self, obj):
        active_districts = obj.city.filter()
        return DistrictSerializer(active_districts, many=True).data


class NotActiveCityAndDistrictsSerializer(serializers.ModelSerializer):
    districts = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = '__all__'

    def get_districts(self, obj):
        active_districts = obj.city.filter()
        return DistrictSerializer(active_districts, many=True).data