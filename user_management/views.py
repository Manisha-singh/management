from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from role_management.models import Role
from user_management.models import UserDetail


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class UserDetailListView(ListView):
    model = UserDetail
    template_name = 'user/list.html'
    context_object_name = 'user_details'

    def get_context_data(self, **kwargs):
        context = super(UserDetailListView, self).get_context_data(**kwargs)
        user_details = self.get_queryset()
        context['user_details'] = user_details
        return context



@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class UserCreateView(View):
    def get(self, request):
        roles = Role.objects.all()
        return render(request, 'user/create.html', {'roles': roles})


    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        role = request.POST['role']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('user-create')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                role = Role.objects.filter(name=role.lower()).first()
                user_details = UserDetail.objects.create(user=user, role=role,
                                                         first_name=first_name, last_name=last_name)
                user_details.save()
                print('user created')
                return redirect('user-list')

        else:
            messages.info(request, 'password not matching..')
            return redirect('user-create')

@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class UserUpdateView(View):
    def post(self, request, pk):
        print(request)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        role = request.POST['role']
        print(first_name)

        role = Role.objects.filter(name=role.lower()).first()
        role.name = role
        user_details = UserDetail.objects.filter(id=pk).first()
        user = user_details.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        user_details.first_name=first_name
        user_details.last_name = last_name
        user_details.role = role
        user_details.save()
        print('user created')
        return redirect("user-list")

    def get(self, request, pk):
        user_detail = UserDetail.objects.filter(id=pk).first()
        return render(request, 'user/update.html', {'user_detail': user_detail})


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class UserDetailDetailView(DetailView):
    model = UserDetail
    template_name = 'user/detail.html'
    context_object_name = 'user_detail'


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='http://localhost:8000/auth/login'),
                  name='dispatch')
class UserDetailDeleteView(DeleteView):
    model = UserDetail
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user-list')
