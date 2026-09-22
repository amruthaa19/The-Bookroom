from django.contrib import admin
from .models import Book, BorrowBook

admin.site.register(Book)
admin.site.register(BorrowBook)