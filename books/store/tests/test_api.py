from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.book1 = Book.objects.create(name='Война и мир', price=500.00, author_name='Лев Толстой')
        self.book2 = Book.objects.create(name='Преступление и наказание', price=300.00, author_name='Фёдор Достоевский')
        self.book3 = Book.objects.create(name='Мастер и Маргарита', price=400.00, author_name='Михаил Булгаков')
        self.book4 = Book.objects.create(name='Анна Каренина', price=600.00, author_name='Лев Толстой')
        self.book5 = Book.objects.create(name='Идиот', price=350.00, author_name='Фёдор Достоевский')

    def test_filter_by_price(self):
        url = reverse('book-list')
        response = self.client.get(url, {'price': 300.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Преступление и наказание')

    def test_search_by_name(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Война и мир'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Война и мир')

    def test_search_by_author_name(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Фёдор Достоевский'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['author_name'], 'Фёдор Достоевский')
        self.assertEqual(response.data[1]['author_name'], 'Фёдор Достоевский')

    def test_ordering_by_price(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'price'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Преступление и наказание')
        self.assertEqual(response.data[1]['name'], 'Идиот')
        self.assertEqual(response.data[2]['name'], 'Мастер и Маргарита')
        self.assertEqual(response.data[3]['name'], 'Война и мир')
        self.assertEqual(response.data[4]['name'], 'Анна Каренина')

    def test_ordering_by_author_name(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'author_name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author_name'], 'Лев Толстой')
        self.assertEqual(response.data[1]['author_name'], 'Лев Толстой')
        self.assertEqual(response.data[2]['author_name'], 'Михаил Булгаков')
        self.assertEqual(response.data[3]['author_name'], 'Фёдор Достоевский')
        self.assertEqual(response.data[4]['author_name'], 'Фёдор Достоевский')

    def test_get_books(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        books = Book.objects.all()
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_single_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url, format='json')
        serializer_data = BookSerializer(self.book1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'name': 'Новая книга',
            'price': '700.00',
            'author_name': 'Новый автор'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 6)
        self.assertEqual(Book.objects.get(id=response.data['id']).name, 'Новая книга')

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            'name': 'Война и мир (обновлено)',
            'price': '800.00',
            'author_name': 'Лев Толстой'
        }
        response = self.client.put(url, data, format='json')
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.name, 'Война и мир (обновлено)')
        self.assertEqual(self.book1.price, 800.00)

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 4)