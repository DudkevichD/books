from unittest import TestCase

from django.contrib.auth.models import User

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        book_1 = Book.objects.create(name='Book 1', price=100, author_name='Author 1', owner=self.user)
        book_2 = Book.objects.create(name='Book 2', price=200, author_name='Author 2', owner=None)
        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Book 1',
                'price': '100.00',
                'author_name': 'Author 1',
                'owner': self.user.id
            },
            {
                'id': book_2.id,
                'name': 'Book 2',
                'price': '200.00',
                'author_name': 'Author 2',
                'owner': None
            }
        ]
        self.assertEqual(expected_data, data)
