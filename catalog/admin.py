from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance

#admin.site.register(Book)

class BookInstanceInline(admin.TabularInline):
    model=BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre') 
    list_filter = ("author",)
    inlines=[BookInstanceInline]




class BookInline(admin.TabularInline):
    model=Book
    extra = 0

#admin.site.register(Author)

"""Define the admin class"""
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines=[BookInline]

admin.site.register(Author,AuthorAdmin)
"""Register the admin class with the associated model
"""





admin.site.register(Genre)







#admin.site.register(BookInstance)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=("book","status","borrower","due_back","id")
    list_filter=("status","due_back")
    fieldsets = (
    (None, {
        'fields': ('book', 'imprint', 'id')
    }),
    ('Availability', {
        'fields': ('status', 'due_back','borrower')
    }),
)


