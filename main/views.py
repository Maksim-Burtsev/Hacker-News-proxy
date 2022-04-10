from django.shortcuts import render

from main.services import get_updated_html_file, add_query_params_to_link


def index(request):

    url = f'https://news.ycombinator.com{request.path}'
    
    request_items = dict(request.GET).items()
    if request_items:
        url = add_query_params_to_link(url, request_items)

    get_updated_html_file(url, filename='index')

    return render(request, 'main/index.html')
