from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.


def index(request):
    return render(request, 'store/index.html')


def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    thisBook = Book.objects.get(id=bid)
    context = {
        # set this to an instance of the required book
        'book': Book.objects.get(id=bid),
        # set this to the number of copies of the book available, or 0 if the book isn't available
        'num_available': BookCopy.objects.filter(book=thisBook, status=True).count(),
    }
    # START YOUR CODE HERE

    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    filteredBooks = Book.objects.all()
    if(request.GET != {}):
        title = request.GET['title']
        author = request.GET['author']
        genre = request.GET['genre']
        # print(title, author, genre)
        if(title):
            print(f"Title={title}")
        filteredBooks = Book.objects.filter(
            title__contains=title, author__contains=author, genre__contains=genre)

    context = {
        # set this to an instance of the requiredlist of required books upon filtering using the GET parameters
        'books': filteredBooks,
        # (i.e. the book search feature will also be implemented in this view)
    }
    # START YOUR CODE HERE

    return render(request, template_name, context=context)


@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'

    userBooks = BookCopy.objects.filter(borrower=request.user)

    context = {
        'books': userBooks,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE

    return render(request, template_name, context=context)


@csrf_exempt
@login_required
def loanBookView(request):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")

    book_id = request.POST['bid']
    book = Book.objects.get(id=book_id)
    availableCopy = BookCopy.objects.filter(status=True, book=book).first()
    availableCopy.status = False
    availableCopy.borrower = request.user
    availableCopy.borrow_date = date
    availableCopy.save()
    response_data = {
        'message': 'Success',
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    # get the book id from post data

    return JsonResponse(response_data)


'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
'''


@csrf_exempt
@login_required
def returnBookView(request):

    copy_id = request.POST['book_id']
    BookCopy.objects.filter(id=copy_id).update(
        status=True, borrower=None, borrow_date=None)
    response_data = {
        'message': 'Success',
    }
    messages.success(request, "Book returned successfully")
    return JsonResponse(response_data)
