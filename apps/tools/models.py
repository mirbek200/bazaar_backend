from django.db import models


class City(models.Model):
    name = models.CharField("Город", max_length=30)
    is_active = models.BooleanField("Активный", default=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        is_active_changed = self.pk is not None and self.is_active != City.objects.get(pk=self.pk).is_active
        super().save(*args, **kwargs)
        if is_active_changed:
            self.city.update(is_active=self.is_active)


class District(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name="Район", related_name="city"
    )
    name = models.CharField("Район", max_length=70)
    is_active = models.BooleanField("Активный", default=True)

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        ordering = ("id",)

    def __str__(self) -> str:
        return self.name
