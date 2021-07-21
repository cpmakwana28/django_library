from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required

import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm



@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genre=Genre.objects.all().count()


    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_visits=request.session.get('num_visits', 0) #access the session id of current user (or current browser)  and use it to access or change the number of visits. 
    # session_id=request.session._get_session()
    request.session['num_visits'] = num_visits + 1
    # request.session.set_expiry(10)
    # session_id=request.session.get_expiry_age()
    expiry_date=request.session.get_expiry_date()
    # type_expiry=str(type(expiry_date))
    # session_db=request.session._get_session_key()
    # session_key=request.session._get_new_session_key()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre':num_genre,
        'num_visits':num_visits,
        # 'session_id':session_id,
        'expiry_date': expiry_date,
        # 'type_expiry':type_expiry,
        # 'session_db':session_db,
        # 'session_key':session_key,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView( LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'book_list.html'  # Specify your own template name/location
    paginate_by = 2 #to support pagination
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model=Book

    template_name='book_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model=BookInstance
    template_name='bookinstance_list_borrowed_user.html'
    paginate_by= 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back') 

    # a=get_queryset()
    # book_instance=get_query()



@login_required
@permission_required('catalog.can_mark_returned',raise_exception=True)
def renew_book_librarian(request, pk):
    #get the particular pk bookinstance from BookInstance class
    book_instance = get_object_or_404(BookInstance, pk=pk)

    """
        Here the idea of POST and GET is like-
        let say there is a one template rendered in a browser which contain form ,
        and that form has a action attribute points to current view function's url 
        THEN the POST method is activated.
        and if the current view function's url gets pointed by some other webpage 
        THEN GET method is activated.   
    """
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        """
            Here the request is an instance of 'django.http.request.HTTPRequest' class
            So in this case .method is an attribute - HTTPRequest.method which contains the string repersenting the HTTP method used in request.
            This is gauranteed to be uppercase.
        """

        # Create a form instance and populate it with data from the request which is called (binding):
        """
            A dictionary-like object containing all given HTTP POST parameters,
            providing that the request contains form data.
            It’s possible that a request can come in via POST with an empty POST dictionary – 
            if, say, a form is requested via the POST HTTP method but does not include form data. 
            Therefore, you shouldn’t use if request.POST to check for use of the POST method; instead, use if request.method ==POST.
        """
        form = RenewBookForm(request.POST)

        """
            Below if the form is not valid ,render() will be call again,
            but this time the form value passed in the context will error messages.
        """
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            """
                Below HttpResponseRedirect(redirect_to) is a class of django.http and 
                django.urls.reverse :- 
                                SIGNATURE:
                                        viewname,
                                        urlconf=None,
                                        args=None,
                                        kwargs=None,
                                        current_app=None
                                
                                
                                HOW OTHERS USED THIS:
                                        reverse(​viewname​)
                                        reverse(​viewname, args​)
                                        reverse(​viewname, kwargs={'pk': 1}​)
            
            """
            return HttpResponseRedirect(reverse('my-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})



    context = {
        'form': form,
        'book_instance': book_instance,
    }

    """
        Here the form is passes to the html , to get render on website
    """
    return render(request, 'book_renew_librarian.html', context)




from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author
"""
    django use generic editing views for creating, editing, and deleting views based on models.
    ,not only do these handle the "view" behavior,
    but they automatically create the form class (a ModelForm) for you from the model.
"""
class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

