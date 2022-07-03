from django.urls import path
from .views import Logout, ProjectView, UserCreateView, CourseView, CourseDetailView, ProjectListView, ProjectDetailView, ProjectStartView, ProfileView, LoginView, LogoutView

urlpatterns = [
    path('', ProjectView.as_view(), name='top'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('course/', CourseView.as_view()),
    path('course/<int:pk>', CourseDetailView.as_view()),
    path('project/', ProjectListView.as_view()),
    path('project/<int:pk>', ProjectDetailView.as_view()),
    path('start/', ProjectStartView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
