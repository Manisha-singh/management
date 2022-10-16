from django.urls import path

from . import views


urlpatterns = [
    path('book', views.BookListView.as_view(),
         name='book-list'),
    path('book/create', views.BookCreateView.as_view(),
         name='book-create'),
    path('book/<int:pk>', views.BookDetailView.as_view(),
         name='book-detail'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(),
         name='book-update'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(),
         name='book-delete'),
    path('book/issued', views.IssuedBookListView.as_view(),
         name='book-issued'),
    path('book/<int:bookId>/assign', views.assign,
         name='assign'),
    path('book/<int:bookId>/returned', views.returned,
         name='returned'),
]
