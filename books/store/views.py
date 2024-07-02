from django.db.models import Avg, Count, Case, When
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from store.models import Book, Stock, Shop, Quote, Comment, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer, UserBookRelationSerializer, CommentSerializer, QuoteSerializer, \
    StockSerializer, ShopSerializer


def oauth(request):
    return render(request, 'oauth.html')


class OwnerStaffReadOnlyModelViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrStaffOrReadOnly]


# Create your views here.
class BookViewSet(OwnerStaffReadOnlyModelViewSet):
    """
    ViewSet for the Book model.
    Provides CRUD operations for the Book model.
    Uses custom permissions: only the owner or staff can modify data.
    """
    queryset = Book.objects.all().select_related('owner').prefetch_related('shops').annotate(
        rate=Avg('userbookrelation__rate')).annotate(
        likes_count=Count(Case(When(userbookrelation__like=True, then=1))))
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationViewSet(OwnerStaffReadOnlyModelViewSet):
    """
    ViewSet for the UserBookRelation model.
    Provides CRUD operations for the UserBookRelation model.
    Uses custom permissions: only the owner or staff can modify data.
    """
    queryset = UserBookRelation.objects.all().select_related('user', 'book')
    serializer_class = UserBookRelationSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        return obj


class CommentViewSet(OwnerStaffReadOnlyModelViewSet):
    """
    ViewSet for the Comment model.
    Provides CRUD operations for the Comment model.
    Uses custom permissions: only the owner or staff can modify data.
    """
    queryset = Comment.objects.all().select_related('user', 'book')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class QuoteViewSet(OwnerStaffReadOnlyModelViewSet):
    """
    ViewSet for the Quote model.
    Provides CRUD operations for the Quote model.
    Uses custom permissions: only the owner or staff can modify data.
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class ShopViewSet(OwnerStaffReadOnlyModelViewSet):
    """
        ViewSet for the Shop model.
        Provides CRUD operations for the Shop model.
        Uses custom permissions: only the owner or staff can modify data.
    """
    queryset = Shop.objects.all().prefetch_related('books')
    serializer_class = ShopSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class StockViewSet(OwnerStaffReadOnlyModelViewSet):
    """
    ViewSet for the Stock model.
    Provides CRUD operations for the Stock model.
    Uses custom permissions: only the owner or staff can modify data.
    """
    queryset = Stock.objects.all().select_related('shop', 'book')
    serializer_class = StockSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
