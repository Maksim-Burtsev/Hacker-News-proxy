from django.test import TestCase


class MainViewsTest(TestCase):

    def test_index(self):

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_index_with_param(self):

        response = self.client.get('/item?id=30977883')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
