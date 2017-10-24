from django.shortcuts import render, redirect
from .models import Book, Review
from ..login_reg.models import User

def index(request):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'all_books': Book.objects.all(),
            'recent_reviews': Review.objects.order_by('created_at')[0:3],
            'five': [1,2,3,4,5]
        }
        return render(request,'book_review/index.html', context)
    else:
        return redirect('/')

def new(request):
    return render(request, 'book_review/new.html')

def create_book(request):
    return redirect('/books/add')

def add_review(request):
    return redirect('/books')

def show(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'book_review/book_detail.html', context)