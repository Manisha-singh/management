from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from role_management.models import Role
from user_management.models import UserDetail


class UserRegisterView(View):
    def get(self, request):
        roles = Role.objects.all()
        return render(request, 'register.html', {'roles': roles})

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
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                role = Role.objects.filter(name=role.lower()).first()
                user_details = UserDetail.objects.create(user=user, role=role,
                                                         first_name=first_name, last_name=last_name)
                user_details.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'password not matching..')
            return redirect('register')


class UserLoninView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
class UserLogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')


@method_decorator(login_required(login_url="http://localhost:8000/auth/login"), name='dispatch')
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
