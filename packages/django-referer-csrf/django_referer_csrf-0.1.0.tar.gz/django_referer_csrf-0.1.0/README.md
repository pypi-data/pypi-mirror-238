# django_referer_csrf

This project has 2 goals:

1. Simplifiy django's CSRF protection so that developers don't need to worry about the token
2. Make it easier for view code to invoke CSRF protection dynamically

## The token isn't needed

https://security.stackexchange.com/a/197269

On https sites, django's csrf protection requires that the request's referer header matches the request's host header. This check makes the entire CSRF token redundant. The token check provides no extra security on top of the referer check.

Django skips the referer check on non-https sites, which is somewhat advantageous (it means that users who configure their web browsers not submit a referer header can still submit forms). 

Our validator actually looks for a valid origin header or referer header. Modern browsers follow the (newish) spec, which is to send an origin header with every request other than head/get. This means that if users have the referer header disabled, they can still pass our CSRF check.

## Usage

- `pip install django_referer_csrf`
- in your `MIDDLEWARE` setting, replace `django.middleware.csrf.CsrfViewMiddleware` with `django_referer_csrf.Middleware`

With this middleware, you can still use Djangos's csrf_exempt decorators.

If you want to apply the CSRF protection based on dynamic conditions in view code, just check to see what the Middleware.process_view() does and replicate that.