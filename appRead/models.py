import re
from django.db import models 
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        error = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex =re.compile(r'^[a-zA-Z0-9.+_-]')
        special_symbols = ['$','@','#','%','^','&']
        if len(postData['first_name']) < 3 :
            error['first_name'] = "first name should be at least 3 characters"
        if len(postData['last_name']) < 3 :
            error['last_name'] = "last name should be at least 3 characters"
        if not email_regex.match(postData['email']) :
            error['email'] = "invaild email"
        if len(postData['password']) < 6:
            error['password_less_than'] = "Password must have atleast 6 characters"
        if len(postData['password']) > 20 :
            error['password_grather_than'] = "'Password cannot have more than 20 characters"
        if not any(characters.isupper() for characters in postData['password']):
            error['password_notInclude_upper'] = "Password must have at least one uppercase character"
        if not any(characters.islower() for characters in postData['password']):
            error['password_notInclude_lower'] = "Password must have at least one lowercase character"
        if not any(characters.isdigit() for characters in postData['password']):
            error['password_notInclude_number'] = "Password must have at least one numeric character."
        if not any(characters in special_symbols for characters in postData['password']):
            error['password_symbol'] = "Password should have at least one of the symbols $@#%^&"
        return error

    def book_validator(self, postData):
        error = {}
        if len(postData['book_title']) <3:
            error['book_title'] = "book title should be at least 3 characters"
        if (len(postData['author_from_database']) == 0 ) and (len(postData['author_from_user']) == 0) :
            error['not_fill_author'] = "please select or insert author name"
        if (len(postData['author_from_database']) > 0 ) and (len(postData['author_from_user']) > 0) :
            error['dople_auther'] = "pleaser choose one author"
        if len(postData['review']) < 3 :
            error['review'] = "please insert your opinion in this book"
        return error
        
# create user table
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # reviews = list of user reviews on books
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # my_books = list of author book

# create book table 
class Book(models.Model):
    book_title = models.CharField(max_length=255)
    author = models.ForeignKey(Author , related_name="my_books" , on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # reviews = list of reviews on thid book


class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User , related_name="reviews" , on_delete=models.CASCADE)
    book = models.ForeignKey(Book , related_name="reviews" , on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


# register new user
def Register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
    if (request.POST['confirm_password'] == password):
        return User.objects.create(first_name = first_name , last_name = last_name, email = email , password = pw_hash )

# login current user
def Login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        loged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), loged_user.password.encode()):
            # request.session['userid'] = loged_user.id
            return loged_user.id
    else:
        return None

# add author
def Add_Author(name):
    return Author.objects.create(name= name)

# add book
def Add_Book(book_title,author_name):
    author = Author.objects.filter( name = author_name)
    return Book.objects.create(book_title = book_title , author = author[0])

# add review
def Add_Review(content,rating,user_id,book_title):
    book = Book.objects.filter( book_title = book_title)
    user = User.objects.get(id = user_id)
    return Review.objects.create(content = content , rating = rating , user = user , book=book[0])

# get all authors
def Get_Authors(request):
    return Author.objects.all()

# get all books
def Get_Books(request):
    return Book.objects.all().order_by('book_title')

# get specific book info
def Get_book_info(BookId):
    print("*********** 1",BookId)
    book = Book.objects.get(id = BookId)
    print("*********** 2", book)
    return book

# get user data
def Get_User(UserId):
    return User.objects.get(id = UserId)

# get number of reviews for user 
def Get_number_of_Reviews_for_user(UserId):
    count = 0
    reviews = Review.objects.filter( user = UserId)
    for one in reviews :
        count += 1
        print("$$$ " ,count)

    return count
   

