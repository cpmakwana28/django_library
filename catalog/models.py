from django.db import models
from django.contrib.auth.models import User

from datetime import date


# class Book(models.Model):
#     """A typical class defining a model, derived from the Model class."""
    
#     ENGLISH = 'ENG'
#     HINDI = 'HIN'
#     FRENCH = 'FRA'
#     FINNISH = 'FIN'
#     JAPANESE = 'JPN'
    
#     """A new migration is created each time the order of choices changes."""

#     LANGUAGES = [
#         (ENGLISH, 'english'),    #(value as stored in database , human_readable_name)
#         (HINDI, 'hindi'),
#         (FRENCH, 'french'),
#         (FINNISH, 'finnish'),
#         (JAPANESE, 'japanese'),
#     ]
#     # Fields
#     language=models.CharField(max_length=20,help_text="language",choices=LANGUAGES,default=HINDI)
    
    
    
#     # Metadata
#     class Meta:
#         ordering = ['language']

#     # # Methods
#     # def get_absolute_url(self):
#     #     """Returns the url to access a particular instance of MyModelName."""
#     #     return reverse('model-detail-view', args=[str(self.id)])

#     def __str__(self):
#         """String for representing the MyModelName object (in Admin site etc.)."""
#         return self.language



class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name



from django.urls import reverse # Used to generate URLs by reversing the URL patterns




class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200,default="",help_text="ENTER TITLE")

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000,default=" ",help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,default="",
                             help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
   
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'



import uuid # Required for unique book instances



class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL, null =True, blank= True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
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
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.title}' 

        
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        





class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('authors')#, args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name} {self.first_name}'




# class Sauce(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Sandwich(models.Model):
#     name = models.CharField(max_length=100)
#     sauces = models.ManyToManyField(Sauce)

#     def __str__(self):
#         return self.name

# chicken_teriyaki_sandwich = Sandwich.objects.create(name="Chicken Teriyaki Sandwich")
# bbq_sauce = Sauce.objects.create(name="Barbeque")
# bbq_sauce = Sauce.objects.get(name="Barbeque sauce")