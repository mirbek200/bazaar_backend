from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.announcement.permissions import IsAdminAndModerator
from apps.events.logic import save_images, send_message, delete_images
from apps.events.models import Event
from apps.events.permissions import IsOwnerOfEvent
from apps.events.serializers import CreateRequestEventSerializer, EventSerializer, EventUpdateSerializer, \
    EventListSerializer


class EventCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create an event with images.",
        request_body=CreateRequestEventSerializer,
        responses={201: "Event created with images", 400: "Bad Request"},
    )
    def post(self, request):    # noqa
        try:
            event_data = request.data
            event_data["user"] = request.user.id
            images_data = request.FILES.getlist('images')
            if len(images_data) > 10:
                return Response(
                    {'error': 'количество картинок больше 10'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                event_serializer = EventSerializer(data=event_data)
                if event_serializer.is_valid():
                    event_instance = event_serializer.save()
                    save_images(images_data=images_data, event_instance=event_instance)
                    if event_serializer.validated_data['is_active']:
                        return Response({
                            "success": "Объявление создано"
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            "error": "Афиша создано, но отмечено как неактивное"
                        }, status=status.HTTP_200_OK)

                return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EventDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
                `DELETE REQUEST` - Удалить объявление.
                id_event - ID объявления.
                Для выполнения операции требуется авторизация и только автор может удалить объявление.
            """,
        responses={204: "No content"},
    )
    def delete(self, request, id_event, *args, **kwargs):
        user = request.user
        if user.is_moderator:
            event = get_object_or_404(Event, id=id_event)
            if event.user != user:
                send_message(event.user, "test")
        else:
            event = get_object_or_404(Event, id=id_event, user=user.id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
                `PUT REQUEST` - Обновить афишу.
                id_event - ID афиша.
                Для выполнения операции требуется авторизация и только автор может обновить объявление.
            """,
        responses={200: "Updated data"},
    )
    def put(self, request, id_event, *args, **kwargs):
        user = request.user
        event = get_object_or_404(Event, id=id_event, user=user)
        serializer = EventUpdateSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_images_data = request.FILES.getlist('new_images', [])
        delete_images_data = request.data.getlist('delete_images', [])

        if new_images_data:
            save_images(new_images_data, event)

        if delete_images_data:
            delete_images(delete_images_data)

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="""
                `PATCH REQUEST` - Частичное обновление афишы.
                id_event - ID афишы.
                Для выполнения операции требуется авторизация и только автор может частично обновить объявление.
            """,
        responses={200: "Partially updated data"},
    )
    def patch(self, request, id_event, *args, **kwargs):
        user = request.user
        event = get_object_or_404(Event, id=id_event, user=user)
        serializer = EventUpdateSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        new_images_data = request.FILES.getlist('new_images', []) if "new_images" in request.FILES else []  # noqa
        delete_images_data = request.data.getlist('delete_images', []) if "delete_images" in request.data else []

        if new_images_data:
            save_images(new_images_data, event)

        if delete_images_data:
            delete_images(delete_images_data)

        return Response(status=status.HTTP_200_OK)


class EventListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Response('List of events', EventListSerializer(many=True))},
        operation_summary="Retrieve a list of events",
        operation_description="This endpoint retrieves a paginated list with filter and search of announcements."
    )
    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(is_active=True, is_banned=False, on_moderation=False)

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        district_id = request.query_params.get('district')
        city_id = request.query_params.get('city')
        search = request.query_params.get('search')

        if min_price:
            events = events.filter(price__gte=min_price)
        if max_price:
            events = events.filter(price__lte=max_price)
        if district_id:
            events = events.filter(district_id=district_id)
        if city_id:
            events = events.filter(city_id=city_id)
        if search:
            events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))

        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(events, request)
        serializer = EventListSerializer(result_page, many=True)

        response_data = {
            'total_pages': paginator.page.paginator.num_pages,
            'results': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class EventNoActivListAPIView(APIView):
    permission_classes = [IsAdminAndModerator]

    @swagger_auto_schema(
        responses={200: openapi.Response('List of events status no active', EventListSerializer(many=True))},
        operation_summary="Retrieve a list of events",
        operation_description="This endpoint retrieves a paginated list with filter and search of events."
    )
    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(is_banned=True)

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        district_id = request.query_params.get('district')
        city_id = request.query_params.get('city')
        search = request.query_params.get('search')

        if min_price:
            events = events.filter(price__gte=min_price)
        if max_price:
            events = events.filter(price__lte=max_price)
        if district_id:
            events = events.filter(district_id=district_id)
        if city_id:
            events = events.filter(city_id=city_id)

        if search:
            events = events.filter(Q(title__icontains=search) | Q(description__icontains=search))

        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(events, request)
        serializer = EventListSerializer(result_page, many=True)

        response_data = {
            'total_pages': paginator.page.paginator.num_pages,
            'results': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class EventDetailAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Response('List of events', EventListSerializer())},
        operation_summary="Retrieve a list of events",
        operation_description="Детальная информация об афишы"
    )
    def get(self, request, id_event, *args, **kwargs):

        events = Event.objects.get(id=id_event)

        events_serializer = EventListSerializer(events)

        events.increment_views()

        return Response(events_serializer.data, status.HTTP_200_OK)


class EventOnModerationListAPIView(APIView):
    permission_classes = [IsAdminAndModerator]

    @swagger_auto_schema(
        responses={200: openapi.Response('List of events status on moderation', EventListSerializer(many=True))},
        operation_summary="Retrieve a list of events",
        operation_description="This endpoint retrieves a paginated list"
    )
    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(on_moderation=True)

        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(events, request)
        serializer = EventListSerializer(result_page, many=True)

        response_data = {
            'total_pages': paginator.page.paginator.num_pages,
            'results': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PassedModerationAPIView(APIView):
    permission_classes = [IsAdminAndModerator]

    @swagger_auto_schema(
        operation_description="This endpoint passed moderation of event"
    )
    def put(self, request, id_event, *args, **kwargs):

        events = Event.objects.get(id=id_event)
        events.passed_moderation()

        return Response(status.HTTP_200_OK)


class HideOrActiveEventAPIView(APIView):
    permission_classes = [IsOwnerOfEvent, IsAuthenticated]

    @swagger_auto_schema(
        operation_description="This endpoint to hide or activate event"
    )
    def put(self, request, id_event, *args, **kwargs):
        action = request.query_params.get('action')
        events = Event.objects.get(id=id_event)
        if action == 'hide':
            events.hide_event()
            return Response(status=status.HTTP_200_OK)
        if action == 'active':
            events.active_event()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
