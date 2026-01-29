from rest_framework import serializers

from apps.forbidden_words.models import ForbiddenWords


class ForbiddenWordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForbiddenWords
        fields = "__all__"

class CreateForbiddenWordsSerializer(serializers.Serializer): # noqa
    words = serializers.ListField(child=serializers.CharField(max_length=255))


class ForbiddenWordsListSerializer(serializers.ListSerializer): # noqa
    child = ForbiddenWordsSerializer()


class UpdateForbiddenWordsSerializer(serializers.Serializer):
    delete_words = serializers.ListField(child=serializers.IntegerField())
    update_words = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))
    new_words = serializers.ListField(child=serializers.CharField(max_length=255))

    def update_forbidden_words(self):
        delete_words = self.validated_data.get('delete_words', [])
        update_words = self.validated_data.get('update_words', [])
        new_words = self.validated_data.get('new_words', [])

        ForbiddenWords.objects.filter(id__in=delete_words).delete()

        for word_data in update_words:
            word_id = word_data.get('id')
            try:
                word = ForbiddenWords.objects.get(id=word_id)
                word.word = word_data.get('word')
                word.save()
            except ForbiddenWords.DoesNotExist:
                pass

        new_words_objects = [ForbiddenWords(word=word) for word in new_words]
        ForbiddenWords.objects.bulk_create(new_words_objects)



