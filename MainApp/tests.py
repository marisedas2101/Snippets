from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User
from .models import Snippet


# examples of different test
# test of getting
class SimpleTests(TestCase):

    def test_home_page_status_code(self):
        resp = self.client.get("/")
        self.failUnlessEqual(resp.status_code, 200)

    def test_snippet_list_status_code(self):
        resp = self.client.get('/snippets/list')
        self.failUnlessEqual(resp.status_code, 200)


# test for models in DB
class SnippetModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        Snippet.objects.create(name='just a test', lang='python', code='something for test',
                               creation_date='2006-10-25 14:30:59', user=self.user)

    def test_text_content(self):
        snippet = Snippet.objects.get(id=1)
        expected_object_name = f'{snippet.name}'
        self.assertEqual(expected_object_name, 'just a test')
