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
            'ids_authors_list': Book.objects.values('author').distinct()
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
            if len(request.POST['author_new']) > 1:
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
    if request.method == 'POST':
        book = Book.objects.get(id=request.POST['book'])
        book_url = '/books/' + str(book.id)
        errors = Review.objects.validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            user = User.objects.get(id=request.session['user_id'])
            Review.objects.create(text=request.POST['review_text'], rating=int(request.POST['rating']), writer=user, book=book)
        return redirect(book_url)
    else:
        return redirect('/books')

def show(request, book_id):
    if 'user_id' in request.session:
        book = Book.objects.get(id=book_id)
        context = {
            'book': book,
            'all_reviews': book.reviews.all().order_by('-created_at'),
            'five': [1,2,3,4,5]
        }
        return render(request, 'book_review/book_detail.html', context)
    else:
        return redirect('/')

def delete_review(request, review_id):
    if request.method == 'POST':
        url = request.POST['goback']
        review = Review.objects.get(id=review_id)
        if request.session['user_id'] == review.writer.id:
            review.delete()
        else:
            print "Naughty hacker trying to delete someone elses reviews!!"
        return redirect(url)
    else:
        return redirect('/books')