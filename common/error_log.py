import sys
from django.views import debug
from django.http import HttpResponseServerError


def server_error_display(request):
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)