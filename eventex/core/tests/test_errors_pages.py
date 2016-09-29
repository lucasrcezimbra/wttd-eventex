from django.test import TestCase

class ErrorsPagesTest(TestCase):
    def test_page_404(self):
        response = self.client.get('/nao-existe-asdfasdf')
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed(response, '404.html')
