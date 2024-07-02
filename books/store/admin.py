from django.contrib import admin
from .models import Book, UserBookRelation, Comment, Quote, Shop, Stock

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'author_name', 'owner')
    search_fields = ('name', 'author_name')
    list_filter = ('price',)

@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'like', 'in_bookmarks', 'rate')
    search_fields = ('user__username', 'book__name')
    list_filter = ('like', 'in_bookmarks', 'rate')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'datetime_created')
    search_fields = ('user__username', 'book__name', 'text')
    list_filter = ('datetime_created',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('book', 'text', 'author', 'owner')
    search_fields = ('book__name', 'author', 'text')
    list_filter = ('author',)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('shop', 'book', 'count')
    search_fields = ('shop__name', 'book__name')
    list_filter = ('shop', 'book')
