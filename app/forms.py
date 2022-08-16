from dataclasses import field
from django import forms
from .models import Plan, User, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# 新規登録フォーム
class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        labels = {
            'username': "ユーザー名",
            'email': "メールアドレス",
            'password1': "パスワード",
            'password2': "パスワード",
        }

# ログインフォーム
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs['placeholder'] = field.label

# プロフィール編集フォーム
class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'img', 'selfIntro', 'github_url')

        labels = {
            'username': "ユーザー名",
            'email': "メールアドレス",
            'img': "プロフィール画像",
            'selfIntro': "自己紹介",
            'github_url': "GitHub URL",
        }

# プロジェクト作成フォーム
class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ["title", "content", "language_category", "userPlan", "img", "repository_url",]

        widgets = {
            "userPlan": forms.HiddenInput()
        }

        labels = {
            'title': "プロジェクト名*",
            'content': "開発内容*",
            'language_category': "技術スタック*",
            'img': "サムネイル画像",
            'repository_url': "リポジトリURL",
        }

# プロジェクト編集フォーム
class ProjectUpdateForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ["title", "content", "language_category", "userPlan", "img", "repository_url",]

        widgets = {
            "userPlan": forms.HiddenInput()
        }

        labels = {
            'title': "プロジェクト名*",
            'content': "開発内容*",
            'language_category': "技術スタック*",
            'img': "サムネイル画像",
            'repository_url': "リポジトリURL",
        }

# プロジェクトコメントフォーム
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'userComment', 'post',]

        widgets = {
            'text':  forms.Textarea(attrs={'rows':3, 'cols':30}),
            'userComment': forms.HiddenInput(),
            'post': forms.HiddenInput(),
        }

        labels = {
            'text': "",
        }

