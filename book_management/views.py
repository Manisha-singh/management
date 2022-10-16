import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from user_management.models import UserDetail
from .models import Book, Issue


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'book/list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        user_detail = UserDetail.objects.filter(user_id=user_id).first()
        if self.request.user.is_superuser or user_detail.role.name == 'student':
            context = super(BookListView, self).get_context_data(**kwargs)
            books = self.get_queryset().filter(issued_status=False)
            context['books'] = books
            return context
        else:
            return


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class BookCreateView(CreateView):
    model = Book
    template_name = 'book/create.html'
    fields = ('name', 'author', 'book_number')
    success_url = reverse_lazy('book-list')


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
class BookDetailView(DetailView):
    model = Book
    template_name = 'book/detail.html'
    context_object_name = 'book'


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    template_name = 'book/update.html'
    context_object_name = 'book'
    fields = ('name', 'author', 'book_number')

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book/delete.html'
    success_url = reverse_lazy('book-list')

@login_required(login_url="http://localhost:8000/auth/login")
def assign(request, bookId):
    user_id = request.user.id
    user_detail = UserDetail.objects.filter(user_id=user_id).first()
    book = Book.objects.filter(id=bookId).first()
    if request.user.is_superuser:
        messages.info(request, 'You are Not a Student !')
        return redirect('book-list')
    elif user_detail.role.name == 'student':
        tomorrow = datetime.datetime.now() + datetime.timedelta(1)
        today = datetime.datetime.now()
        issue = Issue.objects.create(user_detail=user_detail, book=book, issued=True,
                                     return_date=tomorrow, issued_at=today, created_at=today)
        issue.save()
        messages.info(request, 'Book - {} Requested succesfully '.format(book.name))
        book.issued_status = True
        book.save()
        return redirect('book-list')
    else:
        messages.info(request, 'You are Not a Student !')


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
class IssuedBookListView(ListView):
    model = Issue
    template_name = 'issue/list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        user_detail = UserDetail.objects.filter(user_id=user_id).first()
        if self.request.user.is_superuser or user_detail.role.name == 'student':
            context = super(IssuedBookListView, self).get_context_data(**kwargs)
            issued_books = self.get_queryset().filter(user_detail=user_detail).filter(returned=False).all()
            context['books'] = issued_books
            for book in issued_books:
                status = book.days_no()
                if status == 'passed':
                    messages.info(self.request, "Please Submit the book {}".format(book.book.name))
            return context
        else:
            return


def returned(request, bookId):
    user_id = request.user.id
    user_detail = UserDetail.objects.filter(user_id=user_id).first()
    book = Book.objects.filter(id=bookId).first()
    issue_book = Issue.objects.filter(user_detail=user_detail).filter(book=book).filter(returned=False).first()
    issue_book.returned = True
    issue_book.book.issued_status = False
    issue_book.save()
    book.issued_status = False
    book.save()
    messages.success(request, 'Book - {} Returned succesfully '.format(book.name))
    return render(request, 'issue/return.html')
