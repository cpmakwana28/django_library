from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    Years_choices = ['2021']
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")#,initial=datetime.date.today(),widget=forms.SelectDateWidget(years=Years_choices))
    #field name 

    def clean_renewal_date(self):
        """
            Django provides numerous places where you can validate your data.
            The easiest way to validate a single field is to override the method clean_<fieldname>() for the field you want to check.
        """
        #clean_fieldname() : use to validate the text entered from <fieldname>.
        #we access our data using below code
        data=self.cleaned_data['renewal_date']

        #check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #check if a date is in the allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks = 4):
            raise ValidationError(_('Invalid date - renewal is more than 4 weeks ahead'))

        #Remember to always return the cleaned data
        return data

from django.forms import ModelForm

from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    """
        Creating a Form class using the approach described above is very flexible, 
        allowing you to create whatever sort of form page you like and associate it with any model or models.
    """
    
    def clean_due_back(self):
        """
            To add validation ,you define a function named clean_field_name() 
            and raise ValidationError exceptions for invalid values.
            The only difference with respect to our original form is that the model field is named due_back and not "renewal_date". 
            This change is necessary since the corresponding field in BookInstance is called due_back. 
        """
        data = self.cleaned_data['due_back']
        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
            
        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        # Remember to always return the cleaned data.
        return data


    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}