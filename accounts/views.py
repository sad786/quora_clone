from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'accounts/login.html'
    
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return redirect('home')