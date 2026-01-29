from django.db import models


class ForbiddenWords(models.Model):
    word = models.CharField(max_length=255, verbose_name="слова")

    class Meta:
        verbose_name = "Запрещенные слова"
        verbose_name_plural = "Запрещенные словы"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.id}"
