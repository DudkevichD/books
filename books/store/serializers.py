from rest_framework import serializers
from .models import Book, UserBookRelation, Comment, Quote, Shop, Stock


class BookSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    rate = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'author_name', 'owner', 'like_count', 'rate']

    def get_like_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()

class UserBookRelationSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), pk_field=serializers.IntegerField())

    class Meta:
        model = UserBookRelation
        fields = ['id', 'user', 'book', 'like', 'in_bookmarks', 'rate']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'book', 'text', 'datetime_created']


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'book', 'text', 'author', 'owner']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'books']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'shop', 'book', 'count']
