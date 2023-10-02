from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone
import pytest

from news.models import Comment, News
#  from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_main_has_propper_news_amount(client):
    '''
    Проверяет, что на главной странице
    отображается новостейне более штук, чем сколько надо.'''
    url_main = reverse('news:home', args=None)
    today = datetime.today()
    main_page_draft_news_list = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 2)  # На 2 больше, чем.
    ]
    News.objects.bulk_create(main_page_draft_news_list)
    response = client.get(url_main)
    object_list = response.context['object_list']
    assert len(object_list) == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_main_has_propper_news_order(client):
    '''
    Проверяет, что на главной странице
    отображаются новости, сортированные по дате по reverse=True.'''
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
    assert sorted_dates_from_context == dates_from_context


def test_comments_order(author, author_client, novelty, id_for_args):
    '''
    Проверяет, что каменты к новости
    выводятся сортированными как надо по дате.'''
    url_of_novelty_to_comment_to = reverse('news:detail', args=id_for_args)
    now = timezone.now()
    for index in range(2):  # Создаем две, хватит и того.
        comment = Comment.objects.create(
            news=novelty,
            author=author,
            text=f'Tекст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    response = author_client.get(url_of_novelty_to_comment_to)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), False),  # type: ignore
        (pytest.lazy_fixture('admin_client'), True)  # type: ignore
    ),
)
def test_client_has_form(
    id_for_args,
    parametrized_client,
    #  admin_client,
    expected_status
):
    '''
    Проверяет, что форма для отправки комментария:
    - анонимусу недоступна,
    - логированному - доступна,
    - форма, вернувшаяся в ответе - того же типа, что отправлена в запросе.'''
    url_of_novelty_to_comment_to = reverse('news:detail', args=id_for_args)
    response = parametrized_client.get(url_of_novelty_to_comment_to)
    assert ('form' in response.context) == expected_status  # Переделано с "is" на "==".
    # if parametrized_client is admin_client:
        # Надо как-то проверить, что форма, вернувшаяся в ответа, -
        # того же типа, что и была отправлена в запросе.
        # Не получается:(
        # assert (response.context['form'] == CommentForm())
