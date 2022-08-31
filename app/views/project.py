from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Comment, Plan
from django.urls import reverse, reverse_lazy
from ..forms import ProjectCreateForm, CommentForm, ProjectUpdateForm
from chat.forms import CreateRoomForm
from django.contrib import messages
from django.views.generic import TemplateView

class TopPageView(TemplateView):
    template_name = "top.html"

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

class ProjectStartView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'projects/project.html'
    model = Plan
    success_url = reverse_lazy('app:projectlist')

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
    success_url = reverse_lazy('app:projectadmin')

# プロジェクトの削除
class ProjectDeleteView(DeleteView):
    template_name = 'projects/projectDelete.html'
    model = Plan
    success_url = reverse_lazy("app:projectadmin")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "プロジェクトを削除しました")
        return super().delete(request, *args, **kwargs)

# コメント投稿
class CreateCommentView(CreateView):
    form_class = CommentForm
    template_name = 'projects/projectDetail.html'
    model = Comment
    success_url = reverse_lazy('app:projectlist')

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
        return reverse_lazy("app:project",kwargs={"pk":self.kwargs["pk"]})