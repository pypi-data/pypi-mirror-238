from django.test import TestCase, override_settings

@override_settings(ROOT_URLCONF='django_referer_csrf.tests.urls')
class MyTestCase(TestCase):
    def test_get_request_is_allowed(self):
        self.assertEqual(
            self.client.get('/a/').status_code,
            200
        )
    def test_post_without_credentials_fails(self):
        self.assertEqual(
            self.client.post('/a/').status_code,
            403
        )
    def test_post_with_csrf_exempt_passes(self):
        self.assertEqual(
            self.client.post('/b/').status_code,
            200
        )
    @override_settings(ROOT_URLCONF='django_referer_csrf.tests.urls', ALLOWED_HOSTS=['foobar.com'])
    def test_post_with_origin_passes(self):
        r = self.client.post('/a/', 
            HTTP_HOST='foobar.com', 
            HTTP_ORIGIN='http://foobar.com'
        )
        self.assertEqual(
            r.status_code,
            200
        )
    @override_settings(ROOT_URLCONF='django_referer_csrf.tests.urls', ALLOWED_HOSTS=['foobar.com'])
    def test_post_with_referer_passes(self):
        r = self.client.post('/a/', 
            HTTP_HOST='foobar.com', 
            HTTP_REFERER='http://foobar.com/aff/af?foo'
        )
        self.assertEqual(
            r.status_code,
            200
        )