from django.urls import path
from . import views

urlpatterns = [
    path('',views.form_page),
    path('register',views.register),
    path('login',views.login),
    path('books_page',views.books_page),
    path('add_book_page',views.add_book_page),
    path('add_book_process',views.add_book_process),
    path('book_info_page/<int:BookId>',views.book_info_page),
    path('add_review_from_user/<Book_Title>',views.add_review_from_user),
    path('get_user_info/<int:UserId>',views.get_user_info),
    path('log_out',views.log_out),
]