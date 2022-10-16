from django.contrib import admin

# Register your models here.
from book_management.models import Book, Issue

admin.site.register(Book)
admin.site.register(Issue)