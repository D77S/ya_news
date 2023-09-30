from http import HTTPStatus

from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_home_availability_for_anonim(client) -> None:
    '''Проверяет, что главная страница
    доступна анонимусу.
    Помним, что аннотировать только возврат функции,
    её входные данные - не надо. Не будем загромождать код.'''
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
        'name, args',
        (
            ('news:detail', pytest.lazy_fixture('id_for_args')),  # type: ignore
            ('news:home', None),
        ),
)
def test_pages_availability_for_anonim(client, name, args) -> None:
    '''
    Проверяет, что анонимусу доступно:
    - главная,
    - страниц отдельной новости.'''
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
