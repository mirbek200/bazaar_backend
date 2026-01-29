from django.contrib import admin
from .models import Category, SubCategory, UnderSubCategory

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UnderSubCategory)
