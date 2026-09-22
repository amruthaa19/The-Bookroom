from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return self.title


class BorrowBook(models.Model):
    username = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username + " - " + self.book.title