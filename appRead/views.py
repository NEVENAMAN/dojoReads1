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
    userId =  Login(request)
    print(userId)
    if userId!=None:
        request.session['userid'] = userId
        print("login : ",request.session['userid'])
        return redirect('/books_page')
    else:
        print('not Logged In')
        return redirect('/')
    
# view books reviewer page
def books_page(request):
    if 'userid' in request.session:
        id = request.session['userid']
        user = User.objects.get(id = id)
        books = Get_Books(request)
        
        newList = []
        for book in books:
            newBook = {
                'book_title': book.book_title,
                'author': book.author,
                'id' : book.id,
                'reviews': [],
            }
            print("2 ",newBook['reviews'])
            
            reviews = book.reviews.all()
            if len(reviews) > 0:
                review = reviews[0]
            # for review in book.reviews.all():
                yellow_stars = []
                grey_stars = []
                for i in range(review.rating):
                    yellow_stars.append(i)
                for i in range(5-review.rating):
                    grey_stars.append(i)
                

                newBook['reviews'].append({
                    'content': review.content,
                    'yellow_stars': yellow_stars,
                    'grey_stars':grey_stars,
                    'user': review.user,
                    'book': review.book,
                    'created_at': review.created_at
                })
            newList.append(newBook)  
        context = {
            "user" : user , 
            "books" : newList ,
        }
        return render(request,'booksPage.html',context)
    else:
        return redirect('/')
      

# view add book page
def add_book_page(request):
    if 'userid' in request.session:
        id = request.session['userid']
        user = User.objects.get(id = id)
        authors = Get_Authors(request)
        for a in authors:
            print("11 " , a.name )
        context = {
            "user" : user , 
            "authors" : authors ,
        }
        return render(request,'add_book.html',context)
    else:
        return redirect('/')
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
    
    return redirect('/books_page')
    

# get specific book info
def book_info_page(request,BookId):
    if 'userid' in request.session:
        id = request.session['userid']
        user = User.objects.get(id = id)
        book = Get_book_info(BookId)
        
        newBook = {
            'book_title': book.book_title,
            'author': book.author,
            'id' : book.id,
            'reviews': []
        }
        for review in book.reviews.all():
            # print("### " , review.rating)
            yellow_stars = []
            grey_stars = []
            for i in range(review.rating):
                yellow_stars.append(i)
            for i in range(5-review.rating):
                grey_stars.append(i)

            newBook['reviews'].append({ 
                'content': review.content,
                'yellow_stars': yellow_stars,
                'grey_stars':grey_stars,
                'user': review.user,
                'book': review.book,
                'rating' : review.rating,
                'created_at': review.created_at,
            })

        context = {
            "user" : user ,
            "book" : newBook ,
        }
        return render(request,'book_info_page.html',context)
    else:
        return redirect('/')

# add review on this book
def add_review_from_user(request,Book_Title):
    user_id = request.session['userid']
    content = request.POST['content']
    rating = request.POST['rating']
    book = Book.objects.filter(book_title = Book_Title)
    print("@@@@@@ " ,book[0])
    print("@@@@@@ " ,book[0].id)
    print("@@@@@@ " ,book[0].book_title)
    BookId = book[0].id
    Add_Review(content,rating,user_id,Book_Title)
    return redirect('/book_info_page/'+str(BookId))
   


# get user data from database
def get_user_info(request,UserId):
    if 'userid' in request.session:
        user = Get_User(UserId)
        num_of_reviews = Get_number_of_Reviews_for_user(UserId)
        print("num = " , num_of_reviews)
        context = {
            "user" : user ,
            "num_of_reviews" : num_of_reviews,
        }
        return render(request,'user_profile.html',context)
    else:
        return redirect('/')  
    
# logout method
def log_out(request):
    request.session.flush()
    return redirect('/')