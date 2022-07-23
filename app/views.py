from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Project, Course, User, Comment, Plan
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import SignUpForm, LoginForm, ProfileEditForm, ProjectCreateForm
from django.contrib.auth.decorators import login_required

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

# プロジェクトページ
class ProjectListView(ListView):
    template_name = 'projectList.html'
    model = Plan

class ProjectDetailView(DetailView):
    template_name = 'projectDetail.html'
    model = Plan

# プロフィール編集
class ProfileUpdateView(UpdateView):
    form_class = ProfileEditForm
    template_name = 'profile.html'
    model = User
    success_url = reverse_lazy('top')

# プロジェクト作成
class ProjectStartView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'project.html'
    model = Plan
    success_url = reverse_lazy('top')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# プロフィール削除
class AccountDeleteView(DeleteView):
    template_name = 'account.html'
    model = User
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class AccountView(ListView):
    template_name = 'account.html'
    model = User

class AccountDeleteView(DeleteView):
    template_name = 'account.html'
    model = User

class AccountPasswordView(UpdateView):
    template_name = 'account.html'
    model = User

class CommentView(CreateView):
    template_name = 'projectDetail.html'
    model = Comment

