# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#     path("", views.RoleView.as_view(), name="role"),
#     path("add", views.RoleView.as_view(), name="role")
# ]

from django.urls import path

from . import views


urlpatterns = [
    path('', views.RoleListView.as_view(),
         name='role-list'),
    path('create', views.RoleCreateView.as_view(),
         name='role-create'),
    path('<int:pk>', views.RoleDetailView.as_view(),
         name='role-detail'),
    path('<int:pk>/update', views.RoleUpdateView.as_view(),
         name='role-update'),
    path('<int:pk>/delete', views.RoleDeleteView.as_view(),
         name='role-delete'),

]
