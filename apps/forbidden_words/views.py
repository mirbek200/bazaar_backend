from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.forbidden_words.models import ForbiddenWords
from apps.forbidden_words.serializers import CreateForbiddenWordsSerializer, UpdateForbiddenWordsSerializer, \
    ForbiddenWordsSerializer


class CreateForbiddenWordsView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=CreateForbiddenWordsSerializer(),
        responses={201: "Words created successfully", 400: "Bad Request"},
        operation_description="Create Forbidden Words"
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateForbiddenWordsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        words_to_create = serializer.data['words']
        for i in words_to_create:
            word = ForbiddenWords.objects.filter(word=i).first()
            if word:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        words_objects = [ForbiddenWords(word=word) for word in words_to_create]
        ForbiddenWords.objects.bulk_create(words_objects)
        return Response(status=status.HTTP_201_CREATED)


class UpdateForbiddenWordsView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=UpdateForbiddenWordsSerializer,
        responses={200: "Forbidden words updated", 400: "Bad Request"},
        operation_description="Update forbidden words"
    )
    def put(self, request, *args, **kwargs):
        serializer = UpdateForbiddenWordsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update_forbidden_words()
        return Response("Forbidden words updated", status=status.HTTP_200_OK)


class ForbiddenWordsListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={200: openapi.Response('List of forbidden words', ForbiddenWordsSerializer())},
        operation_summary="Retrieve a list of announcements",
        operation_description="List of forbidden words"
    )
    def get(self, request, *args, **kwargs):
        announcements = ForbiddenWords.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10

        page = paginator.paginate_queryset(announcements, request)
        if page is not None:
            announcements_serializer = ForbiddenWordsSerializer(page, many=True)
            return paginator.get_paginated_response(announcements_serializer.data)

        announcements_serializer = ForbiddenWordsSerializer(announcements, many=True)
        return Response(announcements_serializer.data, status.HTTP_200_OK)


class DeleteForbiddenWordAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Delete forbidden word",
        operation_description="Delete forbidden word"
    )
    def delete(self, request, forbidden_word_id, *args, **kwargs):
        ForbiddenWords.objects.get(id=forbidden_word_id).delete()
        return Response("Запрещенное слово удалено", status.HTTP_204_NO_CONTENT)


class DeleteAllForbiddenWordAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Delete all forbidden word",
        operation_description="Delete all forbidden word"
    )
    def delete(self, request, *args, **kwargs):
        try:
            ForbiddenWords.objects.all().delete()
            response_data = {'success': True, 'message': 'Все данные удалены успешно.'}
            status_code = 200
        except Exception as e:
            response_data = {'success': False, 'message': str(e)}
            status_code = 500

        return Response(response_data, status=status_code)
