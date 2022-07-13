from dataclasses import field
from re import template
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Project, Course, User
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import SignUpForm, LoginForm

class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "signup.html" 
    success_url = reverse_lazy("/")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user 
        return HttpResponseRedirect("/")

class LoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"
    model = User

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'login.html'

class ProjectView(ListView):
    template_name = 'top.html'
    model = Project

class CourseView(ListView):
    template_name = 'course.html'
    model = Course

class CourseDetailView(DetailView):
    template_name = 'courseDetail.html'
    model = Course

class ProjectListView(ListView):
    template_name = 'projectList.html'
    model = Project

class ProjectDetailView(DetailView):
    template_name = 'projectDetail.html'
    model = Project

class ProjectStartView(CreateView):
    template_name = 'project.html'
    fields = ('title', 'subtitle', 'img', 'liked')
    model = Project
    success_url = reverse_lazy('/')

class ProfileCreateView(CreateView):
    template_name = 'profile.html'
    fields = ('nickName', 'selfIntro', 'github_url', 'img')
    model = Profile

class AccountView(ListView):
    template_name = 'account.html'
    model = User

class AccountDeleteView(DeleteView):
    template_name = 'account.html'
    model = User

class AccountPasswordView(UpdateView):
    template_name = 'account.html'
    model = User

