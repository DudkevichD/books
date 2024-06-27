from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class AccountTests(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Book 1', price=100)
        book_2 = Book.objects.create(name='Book 2', price=200)
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        serializer_data = BookSerializer([book_1, book_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
