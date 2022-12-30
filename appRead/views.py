from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *

def form_page(request):
    return render(request,'index.html')


def register(request):
    print("***** 1 ")
    error = User.objects.basic_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        if request.method == "POST":
            print("***** 3 ")
            Register(request)
            print("***** 4 ")
        return redirect('/')

def login(request):
    if Login(request):
        return redirect('/books_page')
    
# view books reviewer page
def books_page(request):
    id = request.session['userid']
    user = User.objects.get(id = id)
    books = Get_Books(request)
    # for book in books:
    #     print(book.book_title)

    context = {
        "user" : user , 
        "books" : books ,
    }
    return render(request,'booksPage.html',context)

# view add book page
def add_book_page(request):
    id = request.session['userid']
    user = User.objects.get(id = id)
    authors = Get_Authors(request)
    context = {
        "user" : user , 
        "authors" : authors ,
    }
    return render(request,'add_book.html',context)

# add book process
def add_book_process(request):
    error =Book.objects.book_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/add_book_page')
    else:
        id = request.session['userid']
        book_title = request.POST['book_title']
        rating = request.POST['rating']
        author_from_database = request.POST['author_from_database']
        author_from_user = request.POST['author_from_user']
        review = request.POST['review']
        if len(author_from_user) > 0 :
            author =  author_from_user
        else:
            author = author_from_database
        
        Add_Author(author)
        Add_Book(book_title,author)
        Add_Review(review,rating,id,book_title)
    
    return redirect('/')


