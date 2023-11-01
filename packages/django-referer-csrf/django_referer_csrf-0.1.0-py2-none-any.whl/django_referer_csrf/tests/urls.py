from django import http
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

def return_foo(request):
    return http.HttpResponse('foo')

urlpatterns = [
    path('a/', return_foo),
    path('b/', csrf_exempt(return_foo)),
]