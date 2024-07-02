from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255, default='')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')

    def __str__(self):
        return f"{self.name} : {self.price} : {self.author_name}"


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Terrible'),
        (2, 'Bad'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def get_object(self):
        obl, _ = UserBookRelation.objects.get_or_create(user=self.user, book=self.book)

    def __str__(self):
        return f"{self.user.username}: {self.book.name} : {self.like}"


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.book.name} : {self.text[:10]}"


class Quote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.book.name} : {self.text[:10]}"


class Shop(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='shops')

    def __str__(self):
        return self.name


class Stock(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.shop.name} : {self.book.name} : {self.count}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)  # many to many
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    def get_items(self):
        return self.books.all().count()

    def __str__(self):
        return f"{self.user.username} : {self.total_price}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.order.user.username} : {self.book.name} : {self.count}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)  # many to many
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} : {self.total_price}"
