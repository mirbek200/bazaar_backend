from django.db.models import Q, Count
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.announcement.logic import save_images, delete_images, send_message
from apps.announcement.models import (
    Announcement, BannedAnnouncement,
)
from apps.announcement.permissions import IsAdminAndModerator
from apps.announcement.serializer_mappings import serializer_classes, model_mapping, serializer_list_detail_classes
from apps.announcement.serializers import (
    AnnouncementSerializer,
    CreateRequestAnnouncementSerializer,
    AnnouncementListSerializer, AnnouncementUpdateSerializer, AnnouncementDetailSerializer,
    BannedAnnouncementSerializer,
)
from thailand_bazar.logic.send_email import submitted_for_review, ad_published, banned_announcement as send_banned_announcement


class AnnouncementCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')

        category_serializers = serializer_classes.get(category_type, {})
        serializer_class = category_serializers.get(sub_category_type, AnnouncementSerializer)

        return serializer_class

    @swagger_auto_schema(
        operation_description="Create an announcement.",
        request_body=CreateRequestAnnouncementSerializer,
        manual_parameters=[
            openapi.Parameter('category_type', openapi.IN_QUERY, description="Category type", type=openapi.TYPE_STRING),
            openapi.Parameter('transport_type', openapi.IN_QUERY, description="Transport type",
                              type=openapi.TYPE_STRING),
        ],
        responses={201: "Announcement created", 400: "Bad Request"},
    )
    def post(self, request):
        user = request.user
        try:
            announcement_data = request.data
            announcement_data["user"] = user.id
            images_data = request.FILES.getlist('images')

            if len(images_data) > 10:
                return Response(
                    {'error': 'количество картинок больше 10'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=announcement_data)

            if serializer.is_valid():
                announcement_instance = serializer.save()
                save_images(images_data=images_data, announcement_instance=announcement_instance)

                if serializer.validated_data['is_active']:
                    ad_published(announcement_instance.user.email, announcement_instance.id)
                    return Response({
                        "success": "Объявление создано"
                    }, status=status.HTTP_201_CREATED)
                else:
                    submitted_for_review(user.email, announcement_instance.id)
                    return Response({
                        "error": "Объявление создано, но отмечено как неактивное"
                    }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AnnouncementDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
                `DELETE REQUEST` - Удалить объявление.
                id_announcement - ID объявления.
                Для выполнения операции требуется авторизация и только автор может удалить объявление.
            """,
        responses={204: "No content"},
    )
    def delete(self, request, id_announcement, *args, **kwargs):
        user = request.user
        if user.is_moderator:
            announcement = get_object_or_404(Announcement, id=id_announcement)
            if announcement.user != user:
                send_message(announcement.user, "test")
        else:
            announcement = get_object_or_404(Announcement, id=id_announcement, user=user.id)
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnouncementUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')

        category_serializers = serializer_classes.get(category_type, {})
        serializer_class = category_serializers.get(sub_category_type, AnnouncementUpdateSerializer)

        return serializer_class

    def get_model_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')
        model_class = model_mapping.get(category_type, {}).get(sub_category_type, Announcement)
        return model_class

    def handle_images(self, request, announcement):
        if 'new_images' in request.data:
            new_images_data = request.FILES.getlist('new_images', [])
            if new_images_data:
                save_images(new_images_data, announcement)
        if 'delete_images' in request.data:
            delete_images_data = request.data.getlist('delete_images', [])
            if delete_images_data:
                delete_images(delete_images_data)

    def process_request(self, request, id_announcement, partial):
        user = request.user
        announcement = get_object_or_404(Announcement, id=id_announcement)
        if user.is_moderator or announcement.user.id == user.id:
            is_banned_announcement = announcement.is_banned

            serializer_class = self.get_serializer_class()
            model_class = self.get_model_class()

            announcement_serializer = serializer_class(model_class.objects.get(pk=id_announcement), data=request.data,
                                                       partial=partial)

            announcement_serializer.is_valid(raise_exception=True)
            announcement_serializer.save()

            announcement_instance = model_class.objects.get(pk=id_announcement)

            if is_banned_announcement == True and announcement_instance.is_banned == False:
                ad_published(announcement.user.email, announcement.id)
            if is_banned_announcement == False and announcement_instance.is_banned == True:
                send_banned_announcement(announcement.user.email, announcement.id)

            self.handle_images(request, announcement)

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        operation_description="""
                        `PUT/PATCH REQUEST` - Обновить/частично обновить объявление.
                        id_announcement - ID объявления.
                        Для выполнения операции требуется авторизация и только автор может обновить объявление.
                    """,
        responses={200: "Updated data"},
    )
    def put(self, request, id_announcement, *args, **kwargs):
        return self.process_request(request, id_announcement, partial=False)

    @swagger_auto_schema(
        operation_description="""
                        `PATCH REQUEST` - Частичное обновление объявления.
                        id_announcement - ID объявления.
                        Для выполнения операции требуется авторизация и только автор может частично обновить объявление.
                    """,
        responses={200: "Partially updated data"},
    )
    def patch(self, request, id_announcement, *args, **kwargs):
        return self.process_request(request, id_announcement, partial=True)


class AnnouncementListAPIView(APIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')

        category_serializers = serializer_list_detail_classes.get(category_type, {})
        serializer_class = category_serializers.get(sub_category_type, AnnouncementListSerializer)

        return serializer_class

    def get_model_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')
        model_class = model_mapping.get(category_type, {}).get(sub_category_type, Announcement)
        return model_class

    def count_category(self, queryset):
        return queryset.values('category__id').annotate(count=Count('id'))

    def count_sub_category(self, queryset):
        return queryset.values('sub_category__id').annotate(count=Count('id'))

    def count_district(self, queryset):
        return queryset.values('district__id').annotate(count=Count('id'))

    def count_city(self, queryset):
        return queryset.values('city__id').annotate(count=Count('id'))

    def count_under_sub_category(self, queryset):
        return queryset.values('under_sub_category__id').annotate(count=Count('id'))

    def get_queryset(self):
        model_class = self.get_model_class()
        return model_class.objects.filter(is_active=True, is_banned=False)

    @swagger_auto_schema(
        responses={200: openapi.Response('List of announcements', AnnouncementListSerializer(many=True))},
        operation_summary="Retrieve a list of announcements",
        operation_description="This endpoint retrieves a paginated list with filter and search of announcements."
    )
    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()

        announcements = self.get_queryset()

        category_id = request.query_params.get('category')
        sub_category_id = request.query_params.get('sub_category')
        under_sub_category_id = request.query_params.get('under_sub_category')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        district_id = request.query_params.get('district')
        city_id = request.query_params.get('city')
        search = request.query_params.get('search')

        engine_capacity = request.query_params.get('engine_capacity')
        rental_type = request.query_params.get('rental_type')
        vehicle_type = request.query_params.get('vehicle_type')
        service_type = request.query_params.get('service_type')
        drive = request.query_params.get('drive')
        type_housing = request.query_params.get('type_housing')
        type_electronic = request.query_params.get('type_electronic')
        type_of_cloth = request.query_params.get('type_of_cloth')
        type_of_shoes = request.query_params.get('type_of_shoes')
        type_of_accessories = request.query_params.get('type_of_accessories')
        number_of_rooms = request.query_params.get('number_of_rooms')
        rules = request.query_params.get('rules')
        gender = request.query_params.get('gender')
        size = request.query_params.get('size')
        brand = request.query_params.get('brand')
        state = request.query_params.get('state')
        manufacturer = request.query_params.get('manufacturer')
        schedule = request.query_params.get('schedule')
        payment = request.query_params.get('payment')

        deposit = request.query_params.get('deposit')
        delivery = request.query_params.get('delivery')
        color = request.query_params.get('color')
        swimming_pool = request.query_params.get('swimming_pool')
        availability_of_loaders = request.query_params.get('availability_of_loaders')
        child_seat = request.query_params.get('child_seat')
        phone_charger = request.query_params.get('phone_charger')
        audio_system = request.query_params.get('audio_system')
        phone_mount = request.query_params.get('phone_mount')
        meeting_with_sign = request.query_params.get('meeting_with_sign')

        min_wage = request.query_params.get('min_wage')
        max_wage = request.query_params.get('max_wage')

        if category_id:
            announcements = announcements.filter(category_id=category_id)
        if sub_category_id:
            announcements = announcements.filter(sub_category_id=sub_category_id)
        if under_sub_category_id:
            announcements = announcements.filter(under_sub_category_id=under_sub_category_id)
        if min_price:
            announcements = announcements.filter(price__gte=min_price)
        if max_price:
            announcements = announcements.filter(price__lte=max_price)
        if district_id:
            district_id = [int(i) for i in district_id.split(',')]
            announcements = announcements.filter(district_id__in=district_id)
        if city_id:
            announcements = announcements.filter(city_id=city_id)
        if color:
            announcements = announcements.filter(color=color)

        if search:
            announcements = announcements.filter(Q(title__icontains=search) | Q(description__icontains=search))

        if engine_capacity:
            engine_capacity = [int(i) for i in engine_capacity.split(',')]
            announcements = announcements.filter(engine_capacity__in=engine_capacity)

        if rental_type:
            rental_type = [i for i in rental_type.split(',')]
            announcements = announcements.filter(rental_type__in=rental_type)

        if vehicle_type:
            vehicle_type = [i for i in vehicle_type.split(',')]
            announcements = announcements.filter(vehicle_type__in=vehicle_type)

        if service_type:
            service_type = [i for i in service_type.split(',')]
            announcements = announcements.filter(service_type__in=service_type)

        if drive:
            drive = [i for i in drive.split(',')]
            announcements = announcements.filter(drive__in=drive)

        if type_housing:
            type_housing = [i for i in type_housing.split(',')]
            announcements = announcements.filter(type_housing__in=type_housing)

        if type_electronic:
            announcements = announcements.filter(type_electronic=type_electronic)
        if type_of_cloth:
            announcements = announcements.filter(type_of_cloth=type_of_cloth)
        if type_of_shoes:
            announcements = announcements.filter(type_of_shoes=type_of_shoes)
        if type_of_accessories:
            announcements = announcements.filter(type_of_accessories=type_of_accessories)

        if number_of_rooms:
            number_of_rooms = [i for i in number_of_rooms.split(',')]
            announcements = announcements.filter(number_of_rooms__in=number_of_rooms)

        if gender:
            gender = [i for i in gender.split(',')]
            announcements = announcements.filter(gender__in=gender)

        if size:
            size = [i for i in size.split(',')]
            announcements = announcements.filter(size__in=size)

        if brand:
            brand = [i for i in brand.split(',')]
            announcements = announcements.filter(brand__in=brand)

        if state:
            state = [i for i in state.split(',')]
            announcements = announcements.filter(state__in=state)

        if manufacturer:
            manufacturer = [i for i in manufacturer.split(',')]
            announcements = announcements.filter(manufacturer__in=manufacturer)

        if schedule:
            schedule = [i for i in schedule.split(',')]
            announcements = announcements.filter(schedule__in=schedule)

        if payment:
            payment = [i for i in payment.split(',')]
            announcements = announcements.filter(payment__in=payment)

        if rules:
            rules = [i for i in rules.split(',')]
            announcements = announcements.filter(rules__in=rules)

        if deposit:
            if deposit.lower() == 'true':
                announcements = announcements.filter(deposit=True)
            elif deposit.lower() == 'false':
                announcements = announcements.filter(deposit=False)

        if delivery:
            if delivery.lower() == 'true':
                announcements = announcements.filter(delivery=True)
            elif delivery.lower() == 'false':
                announcements = announcements.filter(delivery=False)

        if swimming_pool:
            if swimming_pool.lower() == 'true':
                announcements = announcements.filter(swimming_pool=True)
            elif swimming_pool.lower() == 'false':
                announcements = announcements.filter(swimming_pool=False)

        if availability_of_loaders:
            if availability_of_loaders.lower() == 'true':
                announcements = announcements.filter(availability_of_loaders=True)
            elif availability_of_loaders.lower() == 'false':
                announcements = announcements.filter(availability_of_loaders=False)

        if child_seat:
            if child_seat.lower() == 'true':
                announcements = announcements.filter(child_seat=True)
            elif child_seat.lower() == 'false':
                announcements = announcements.filter(child_seat=False)

        if phone_charger:
            if phone_charger.lower() == 'true':
                announcements = announcements.filter(phone_charger=True)
            elif phone_charger.lower() == 'false':
                announcements = announcements.filter(phone_charger=False)

        if audio_system:
            if audio_system.lower() == 'true':
                announcements = announcements.filter(audio_system=True)
            elif audio_system.lower() == 'false':
                announcements = announcements.filter(audio_system=False)

        if phone_mount:
            if phone_mount.lower() == 'true':
                announcements = announcements.filter(phone_mount=True)
            elif phone_mount.lower() == 'false':
                announcements = announcements.filter(phone_mount=False)

        if meeting_with_sign:
            if meeting_with_sign.lower() == 'true':
                announcements = announcements.filter(meeting_with_sign=True)
            elif meeting_with_sign.lower() == 'false':
                announcements = announcements.filter(meeting_with_sign=False)

        if min_wage:
            announcements = announcements.filter(wage__gte=min_wage)
        if max_wage:
            announcements = announcements.filter(wage__lte=max_wage)

        category_counts = self.count_category(announcements)
        category_counts_dict = {item['category__id']: item['count'] for item in category_counts}

        sub_category_counts = self.count_sub_category(announcements)
        sub_category_counts_dict = {item['sub_category__id']: item['count'] for item in sub_category_counts}

        district_counts = self.count_district(announcements)
        district_counts_dict = {item['district__id']: item['count'] for item in district_counts}

        city_counts = self.count_city(announcements)
        city_counts_dict = {item['city__id']: item['count'] for item in city_counts}

        under_sub_category_counts = self.count_under_sub_category(announcements)
        under_sub_category_counts_dict = {item['under_sub_category__id']: item['count'] for item in
                                          under_sub_category_counts}

        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(announcements, request)

        announcements_serializer = serializer_class(result_page, many=True)

        response_data = {
            'total_pages': paginator.page.paginator.num_pages,
            'results': announcements_serializer.data,
            'count': len(announcements),
            'counts': {
                'all': len(announcements),
                'category': category_counts_dict,
                'sub_category': sub_category_counts_dict,
                'under_sub_category': under_sub_category_counts_dict,
                'district': district_counts_dict,
                'city': city_counts_dict,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AnnouncementNoActivListAPIView(APIView):
    permission_classes = [IsAdminAndModerator]

    def get_serializer_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')

        category_serializers = serializer_list_detail_classes.get(category_type, {})
        serializer_class = category_serializers.get(sub_category_type, AnnouncementListSerializer)

        return serializer_class

    def get_model_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')
        model_class = model_mapping.get(category_type, {}).get(sub_category_type, Announcement)
        return model_class

    def get_queryset(self):
        model_class = self.get_model_class()
        return model_class.objects.filter(is_banned=True)

    @swagger_auto_schema(
        responses={200: openapi.Response('List of announcements status no active', AnnouncementListSerializer(many=True))},
        operation_summary="Retrieve a list of announcements",
        operation_description="This endpoint retrieves a paginated list with filter and search of announcements."
    )
    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()

        announcements = self.get_queryset()

        category_id = request.query_params.get('category')
        sub_category_id = request.query_params.get('sub_category')
        under_sub_category_id = request.query_params.get('under_sub_category')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        district_id = request.query_params.get('district')
        city_id = request.query_params.get('city')
        search = request.query_params.get('search')

        if category_id:
            announcements = announcements.filter(category_id=category_id)
        if sub_category_id:
            announcements = announcements.filter(sub_category_id=sub_category_id)
        if under_sub_category_id:
            announcements = announcements.filter(under_sub_category_id=under_sub_category_id)
        if min_price:
            announcements = announcements.filter(price__gte=min_price)
        if max_price:
            announcements = announcements.filter(price__lte=max_price)
        if district_id:
            announcements = announcements.filter(district_id=district_id)
        if city_id:
            announcements = announcements.filter(city_id=city_id)

        if search:
            announcements = announcements.filter(Q(title__icontains=search) | Q(description__icontains=search))

        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(announcements, request)

        announcements_serializer = serializer_class(result_page, many=True)

        response_data = {
            'total_pages': paginator.page.paginator.num_pages,
            'results': announcements_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AnnouncementDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')

        category_serializers = serializer_list_detail_classes.get(category_type, {})
        serializer_class = category_serializers.get(sub_category_type, AnnouncementDetailSerializer)

        return serializer_class

    def get_model_class(self):
        category_type = self.request.query_params.get('category_type')
        sub_category_type = self.request.query_params.get('sub_category_type')
        model_class = model_mapping.get(category_type, {}).get(sub_category_type, Announcement)
        return model_class

    @swagger_auto_schema(
        responses={200: openapi.Response('List of announcements', AnnouncementDetailSerializer())},
        operation_summary="Retrieve a list of announcements",
        operation_description="Детальная информация об обьявлении"
    )
    def get(self, request, id_announcement, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        model_class = self.get_model_class()

        announcement = get_object_or_404(model_class, id=id_announcement)
        announcement_base = get_object_or_404(Announcement, id=id_announcement)
        specifications = {k: v for k, v in announcement.__dict__.items() if k not in announcement_base.__dict__}

        announcement.increment_views()

        announcement_serializer = serializer_class(announcement_base)
        announcement_data = announcement_serializer.data
        announcement_data["specifications"] = specifications

        return Response(announcement_data, status=status.HTTP_200_OK)


class AnnouncementSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        search = request.query_params.get('search')

        if search is not None:
            announcements = Announcement.objects.filter(is_active=True, is_banned=False, title__icontains=search)
            serializer = AnnouncementListSerializer(announcements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Search parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class BannedAnnouncementAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        announcement = get_object_or_404(Announcement, id=id)

        if announcement.is_active == False:
            return Response({"status": "уже забанен"}, status=status.HTTP_400_BAD_REQUEST)

        if user.id == announcement.user.id:
            data = request.data.copy()
            data["announcement"] = announcement.id  # Assign the announcement id, not the object
            serializer = BannedAnnouncementSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            announcement.is_active = False
            announcement.save()

            banned_announcement, created = BannedAnnouncement.objects.get_or_create(
                user_id=user.id,
                announcement_id=announcement.id,
                defaults={'cause': serializer.validated_data["cause"]}
            )

            send_banned_announcement(announcement.user.email, announcement.id)

            return Response(BannedAnnouncementSerializer(banned_announcement).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)


