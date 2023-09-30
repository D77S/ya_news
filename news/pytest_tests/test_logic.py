import pytest

from django.urls import reverse

from news.models import Comment


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('client'), True),  # type: ignore
        (pytest.lazy_fixture('admin_client'), False)  # type: ignore
    ),
)
def test_anonymous_user_cant_create_comment(
    id_for_args,
    parametrized_client,
    expected_status
):
    '''
    Проверяет, что комментарий:
    - не может быть отправлен анонимусом,
    - может быть отправлен залогированным.'''
    url_of_novost_to_comment_to = reverse('news:detail', args=id_for_args)
    form_data = {'text': 'Текст попытки комментировать.'}
    parametrized_client.post(url_of_novost_to_comment_to, data=form_data)
    comments_count = Comment.objects.count()
    assert (comments_count == 0) is expected_status
