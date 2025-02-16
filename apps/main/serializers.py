from rest_framework import serializers
from .models import News
from apps.products.models import Category, ProductImage, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']

class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()  

    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'tags', 'text', 'published_at']

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()] 

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'rating', 'images']