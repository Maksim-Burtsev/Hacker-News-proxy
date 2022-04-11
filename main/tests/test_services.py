import os

from django.test import TestCase

from main.services import(
    add_query_params_to_link,
    _parser,
    _clean_text_from_html,
    _clean_extra_tm,
    _update_links_and_static,
    get_updated_html_file,
    _replace_and_create_file
)


class MainServicesTest(TestCase):

    def test_add_query_param(self):
        url = 'https://gogle.com/'
        params = {
            'p': ['test_param'],
            'p2': ['2test_param', ],
        }

        correct_result = 'https://gogle.com/?p=test_param&p2=2test_param'
        result = add_query_params_to_link(url, params.items())

        self.assertEqual(result, correct_result)


    def test_parser(self):

        text = _parser('https://news.ycombinator.com/')
        self.assertTrue(text)


    def test_parser_bad_url(self):

        text = _parser('https://news.ycombinator.com/bad_url')
        self.assertIsNone(text)


    def test_clean_text_from_html(self):

        raw_text = '<h1>Hello, world!</h1>'
        self.assertEqual('  Hello  world \n\n',
                         _clean_text_from_html(raw_text))


    def test_clean_extra_tm(self):
        text = 'sixsix™ wron™g w™rnddfasd corrct™'

        self.assertEqual('sixsix™ wrong wrnddfasd corrct™',
                         _clean_extra_tm(text))


    def test_update_links_and_static(self):

        text = 'test text https://news.ycombinator.com favicon.ico y18.gif'
        result = _update_links_and_static(text)

        self.assertTrue(result.startswith('{% load static %}'))

        self.assertFalse('favicon.ico' in result)

        self.assertFalse('y18.gif' in result)

        self.assertTrue("{% static 'main/logo.ico' %}" in result)

        self.assertEqual(result.count("{% static 'main/logo.ico' %}"), 2)


    def test_get_updated_html_page(self):

        url = 'https://news.ycombinator.com/news'
        path_to_file = 'main\\templates\\main\\test.html'

        get_updated_html_file(url, filename='test')

        self.assertTrue(os.path.exists(path_to_file))

        os.remove('main\\templates\\main\\test.html')


    def test_replace_and_create_file(self):

        path_to_file = 'main\\templates\\main\\test_2.html'
        text = '<a href="#"> Some tessts texxxt </a><h1>Hello worlld!</h1>'
        correct_result = 'Some tessts™ texxxt™ Hello worlld™!'

        _replace_and_create_file(text, 'test_2')

        self.assertTrue(os.path.exists(path_to_file))

        with open(path_to_file, 'r', encoding='utf-8') as f:
            text = f.read()
            for word in correct_result.split():
                self.assertTrue(word in text)

        os.remove(path_to_file)
