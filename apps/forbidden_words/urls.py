from django.urls import path
from apps.forbidden_words.views import CreateForbiddenWordsView, UpdateForbiddenWordsView, \
    ForbiddenWordsListAPIView, DeleteForbiddenWordAPIView, DeleteAllForbiddenWordAPIView

urlpatterns = [
    path('create/', CreateForbiddenWordsView.as_view(), name="create"),
    path('update/', UpdateForbiddenWordsView.as_view(), name="create"),
    path('list/', ForbiddenWordsListAPIView.as_view(), name="list"),
    path('delete/<int:forbidden_word_id>/', DeleteForbiddenWordAPIView.as_view(), name="delete"),
    path('delete_all/', DeleteAllForbiddenWordAPIView.as_view(), name="delete"),
]
