import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Book, UserBookRelation, Comment, Quote, Shop, Stock, Order, OrderItem, Cart

def populate_data():
    user1 = User.objects.create_user(username='alexey', password='password1', first_name='Алексей', last_name='Иванов')
    user2 = User.objects.create_user(username='maria', password='password2', first_name='Мария', last_name='Петрова')
    user3 = User.objects.create_user(username='ivan', password='password3', first_name='Иван', last_name='Сидоров')

    book1 = Book.objects.create(name='Война и мир', price=500.00, author_name='Лев Толстой', owner=user1)
    book2 = Book.objects.create(name='Преступление и наказание', price=300.00, author_name='Фёдор Достоевский', owner=user2)
    book3 = Book.objects.create(name='Мастер и Маргарита', price=400.00, author_name='Михаил Булгаков', owner=user3)

    UserBookRelation.objects.create(user=user1, book=book1, like=True, rate=5)
    UserBookRelation.objects.create(user=user2, book=book2, like=True, rate=4)
    UserBookRelation.objects.create(user=user3, book=book3, like=True, rate=5)

    Comment.objects.create(user=user1, book=book1, text='Великолепная книга!')
    Comment.objects.create(user=user2, book=book2, text='Очень интересное произведение.')
    Comment.objects.create(user=user3, book=book3, text='Захватывающая история.')

    Quote.objects.create(book=book1, text='Все счастливые семьи похожи друг на друга...', author='Лев Толстой', owner=user1)
    Quote.objects.create(book=book2, text='Красота спасет мир.', author='Фёдор Достоевский', owner=user2)
    Quote.objects.create(book=book3, text='Рукописи не горят.', author='Михаил Булгаков', owner=user3)

    shop1 = Shop.objects.create(name='Библио-Глобус')
    shop2 = Shop.objects.create(name='Читай-город')
    shop1.books.add(book1, book2)
    shop2.books.add(book3)
    Stock.objects.create(shop=shop1, book=book1, count=10)
    Stock.objects.create(shop=shop1, book=book2, count=5)
    Stock.objects.create(shop=shop2, book=book3, count=8)

    order = Order.objects.create(user=user1, total_price=800.00)
    order.books.add(book1, book2)
    OrderItem.objects.create(order=order, book=book1, count=1)
    OrderItem.objects.create(order=order, book=book2, count=1)

    cart = Cart.objects.create(user=user1, total_price=800.00)
    cart.books.add(book1, book2)

    print('Successfully populated the database with initial data')

if __name__ == '__main__':
    populate_data()