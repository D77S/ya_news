import pytest
from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_main_is_that_needs_to_be(client):
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


def test_comments_order(author, author_client, novost, id_for_args):
    '''
    Проверяет, что каменты к новости
    выводятся сортированными как надо по дате.'''
    url_of_novost_to_comment_to = reverse('news:detail', args=id_for_args)
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=novost,
            author=author,
            text=f'Tекст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    response = author_client.get(url_of_novost_to_comment_to)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(id_for_args, client):
    '''
    Проверяет, что анонимусу недоступна
    форма для отправки комментария'''
    url_of_novost_to_comment_to = reverse('news:detail', args=id_for_args)
    response = client.get(url_of_novost_to_comment_to)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(id_for_args, admin_client):
    '''
    Проверяет, что авторизованному юзеру
    доступна форма для отправки комментария.'''
    url_of_novost_to_comment_to = reverse('news:detail', args=id_for_args)
    response = admin_client.get(url_of_novost_to_comment_to)
    assert 'form' in response.context
