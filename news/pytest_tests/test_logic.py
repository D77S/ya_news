import pytest
from pytest_django.asserts import assertFormError

from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


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


@pytest.mark.django_db
def test_user_cant_use_bad_words(id_for_args, novost, admin_client):
    '''
    Проверяет, что если камент содержит
    запрещенные слова, то он не будет опубликован,
    а форма вернет ошибку.'''
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url_of_novost_to_comment_to = reverse('news:detail', args=id_for_args)
    response = admin_client.post(url_of_novost_to_comment_to, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    comments_count = Comment.objects.count()
    assert comments_count == 0
