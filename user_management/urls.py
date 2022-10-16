from django.urls import path

from . import views

urlpatterns = [

    path('', views.UserDetailListView.as_view(),
         name='user-list'),
    path('create', views.UserCreateView.as_view(),
         name='user-create'),
    path('<int:pk>', views.UserDetailDetailView.as_view(),
         name='user-detail'),
    path('<int:pk>/delete', views.UserDetailDeleteView.as_view(),
         name='user-delete'),
    path('<int:pk>/update', views.UserUpdateView.as_view(),
         name='user-update'),

]
