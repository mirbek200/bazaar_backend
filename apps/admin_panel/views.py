import csv
import json

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.admin_panel.logic import get_announcement_stats, get_banned_announcements_stats
from apps.admin_panel.models import Category, SubCategory, UnderSubCategory
from apps.admin_panel.serializers import ModeratorCreateSerializer, CategorySerializer, SubCategorySerializer, \
    UnderSubCategorySerializer, CategoryWithSubSerializer, CategorySerializerFCCASC, \
    SubCategoryCreateOrUpdateSerializer, ModeratorsListSerializer, ModeratorsDetailSerializer, \
    SubCategoryWithUnderSerializer
from apps.announcement.models import Announcement
from apps.events.models import Event
from apps.users.models import MyUser
from thailand_bazar.logic.send_email import send_email_after_ban


class ModeratorCreateView(APIView):
    serializer_class = ModeratorCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = ModeratorCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = MyUser.objects.create(
                full_name=request.data['full_name'],
                email=request.data['email'],
                phone_number=request.data['phone_number'],
                is_moderator=True,
                is_active=True,
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModeratorsListAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        moderators = MyUser.objects.filter(is_moderator=True)
        serializer = ModeratorsListSerializer(moderators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ModeratorDetailAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(MyUser, pk=pk)

    def get(self, request, pk):
        moderator = self.get_object(pk)
        serializer = ModeratorsDetailSerializer(moderator)
        return Response(serializer.data)

    def delete(self, request, pk):
        moderator = self.get_object(pk)
        moderator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithSubSerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class SubCategoryCreateAPIView(generics.CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAdminUser]


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryWithUnderSerializer


class SubCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryWithUnderSerializer
    permission_classes = [permissions.IsAdminUser]


class UnderSubCategoryCreateAPIView(generics.CreateAPIView):
    queryset = UnderSubCategory.objects.all()
    serializer_class = UnderSubCategorySerializer
    permission_classes = [permissions.IsAdminUser]


class UnderSubCategoryListAPIView(generics.ListAPIView):
    queryset = UnderSubCategory.objects.all()
    serializer_class = UnderSubCategorySerializer


class UnderSubCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnderSubCategory.objects.all()
    serializer_class = UnderSubCategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryAndSubCategoryCreateView(APIView):
    def post(self, request):
        serializer = CategorySerializerFCCASC(data=request.data)

        if serializer.is_valid():
            sub_categories = serializer.data['sub_categories']
            sub_categories = json.loads(sub_categories)
            category_title = serializer.validated_data['category_title']
            category_icon = serializer.validated_data['category_icon']

            category = Category.objects.create(
                category_title=category_title,
                category_icon=category_icon
            )

            for sub_category_data in sub_categories:
                SubCategory.objects.create(
                    sub_category_title=sub_category_data['sub_category_title'],
                    category_title_fk=category
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryCreateOrUpdateView(APIView):

    def patch(self, request, id):
        serializer = SubCategoryCreateOrUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.get(id=id)

        if "del_sub_categories" in serializer.data:
            del_sub_categories = serializer.data['del_sub_categories']
            del_sub_categories = json.loads(del_sub_categories)

            for del_sub_category in del_sub_categories:
                sub_category = SubCategory.objects.get(id=del_sub_category)
                sub_category.delete()

        if "new_sub_categories" in serializer.data:
            new_sub_categories = serializer.data['new_sub_categories']
            new_sub_categories = json.loads(new_sub_categories)

            for new_sub_category in new_sub_categories:
                SubCategory.objects.create(
                    sub_category_title=new_sub_category,
                    category_title_fk=category
                )

        if "name" in serializer.data and serializer.data['name'] != category.category_title:
            name = serializer.data['name']

            category.category_title = name
            category.save()

        if "icon" in serializer.data:
            icon = request.FILES['icon']

            category.category_icon = icon
            category.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BanToUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def deactivate_related_objects(self, user):
        Announcement.objects.filter(user=user).update(is_active=False)
        Event.objects.filter(user=user).update(is_active=False)

    def put(self, request, user_id):
        user = get_object_or_404(MyUser, id=user_id)

        if request.user.id == user.id or request.user.is_moderator:
            user.is_active = False
            user.save()
            self.deactivate_related_objects(user)
            send_email_after_ban(user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class BanToUserAdmin(APIView):
    permission_classes = [permissions.IsAdminUser]

    def deactivate_related_objects(self, user):
        Announcement.objects.filter(user=user).update(is_active=False)
        Event.objects.filter(user=user).update(is_active=False)

    def put(self, request, user_id):
        user = get_object_or_404(MyUser, id=user_id)
        user.is_active = False
        user.save()
        self.deactivate_related_objects(user)
        send_email_after_ban(user)
        return Response(status=status.HTTP_200_OK)

class ActiveToUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        user = get_object_or_404(MyUser, id=user_id)
        if request.user.is_moderator:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class Statistic(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response(get_announcement_stats(), status=status.HTTP_200_OK)


class StatisticBannedAnnouncements(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response(get_banned_announcements_stats(), status=status.HTTP_200_OK)


class TopFourCategoriesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        top_categories = Category.objects.annotate(
            announcement_count=Count('announcement')
        ).order_by('-announcement_count')[:4]

        serializer = CategorySerializer(top_categories, many=True)
        return Response(serializer.data)


class CountOfUsersAndAnnouncementsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        active_users_count = MyUser.objects.filter(is_active=True).count()
        active_announcements_count = Announcement.objects.filter(is_active=True).count()
        data = {
            'active_users_count': active_users_count,
            'active_announcements_count': active_announcements_count
        }
        return Response(data, status=status.HTTP_200_OK)


class ExportAnnouncementsCSV(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        start_date = timezone.datetime.strptime(start_date, '%d-%m-%Y').replace(tzinfo=timezone.utc) if start_date else None
        end_date = timezone.datetime.strptime(end_date, '%d-%m-%Y').replace(tzinfo=timezone.utc) if end_date else None

        queryset = Announcement.objects.all()

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="announcements_export.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['ID', 'Created At', 'User Email', 'User Name'])

        for announcement in queryset:
            csv_writer.writerow([
                announcement.id,
                announcement.created_at,
                announcement.user.email,
                announcement.user.full_name
            ])

        return response


class AdminDeleteAnnouncementAPIView(generics.DestroyAPIView):
    queryset = Announcement.objects.all()
    permission_classes = [permissions.IsAdminUser]
