
from django.contrib import admin
from django.urls import path,include
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('books/<int:pk>',views.BookDetailView.as_view(),name='book-detail')
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

"""
    You can see that the views are classes, and must hence be called via .as_view().
"""
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
        path('authors/',views.AuthorListView.as_view(),name='authors')
]