from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from store.views import BookViewSet, oauth

router = SimpleRouter()
router.register(r'book', BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('oauth/', oauth)
]

urlpatterns += router.urls
