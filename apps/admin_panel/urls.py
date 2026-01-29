from django.urls import path
from apps.admin_panel.views import ModeratorCreateView, CategoryCreateAPIView, CategoryListAPIView, \
    CategoryRetrieveUpdateDestroyAPIView, SubCategoryCreateAPIView, SubCategoryListAPIView, \
    SubCategoryRetrieveUpdateDestroyAPIView, UnderSubCategoryCreateAPIView, UnderSubCategoryListAPIView, \
    UnderSubCategoryRetrieveUpdateDestroyAPIView, CategoryAndSubCategoryCreateView, SubCategoryCreateOrUpdateView, \
    ModeratorsListAPIView, ModeratorDetailAPIView, BanToUser, ActiveToUser, Statistic, TopFourCategoriesView, \
    CountOfUsersAndAnnouncementsView, ExportAnnouncementsCSV, StatisticBannedAnnouncements, BanToUserAdmin, \
    AdminDeleteAnnouncementAPIView

urlpatterns = [
    path('moderator_create/', ModeratorCreateView.as_view(), name='moderator_create'),
    path('moderator_list/', ModeratorsListAPIView.as_view(), name='moderator_list'),
    path('moderator_detail/<int:pk>/', ModeratorDetailAPIView.as_view(), name='moderator_detail'),

    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path('category/create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),

    path('subcategory/', SubCategoryListAPIView.as_view(), name='sub-category-list'),
    path('subcategory/create/', SubCategoryCreateAPIView.as_view(), name='sub-category-create'),
    path('subcategory/<int:pk>/', SubCategoryRetrieveUpdateDestroyAPIView.as_view(), name='sub-category-detail'),

    path('undersubcategory/', UnderSubCategoryListAPIView.as_view(), name='under-subcategory-list'),
    path('undersubcategory/create/', UnderSubCategoryCreateAPIView.as_view(), name='under-subcategory-create'),
    path('undersubcategory/<int:pk>/', UnderSubCategoryRetrieveUpdateDestroyAPIView.as_view(),
         name='under-subcategory-detail'),

    path('category_and_sub_category_craete/', CategoryAndSubCategoryCreateView.as_view(), name='category-create'),

    path('sub_category_create_or_update/<int:id>/', SubCategoryCreateOrUpdateView.as_view(),
         name='category-create-or-update'),

    path('ban_to_user/<int:user_id>/', BanToUser.as_view(),
         name='ban_to_user'),

    path('ban_to_user_admin/<int:user_id>/', BanToUserAdmin.as_view(),
             name='ban_to_user_admin'),

    path('active_to_user/<int:user_id>/', ActiveToUser.as_view(),
         name='active_to_user'),
    path('statistic/', Statistic.as_view(), name='statistic'),
    path('statistic_banned_announcements/', StatisticBannedAnnouncements.as_view(), name='statistic_complaint'),
    path('top_four_categories/', TopFourCategoriesView.as_view(), name='top_four_categories'),
    path('count_of_user_and_announcements/', CountOfUsersAndAnnouncementsView.as_view(),
         name='count_of_user_and_announcements'),

    path('export_announcements/', ExportAnnouncementsCSV.as_view(), name='export-announcements'),
    path('del_ann/<int:pk>/', AdminDeleteAnnouncementAPIView.as_view(), name='del_ann'),
]
