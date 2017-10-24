from django.shortcuts import render, redirect
from .models import Book, Review
from ..login_reg.models import User
from django.contrib import messages

def index(request):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'all_books': Book.objects.all(),
            'recent_reviews': Review.objects.order_by('-created_at')[0:3],
            'five': [1,2,3,4,5]
        }
        return render(request,'book_review/index.html', context)
    else:
        return redirect('/')

def new(request):
    if 'user_id' in request.session:
        context = {
            'ids_authors_list': Book.objects.raw("SELECT DISTINCT book_review_book.id, book_review_book.author FROM book_review_book")
        }
        return render(request, 'book_review/new.html', context)
    else:
        return redirect('/')

def create_book(request):
    if request.method == 'POST':
        errors = Book.objects.validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            if request.POST['author_new'] > 1:
                author = request.POST['author_new']
            else:
                author = request.POST['author_list']

            user = User.objects.get(id = request.session['user_id'])
            book = Book.objects.create(title=request.POST['title'], author=author)
            review = Review.objects.create(text=request.POST['review_text'], rating=int(request.POST['rating']), writer=user, book=book)
            book_url = '/books/' + str(book.id)
            return redirect(book_url)
    
    return redirect('/books/add')

def add_review(request):
    return redirect('/books')

def show(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'book_review/book_detail.html', context)