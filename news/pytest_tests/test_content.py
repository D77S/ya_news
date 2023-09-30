import pytest

from django.urls import reverse

from news.models import News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_main_not_more_than_need(client):
    '''
    Проверяет, что на главной странице
    отображается новостей не более штук, чем сколько надо.'''
    url_main = reverse('news:home', args=None)
    main_page_draft_news_list = []
    for index in range(NEWS_COUNT_ON_HOME_PAGE + 2):
        news = News(title=f'Новость {index}', text='Просто текст.')
        main_page_draft_news_list.append(news)
    News.objects.bulk_create(main_page_draft_news_list)
    response = client.get(url_main)
    object_list = response.context['object_list']
    assert len(object_list) == NEWS_COUNT_ON_HOME_PAGE
