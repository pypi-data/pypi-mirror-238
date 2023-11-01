from urllib.parse import urlparse

from django import http

def is_valid(request):
    # Assume that anything not defined as 'safe' by RFC7231 needs no protection
    if request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
        return True

    host = request.build_absolute_uri('/').rstrip('/')
    '''
        Note - we actually look for a valid referer header or origin header.
        Modern browsers will send an origin header with any non head/get request, and this may catch cases where the user has disable the referer header.
    '''

    if host == request.META.get('HTTP_ORIGIN') :
        return True

    parts = urlparse(request.META.get('HTTP_REFERER', ''))
    return host == f'{parts.scheme}://{parts.netloc}'


class Middleware:
    # middleware boilerplate
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        return response

    # Where the magic happens...
    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(view_func, 'csrf_exempt', False):
            return None

        if is_valid(request) :
            return None

        return http.HttpResponseForbidden('CSRF check failed.')