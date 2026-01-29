from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tools.models import City, District
from apps.tools.serializers import CreateCityWithDistrictSerializer, UpdateCityWithDistrictSerializer, \
    ActiveCityAndDistrictsSerializer, CitySerializer, NotActiveCityAndDistrictsSerializer, DistrictSerializer


class CreateCityWithDistrictsAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = CreateCityWithDistrictSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        name = serializer.data['name']
        districts = serializer.data['districts']

        city = City.objects.create(name=name)
        for district in districts:
            District.objects.create(city=city, name=district)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateCityWithDistrictAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, city_id):
        serializer = UpdateCityWithDistrictSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        city = City.objects.get(id=city_id)

        if "del_districts" in serializer.data:
            del_districts = serializer.data['del_districts']

            for del_district in del_districts:
                district = District.objects.get(id=del_district).delete()

        if "new_districts" in serializer.data:
            new_districts = serializer.data['new_districts']

            for new_district in new_districts:
                District.objects.create(name=new_district, city=city)

        if "name" in serializer.data and serializer.data['name'] != city.name:
            name = serializer.data['name']

            city.category_title = name
            city.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActiveCitiesAndDistrictsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        active_cities = City.objects.filter(is_active=True)
        serializer = ActiveCityAndDistrictsSerializer(active_cities, many=True)
        return Response(serializer.data)


class CityUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        city = City.objects.get(pk=pk)
        serializer = CitySerializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotActiveCitiesAndDistrictsAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        not_active_cities = City.objects.filter(is_active=False)
        serializer = NotActiveCityAndDistrictsSerializer(not_active_cities, many=True)
        return Response(serializer.data)


class DistrictUpdateAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        serializer = DistrictSerializer(district, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityDeleteAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DistrictDeleteAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        district.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
