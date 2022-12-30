from django.urls import path
from . import views

urlpatterns = [
    path('',views.form_page),
    path('register',views.register),
    path('login',views.login),
    path('books_page',views.books_page),
    path('add_book_page',views.add_book_page),
    path('add_book_process',views.add_book_process),
]