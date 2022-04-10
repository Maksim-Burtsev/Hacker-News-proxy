from django.shortcuts import render

from main.services import get_updated_html_page


def index(request):

    page = get_updated_html_page(f'https://news.ycombinator.com{request.path}')

    return render(request, 'main/index.html')