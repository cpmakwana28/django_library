"""
    the below tests run using 
    python manage.py test
    This will discover all files named with the pattern test*.py under the current directory 
    and run all tests defined using appropriate base classes.
    By default the tests will individually report only on test failures, followed by a test summary.

"""

"""
    we should test anything that is part of our design or that is defined by code that we have written,
    but not libraries/code that is already tested by Django or the Python development team.
"""
from django.test import TestCase

from catalog.models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        #Get the authur object to test
        author = Author.objects.get(id=1)
        #Get the metadata for the required field and use it to query the required field data.
        """
             we need to use the author's _meta attribute to get an instance of the field 
             and use that to query for the additional information.    
        """
        field_label = author._meta.get_field('first_name').verbose_name
        #Compare the value to the expected result
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name} {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/authors/')