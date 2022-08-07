from distutils.errors import CompileError
from pyexpat import model
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, Course, User, Comment, Plan
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import SignUpForm, LoginForm, ProfileEditForm, ProjectCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("/")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user 
        return HttpResponseRedirect("/")

class LoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    model = User

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/login.html'

class ProjectView(ListView):
    template_name = 'top.html'
    model = Project

class CourseView(ListView):
    template_name = 'courses/course.html'
    model = Course

class CourseDetailView(DetailView):
    template_name = 'courses/courseDetail.html'
    model = Course

# プロジェクト一覧ページ
class ProjectListView(ListView):
    template_name = 'projects/projectList.html'
    model = Plan
    ordering = ['-created_at']

# プロジェクト詳細ページ
class ProjectDetailView(DetailView):
    template_name = 'projects/projectDetail.html'
    model = Plan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CommentForm'] = CommentForm(initial={'post': self.object})
        return context

# プロフィール編集
class ProfileUpdateView(UpdateView):
    form_class = ProfileEditForm
    template_name = 'accounts/profile.html'
    model = User
    success_url = reverse_lazy('top')

# プロジェクト作成
class ProjectStartView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'projects/project.html'
    model = Plan
    success_url = reverse_lazy('top')

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.POST.dict()
        data['userPlan'] = user.id
        form = ProjectCreateForm(data=data, files=request.FILES)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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
    template_name = 'accounts/account.html'
    model = User

# パスワード変更
class AccountPasswordView(UpdateView):
    template_name = 'accounts/account.html'
    model = User

# プロジェクト管理
class ProjectAdminView(ListView):
    template_name = 'projects/project-admin.html'
    model = Plan

# ユーザーのプロジェクト管理
class ProjectAdminView(ListView):
    template_name = "projects/project-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['recipe_list'] = Plan.objects.filter(user=self.request.user)
        else:
            context['recipe_list'] = None


        return context

# プロジェクトの編集
class PlanUpdateView(UpdateView):
    model = Plan
    # formを持ってくる
    form_class = ProjectCreateForm

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        # プロジェクト管理のapp name
        return reverse("", kwargs={"pk": pk})

    def form_valid(self, form):
        messages.success(self.request, "更新しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした")
        return super().form_invalid(form)

# プロジェクトの削除
class PlanDeleteView(DeleteView):
    model = Plan
    # プロジェクト管理のapp name
    success_url = reverse_lazy("")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "削除しました")
        return super().delete(request, *args, **kwargs)


# コメント投稿
class CreateCommentView(CreateView):
    form_class = CommentForm
    template_name = 'projects/projectDetail.html'
    model = Comment
    success_url = reverse_lazy('projectlist')

    def comment_create(request):
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



# def comment_create(request):
#     user = request.user
#     post_id = request.POST.get("post")
#     text = request.POST.get("text")
#     user.id = request.POST.get("userComment")

#     data = {"text": text, "post": post_id, "userComment": user.id}

#     form = CommentForm(data=data)
#     if form.is_valid():
#         form.save()
#         messages.success(request, "コメントを投稿しました。")
#     else:
#         messages.error(request, "コメントが投稿できませんでした")

#     return redirect("project", pk=post_id)