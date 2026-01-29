from django.db import models


class Category(models.Model):
    category_title = models.CharField(max_length=255, null=False, blank=False)
    category_icon = models.ImageField(upload_to='category_icons/', null=False, blank=False)


class SubCategory(models.Model):
    sub_category_title = models.CharField(max_length=255, null=False, blank=False)
    category_title_fk = models.ForeignKey(Category, on_delete=models.CASCADE)


class UnderSubCategory(models.Model):
    under_sub_category_title = models.CharField(max_length=255, null=False, blank=False)
    sub_category_title_fk = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
