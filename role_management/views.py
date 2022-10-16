from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from .models import Role


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
class RoleListView(ListView):

    model = Role
    template_name = 'role/list.html'
    context_object_name = 'roles'

    def get_context_data(self, **kwargs):
        context = super(RoleListView, self).get_context_data(**kwargs)
        roles = self.get_queryset()
        context['roles'] = roles
        return context


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'), name='dispatch')
class RoleCreateView(CreateView):
    model = Role
    template_name = 'role/create.html'
    fields = ('name',)
    success_url = reverse_lazy('role-list')


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
class RoleDetailView(DetailView):

    model = Role
    template_name = 'role/detail.html'
    context_object_name = 'role'


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'), name='dispatch')
class RoleUpdateView(UpdateView):

    model = Role
    template_name = 'role/update.html'
    context_object_name = 'roles'
    fields = ('name', )

    def get_success_url(self):
        return reverse_lazy('role-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"),  name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'), name='dispatch')
class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'role/delete.html'
    success_url = reverse_lazy('role-list')

