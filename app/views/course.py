from django.views.generic import ListView, DetailView
from ..models import Course

class CourseView(ListView):
    template_name = 'courses/course.html'
    model = Course

class CourseDetailView(DetailView):
    template_name = 'courses/courseDetail.html'
    model = Course
