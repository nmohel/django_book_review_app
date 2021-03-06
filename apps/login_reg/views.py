from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'login_reg/index.html')

def show(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user,
        'total_reviews': user.reviews.count(),
        'books': User.objects.raw("SELECT DISTINCT book_review_book.id, book_review_book.title FROM login_reg_user JOIN book_review_review ON book_review_review.writer_id = login_reg_user.id JOIN book_review_book ON book_review_book.id = book_review_review.book_id WHERE login_reg_user.id = " + str(user_id))
    }
    return render(request, 'login_reg/user_detail.html', context)

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            request.session['user_id'] = User.objects.get(email=request.POST['email']).id
            return redirect('/books')
        
    return redirect('/')

def create(request):
    if request.method == 'POST':
        errors = User.objects.register_validatior(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            User.objects.create(
                name=request.POST['name'], 
                alias=request.POST['alias'], 
                email=request.POST['email'],
                password= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                )
            request.session['user_id'] = User.objects.get(email=request.POST['email']).id
            return redirect('/books')
    
    return redirect('/')

def logout(request):
    request.session.pop('user_id')
    return redirect('/')


