from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter any book genre (Eg: Science Fiction, Fantasy, etc.)"
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
       constraints = [
           UniqueConstraint(
               Lower('name'),
               name='genre_name_case_insensitive_unique',
               violation_error_message="Genre already exists (case insensitive match)"
           )
       ]

class Book(models.Model):
    """Model representing a Book"""

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)

    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book"
        )
    
    isbn = models.CharField("ISBN", max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>'
                            )
    
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    

class BookInstance(models.Model):
    """Model representing book instance (availibility in the library)"""

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text="Unique ID for this particular book across whole library"
        )
    
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenence'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def _str__(self):
        return f"{self.id} {self.book.title}"
    
class Author(models.Model):
    """Model representing an Author"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank="True")
    date_of_death = models.DateField('Death', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-details', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
