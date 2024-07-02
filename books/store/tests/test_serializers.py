from django.db.models import Avg, Count, Case, When
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from store.models import Book, UserBookRelation, Comment, Quote, Shop, Stock
from store.serializers import BookSerializer, UserBookRelationSerializer, CommentSerializer, QuoteSerializer, \
    ShopSerializer, StockSerializer
from datetime import timezone
from freezegun import freeze_time


class BookSerializerTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase_user', password='testpassword')
        self.user2 = User.objects.create_user(username='testcase_user2', password='testpassword')

    def tearDown(self):
        User.objects.all().delete()
        Book.objects.all().delete()

    def test_book_serialization(self):
        book = Book.objects.create(name='Book 1', price=100, author_name='Author 1', owner=self.user)
        UserBookRelation.objects.create(user=self.user, book=book, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=book, like=False, rate=3)
        book = Book.objects.annotate(rate=Avg('userbookrelation__rate')).annotate(
            like_count=Count(Case(When(userbookrelation__like=True, then=1)))).get(id=book.id)
        data = BookSerializer(book).data
        expected_data = {
            'id': book.id,
            'name': 'Book 1',
            'price': '100.00',
            'author_name': 'Author 1',
            'owner': self.user.id,
            'like_count': 1,
            'rate': '4.00'
        }
        self.assertEqual(expected_data, data)

    def test_book_serialization_without_owner(self):
        book = Book.objects.create(name='Book 2', price=200, author_name='Author 2')
        book = Book.objects.annotate(rate=Avg('userbookrelation__rate')).annotate(
            like_count=Count(Case(When(userbookrelation__like=True, then=1)))).get(id=book.id)
        data = BookSerializer(book).data
        expected_data = {
            'id': book.id,
            'name': 'Book 2',
            'price': '200.00',
            'author_name': 'Author 2',
            'owner': None,
            'like_count': 0,
            'rate':  None,
        }
        self.assertEqual(expected_data, data)


class UserBookRelationSerializerTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase_user', password='testpassword')
        self.book = Book.objects.create(name='Book 1', price=100, author_name='Author 1')

    def tearDown(self):
        User.objects.all().delete()
        Book.objects.all().delete()
        UserBookRelation.objects.all().delete()

    def test_book_relation_serialization(self):
        book_relation = UserBookRelation.objects.create(user=self.user, book=self.book, like=True, in_bookmarks=True,
                                                        rate=5)
        data = UserBookRelationSerializer(book_relation).data
        expected_data = {
            'id': book_relation.id,
            'user': self.user.id,
            'book': self.book.id,
            'like': True,
            'in_bookmarks': True,
            'rate': 5
        }
        self.assertEqual(expected_data, data)

    def test_book_relation_serialization_without_rate(self):
        book_relation = UserBookRelation.objects.create(user=self.user, book=self.book, like=False, in_bookmarks=False)
        data = UserBookRelationSerializer(book_relation).data
        expected_data = {
            'id': book_relation.id,
            'user': self.user.id,
            'book': self.book.id,
            'like': False,
            'in_bookmarks': False,
            'rate': None
        }
        self.assertEqual(expected_data, data)


class CommentSerializerTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase_user', password='testpassword')
        self.book = Book.objects.create(name='Book 1', price=100, author_name='Author 1')

    def tearDown(self):
        User.objects.all().delete()
        Book.objects.all().delete()
        Comment.objects.all().delete()

    @freeze_time('2024-06-29T00:00:00.000000+00:00')
    def test_comment_serialization(self):
        comment = Comment.objects.create(user=self.user, book=self.book, text='Great book!')
        data = CommentSerializer(comment).data
        expected_data = {
            'id': comment.id,
            'user': self.user.id,
            'book': self.book.id,
            'text': 'Great book!',
            'datetime_created': '2024-06-29T00:00:00Z'
        }
        self.assertEqual(expected_data, data)

    def test_comment_serialization_empty_text(self):
        comment = Comment.objects.create(user=self.user, book=self.book, text='')
        data = CommentSerializer(comment).data
        expected_data = {
            'id': comment.id,
            'user': self.user.id,
            'book': self.book.id,
            'text': '',
            'datetime_created': comment.datetime_created.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        self.assertEqual(expected_data, data)


class QuoteSerializerTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase_user', password='testpassword')
        self.book = Book.objects.create(name='Book 1', price=100, author_name='Author 1')

    def tearDown(self):
        User.objects.all().delete()
        Book.objects.all().delete()
        Quote.objects.all().delete()

    def test_quote_serialization(self):
        quote = Quote.objects.create(book=self.book, text='Inspiring quote', author='Author 1', owner=self.user)
        data = QuoteSerializer(quote).data
        expected_data = {
            'id': quote.id,
            'book': self.book.id,
            'text': 'Inspiring quote',
            'author': 'Author 1',
            'owner': self.user.id
        }
        self.assertEqual(expected_data, data)

    def test_quote_serialization_without_owner(self):
        quote = Quote.objects.create(book=self.book, text='Another quote', author='Author 2')
        data = QuoteSerializer(quote).data
        expected_data = {
            'id': quote.id,
            'book': self.book.id,
            'text': 'Another quote',
            'author': 'Author 2',
            'owner': None
        }
        self.assertEqual(expected_data, data)


class ShopSerializerTestCase(TransactionTestCase):
    def tearDown(self):
        Shop.objects.all().delete()
        Book.objects.all().delete()

    def test_shop_serialization(self):
        shop = Shop.objects.create(name='Shop 1')
        data = ShopSerializer(shop).data
        expected_data = {
            'id': shop.id,
            'name': 'Shop 1',
            'books': []
        }
        self.assertEqual(expected_data, data)

    def test_shop_serialization_with_books(self):
        shop = Shop.objects.create(name='Shop 2')
        book1 = shop.books.create(name='Book 1', price=100, author_name='Author 1')
        book2 = shop.books.create(name='Book 2', price=200, author_name='Author 2')
        data = ShopSerializer(shop).data
        expected_data = {
            'id': shop.id,
            'name': 'Shop 2',
            'books': [book1.id, book2.id]
        }
        self.assertEqual(expected_data, data)


class StockSerializerTestCase(TransactionTestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name='Shop 1')
        self.book = Book.objects.create(name='Book 1', price=100, author_name='Author 1')

    def tearDown(self):
        Shop.objects.all().delete()
        Book.objects.all().delete()
        Stock.objects.all().delete()

    def test_stock_serialization(self):
        stock = Stock.objects.create(shop=self.shop, book=self.book, count=10)
        data = StockSerializer(stock).data
        expected_data = {
            'id': stock.id,
            'shop': self.shop.id,
            'book': self.book.id,
            'count': 10
        }
        self.assertEqual(expected_data, data)

    def test_stock_serialization_zero_count(self):
        stock = Stock.objects.create(shop=self.shop, book=self.book, count=0)
        data = StockSerializer(stock).data
        expected_data = {
            'id': stock.id,
            'shop': self.shop.id,
            'book': self.book.id,
            'count': 0
        }
        self.assertEqual(expected_data, data)
