from django.urls import path
from .views.user import UserCreateView, ProfileUpdateView, LoginView, LogoutView, AccountView, AccountDeleteView, AccountPasswordView
from .views.course import CourseView, CourseDetailView
from .views.project import ProjectListView, ProjectDetailView, ProjectStartView, ProjectAdminView,  CreateCommentView, ProjectUpdateView, ProjectDeleteView, TopPageView

app_name = "app"

urlpatterns = [
    path('', TopPageView.as_view(), name='top'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('course/', CourseView.as_view(), name='courselist'),
    path('course/<int:pk>', CourseDetailView.as_view(), name="course"),
    path('project/', ProjectListView.as_view(), name='projectlist'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name="project"),
    path('readyfor/', ProjectStartView.as_view(), name='readyfor'),
    path('profile/<int:pk>', ProfileUpdateView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('account/delete/<int:pk>', AccountDeleteView.as_view(), name='accountDelete'),
    path('account/password/<int:pk>', AccountPasswordView.as_view(), name='accountPassword'),
    path('project-dashboard/', ProjectAdminView.as_view(), name='projectadmin'),
    path('comment/', CreateCommentView.as_view(), name="comment"),
    path('project-dashboard/<int:pk>/edit', ProjectUpdateView.as_view(), name='projectEdit'),
    path('project-dashboard/<int:pk>/delete', ProjectDeleteView.as_view(), name='projectDelete'),
]
