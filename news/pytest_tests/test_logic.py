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
def test_user_cant_use_bad_words(id_for_args, admin_client):
    '''
    Проверяет, что если камент содержит
    запрещенные слова, то он не будет опубликован,
    а форма вернет ошибку.'''
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url_of_novost_to_comment_to = reverse('news:detail', args=id_for_args)
    response = admin_client.post(
        url_of_novost_to_comment_to,
        data=bad_words_data
    )
    assertFormError(response, 'form', 'text', errors=(WARNING))
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), True),  # type: ignore
        (pytest.lazy_fixture('client'), False)  # type: ignore
    ),
)
def test_author_can_edit_note(
    comment,
    parametrized_client,
    expected_status
):
    '''
    Проверяет, что редактирование комментария:
    - разрешено, если это пытается делать его автор,
    - запрещено, если это пытается делать не его автор.'''
    NEW_COMMENT_TEXT = "Новое бла-бла-бла."
    url_of_coment_to_edit_to = reverse('news:edit', args=(comment.id,))
    url_of_coment_to_edit_after = reverse('news:detail', args=(comment.id,)) + '#comments'
    form_data = {'text': NEW_COMMENT_TEXT}
    response = parametrized_client.post(url_of_coment_to_edit_to, form_data)
    assert (response.url == url_of_coment_to_edit_after) is expected_status
    comment.refresh_from_db()
    assert (comment.text == NEW_COMMENT_TEXT) is expected_status
