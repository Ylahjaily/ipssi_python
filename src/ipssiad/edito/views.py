from django.http import HttpResponse
from django.template import loader

from .models import Article


def articles(request):
    template = loader.get_template('articles.html')
    articles = Article.objects.filter(status='online')

    context = {
        'article_list': articles,
    }

    return HttpResponse(template.render(context, request))


def article(request, uuid):
    template = loader.get_template('article.html')
    article = Article.objects.get(pk=uuid)

    context = {
        'article': article,
    }

    return HttpResponse(template.render(context, request))
