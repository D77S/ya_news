import pytest
from datetime import datetime, timedelta

from django.urls import reverse

from news.models import News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_main_not_more_than_need(client):
    '''
    Проверяет, что на главной странице
    отображаются новости:
    - не более штук, чем сколько надо,
    - сортированы по дате так, как надо.'''
    url_main = reverse('news:home', args=None)

    today = datetime.today()
    main_page_draft_news_list = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 2)
    ]
    News.objects.bulk_create(main_page_draft_news_list)
    response = client.get(url_main)
    object_list = response.context['object_list']
    dates_from_context = [news.date for news in object_list]
    sorted_dates_from_context = sorted(dates_from_context, reverse=True)
    assert ((len(object_list) == NEWS_COUNT_ON_HOME_PAGE)
           and (sorted_dates_from_context == dates_from_context))

def test_comments_order():
    '''
    Проверяет, что каменты к новости
    выводятся сортированными как надо по дате.'''

    # создать новость
    # создать к ней два камента
    # запросить клиента
    # из него запросить объект новости
    # к нему запросить каменты
    # проверить их сортировку
    #
    # примерно так:
    # response = client.get(detail_url)
    # assertIn('news', response.context)
    # news = response.context['news']
    # all_comments = news.comment_set.all()
    # assertLess(all_comments[0].created, all_comments[1].created)
