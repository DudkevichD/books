from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from store.views import BookViewSet, oauth, UserBookRelationViewSet, CommentViewSet, QuoteViewSet, StockViewSet, \
    ShopViewSet

router = SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'userbookrelation', UserBookRelationViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'quote', QuoteViewSet)
router.register(r'stock', StockViewSet)
router.register(r'shop', ShopViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('oauth/', oauth)
]

urlpatterns += router.urls
