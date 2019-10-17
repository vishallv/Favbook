from django.shortcuts import render,HttpResponse,redirect
from .models import User,Books
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'app1/index.html')

def registerUser(request):
    if request.method == "POST":
        print(request.POST)
        pw_hash = bcrypt.hashpw(request.POST["pass"].encode(),bcrypt.gensalt())
        
        error = User.objects.basic_validation(request.POST)
        
        if len(error)>0:
            for val in error.values():
                messages.error(request,val)
            return redirect("/")
        else:
            
            store_user = User.objects.create(first_name=request.POST["first_name"],last_name=request.POST["last_name"],
                                             email=request.POST["email"],password=pw_hash)
            request.session['uid']= store_user.id
            print(store_user)
            
            
            return redirect('/books')

def loginUser(request):
    if request.method == "POST":
        # print(request.POST)
        
        user = User.objects.filter(email=request.POST["email"])
        # print(user)
        
        if user:
            log_user = user[0]
            
            if bcrypt.checkpw(request.POST["pass"].encode(),log_user.password.encode()):
                # print(log_user.id)
                request.session['uid']= log_user.id  
                return redirect('/books')
            else:
                val = "Invalid Password"
                messages.error(request,val)
                return redirect('/')
        else:
            val = "Invalid Email"
            messages.error(request,val)
            return redirect('/')

def addBook(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.get(id = request.session['uid'])
        add_book = Books.objects.create(title=request.POST['title'],description=request.POST['description'],uploaded_by= user)
        add_book.users_who_like.add(user)
        return redirect('/books')
    
def books(request):
    print(request.session['uid'])
    user = User.objects.get(id = request.session['uid'])
    print(user)
    allBook = Books.objects.all()
    context = {
        "allBook":allBook,
        "user":user
    }
    return render(request,'app1/book.html',context)

def showBook(request,uid):
    check = True
    ebook = Books.objects.get(id=uid)
    
    if ebook.users_who_like.get(id = request.session['uid']):
        check = False
    
     
    context= {
        "book":ebook,
        "users":ebook.users_who_like.all(),
        "check":check
        
    }
    return render(request,'app1/showbook.html',context)

def editBook(request,uid):
    ebook = Books.objects.get(id=uid)
    context={
        "book":ebook,
        "users":ebook.users_who_like.all()
    }
    return render(request,'app1/editbook.html',context)

def verify(request,uid):
    checkBook = Books.objects.get(id = uid)
    verify = checkBook.uploaded_by.id 
    if verify == (request.session['uid']):
        return redirect(f'/edit/{uid}')
    else:
        return redirect(f'/show/{uid}')

def makeEdit(request,uid):
    if request.method == "POST":
        print(uid)
        print(request.POST)
        book = Books.objects.get(id=uid)
        book.title = request.POST['title']
        book.description = request.POST['description']
        book.save()
        return redirect('/books')
    
def addFavorite(request,uid):
    user = User.objects.get(id = request.session['uid'])
    book = Books.objects.get(id = uid)
    
    book.users_who_like.add(user)
    return redirect('/books')
    
    pass
    
 
    