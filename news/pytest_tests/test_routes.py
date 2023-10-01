from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse


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


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture(
            'admin_client'
        ), HTTPStatus.NOT_FOUND),  # type: ignore
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)  # type: ignore
    ),
)
@pytest.mark.parametrize(
        'name',
        ('news:edit', 'news:delete'),
)
def test_comment_change_pages_for_author(
    parametrized_client,
    name,
    comment,
    expected_status
):
    '''
    Проверяет, что НЕавтору камента НЕдоступно:
    - его редактирование,
    - его удаление.
    А вот автору камента доступно:
    - его редактирование,
    - его удаление.'''
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
        'name',
        ('news:edit', 'news:delete'),
)
def test_redirects(client, name, comment):
    '''
    Проверяет, что если анонимус хочет
    на страницу редактирования или удаления камента,
    то его перенаправляет на логин.'''
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
