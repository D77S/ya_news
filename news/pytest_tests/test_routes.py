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
            ('news:detail', pytest.lazy_fixture('id_for_args')),  # type: ignore
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
