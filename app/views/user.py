from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from ..forms import SignUpForm, LoginForm, ProfileEditForm
from django.contrib import messages

class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("app:top")

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

class ProfileUpdateView(UpdateView):
    form_class = ProfileEditForm
    template_name = 'accounts/profile.html'
    model = User
    success_url = reverse_lazy('app:top')

    def form_valid(self, form):
        messages.success(self.request, "プロフィールを更新しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "プロフィールが更新できませんでした")
        return super().form_invalid(form)

# プロフィール削除
class AccountDeleteView(DeleteView):
    template_name = 'accounts/account.html'
    model = User
    success_url = reverse_lazy('app:top')
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
    success_url = reverse_lazy('app:top')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "アカウントを削除しました")
        return super().delete(request, *args, **kwargs)

# パスワード変更
class AccountPasswordView(UpdateView):
    template_name = 'accounts/account.html'
    model = User
