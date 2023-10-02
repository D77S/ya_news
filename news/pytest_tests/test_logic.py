from django.urls import reverse
from pytest_django.asserts import assertFormError
import pytest

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(id_for_args, client, ):
    '''
    Проверяет, что комментарий не может быть отправлен анонимусом.'''
    url_of_novelty_to_comment_to = reverse('news:detail', args=id_for_args)
    form_data = {'text': 'Текст попытки комментировать.'}
    comments_count_before_request = Comment.objects.count()
    client.post(url_of_novelty_to_comment_to, data=form_data)
    comments_count_after_request = Comment.objects.count()
    assert comments_count_after_request == comments_count_before_request


@pytest.mark.django_db
def test_logged_user_can_create_comment(id_for_args, admin_client):
    '''
    Проверяет, что комментарийможет быть отправлен залогированным.'''
    url_of_novelty_to_comment_to = reverse('news:detail', args=id_for_args)
    form_data = {'text': 'Текст попытки комментировать.'}
    comments_count_before_request = Comment.objects.count()
    admin_client.post(url_of_novelty_to_comment_to, data=form_data)
    comments_count_after_request = Comment.objects.count()
    assert comments_count_after_request == (comments_count_before_request + 1)


@pytest.mark.django_db
def test_user_cant_use_bad_words(id_for_args, admin_client):
    '''
    Проверяет, что если камент содержит
    запрещенные слова, то он не будет опубликован,
    а форма вернет ошибку.'''
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url_of_novelty_to_comment_to = reverse('news:detail', args=id_for_args)
    response = admin_client.post(
        url_of_novelty_to_comment_to,
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
def test_somebody_can_edit_comment(
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
    url_of_coment_to_edit_after = reverse(
        'news:detail',
        args=(comment.id,)
    ) + '#comments'
    form_data = {'text': NEW_COMMENT_TEXT}
    response = parametrized_client.post(url_of_coment_to_edit_to, form_data)
    assert (response.url == url_of_coment_to_edit_after) is expected_status
    comment.refresh_from_db()
    assert (comment.text == NEW_COMMENT_TEXT) == expected_status   # Переделано с "is" на "==".


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), True),  # type: ignore
        (pytest.lazy_fixture('client'), False)  # type: ignore
    ),
)
def test_somebody_can_delete_comment(
    id_for_args,
    comment,
    parametrized_client,
    expected_status
):
    '''
    Проверяет, что удаление комментария:
    - разрешено, если это пытается делать его автор,
    - запрещено, если это пытается делать не его автор.'''
    url_of_coment_to_delete_to = reverse('news:delete', args=(comment.id,))
    url_of_coment_to_delete_after = reverse(
        'news:detail',
        args=id_for_args
    ) + '#comments'
    response = parametrized_client.post(url_of_coment_to_delete_to)
    assert (response.url == url_of_coment_to_delete_after) == expected_status   # Переделано с "is" на "==".
