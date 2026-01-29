from rest_framework import serializers

from apps.admin_panel.models import Category, SubCategory, UnderSubCategory
from apps.users.models import MyUser


class ModeratorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class ModeratorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'


class ModeratorsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'full_name', 'email', 'phone_number']

# For Generics


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class UnderSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnderSubCategory
        fields = '__all__'

# For Category List


class SubCategoryWithUnderSerializer(serializers.ModelSerializer):
    under_sub_categories = UnderSubCategorySerializer(source='undersubcategory_set', many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'sub_category_title', 'under_sub_categories']


class CategoryWithSubSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryWithUnderSerializer(source='subcategory_set', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'category_title', 'category_icon', 'sub_categories']


# For Create Category And SubCategory


class CategorySerializerFCCASC(serializers.Serializer):
    category_title = serializers.CharField(max_length=255)
    category_icon = serializers.ImageField()
    sub_categories = serializers.CharField(max_length=255)


# For Update Category And SubCategory


class SubCategoryCreateOrUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    icon = serializers.ImageField(required=False)
    del_sub_categories = serializers.CharField(max_length=400, required=False)
    new_sub_categories = serializers.CharField(max_length=400, required=False)
