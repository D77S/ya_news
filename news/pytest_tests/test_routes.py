from http import HTTPStatus

from django.urls import reverse
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
        'name, args',
        (
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
            ('news:home', None),
            ('news:detail', pytest.lazy_fixture(
                'id_for_args'
            )),  # type: ignore
        ),
)
def test_pages_availability_for_anonim(client, name, args) -> None:
    '''
    Проверяет, что анонимусу доступно:
    - логин,
    - логаут,
    - рега,
    - главная,
    - страниц отдельной новости.'''
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
        'name',
        ('news:edit', 'news:delete'),
)
def test_comment_change_pages_for_author(author_client, name, comment):
    url = reverse(name, args=(comment.id,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK
