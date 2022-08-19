from distutils.errors import CompileError
from pyexpat import model
from re import template
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, User, Comment, Plan
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import SignUpForm, LoginForm, ProfileEditForm, ProjectCreateForm, CommentForm, ProjectUpdateForm
from chat.forms import CreateRoomForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class TopPageView(TemplateView):
    template_name = "top.html"

class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("top")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user 
        return HttpResponseRedirect("top")

    def form_valid(self, form):
        messages.success(self.request, "新規アカウントが作成されました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "新規アカウントが作成できませんでした")
        return super().form_invalid(form)

class LoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    model = User

    def form_valid(self, form):
        messages.success(self.request, "ログインしました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ログインできませんでした")
        return super().form_invalid(form)

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'

class CourseView(ListView):
    template_name = 'courses/course.html'
    model = Course

class CourseDetailView(DetailView):
    template_name = 'courses/courseDetail.html'
    model = Course

class ProjectListView(ListView):
    template_name = 'projects/projectList.html'
    model = Plan
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Plan.objects.all()
        keyword = self.request.GET.get("q")

        if keyword:
            qs = qs.filter(title__contains=keyword)

        return qs

# プロジェクト詳細ページ
class ProjectDetailView(DetailView):
    template_name = 'projects/projectDetail.html'
    model = Plan

    # コメント投稿時のプロジェクトの指定
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CommentForm'] = CommentForm(initial={'post': self.object})
        return context

    # ルーム作成時の実装
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CreateRoomForm'] = CreateRoomForm(initial={'plan': self.object})
        return context

class ProfileUpdateView(UpdateView):
    form_class = ProfileEditForm
    template_name = 'accounts/profile.html'
    model = User
    success_url = reverse_lazy('top')

    def form_valid(self, form):
        messages.success(self.request, "プロフィールを更新しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "プロフィールが更新できませんでした")
        return super().form_invalid(form)

class ProjectStartView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'projects/project.html'
    model = Plan
    success_url = reverse_lazy('projectlist')

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.POST.dict()
        data['userPlan'] = user.id
        form = ProjectCreateForm(data=data, files=request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "プロジェクトを作成しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "プロジェクトを作成できませんでした")
        return super().form_invalid(form)

# プロフィール削除
class AccountDeleteView(DeleteView):
    template_name = 'accounts/account.html'
    model = User
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# アカウント表示
class AccountView(ListView):
    template_name = 'accounts/account.html'
    model = User

# アカウント削除
class AccountDeleteView(DeleteView):
    template_name = 'accounts/accountDelete.html'
    model = User
    success_url = reverse_lazy('top')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "アカウントを削除しました")
        return super().delete(request, *args, **kwargs)

# パスワード変更
class AccountPasswordView(UpdateView):
    template_name = 'accounts/account.html'
    model = User

# プロジェクト管理
class ProjectAdminView(ListView):
    template_name = 'projects/project-admin.html'
    model = Plan

# ユーザーのプロジェクトダッシュボード表示
class ProjectAdminView(TemplateView):
    template_name = "projects/project-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            context['projects_list'] = Plan.objects.filter(userPlan=self.request.user)
        else:
            context['projects_list'] = None

        return context

# プロジェクトの編集
class ProjectUpdateView(UpdateView):
    template_name = 'projects/projectUpdate.html'
    model = Plan
    form_class = ProjectUpdateForm
    success_url = reverse_lazy('projectadmin')

# プロジェクトの削除
class ProjectDeleteView(DeleteView):
    template_name = 'projects/projectDelete.html'
    model = Plan
    success_url = reverse_lazy("projectadmin")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "プロジェクトを削除しました")
        return super().delete(request, *args, **kwargs)


# コメント投稿
class CreateCommentView(CreateView):
    form_class = CommentForm
    template_name = 'projects/projectDetail.html'
    model = Comment
    success_url = reverse_lazy('projectlist')

    # プロジェクトの指定
    def comment_create(request):
        # どの投稿かのフィールドを指定
        post_id = request.POST.get("post")
        text = request.POST.get("text")
        data = {"text": text, "post": post_id}
        form = CommentForm(data=data)

        if form.is_valid():
            form.save()
            messages.success(request, "コメントを投稿しました")
        else:
            messages.error(request, "コメントが投稿できませんでした")

        return redirect("project")

    # ユーザーの指定
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.POST.dict()
        data['userComment'] = user.id
        form = CommentForm(data=data)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_url_success(self):
        return reverse_lazy("project",kwargs={"pk":self.kwargs["pk"]})