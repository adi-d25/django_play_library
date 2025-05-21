from django.contrib import admin
from .models import Book, Genre, BookInstance, Author

# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Author)

