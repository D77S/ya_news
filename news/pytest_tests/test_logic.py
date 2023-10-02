from django.urls import reverse
from pytest_django.asserts import assertFormError
import pytest

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

TRY_TO_COMMENT_FORM = {'text': 'Текст попытки комментировать.'}
NEW_COMMENT_TEXT = "Новое бла-бла-бла."
NEW_FORM_DATA = {'text': NEW_COMMENT_TEXT}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(id_for_args, client, ):
    '''
    Проверяет, что комментарий не разрешен анонимусу.'''
    url_of_novelty_to_comment_to = reverse('news:detail', args=id_for_args)
    comments_count_before_request = Comment.objects.count()
    client.post(url_of_novelty_to_comment_to, data=TRY_TO_COMMENT_FORM)
    comments_count_after_request = Comment.objects.count()
    assert comments_count_after_request == comments_count_before_request


@pytest.mark.django_db
def test_logged_user_can_create_comment(id_for_args, admin_client):
    '''
    Проверяет, что комментарий разрешен залогированному.'''
    url_of_novelty_to_comment_to = reverse('news:detail', args=id_for_args)
    comments_count_before_request = Comment.objects.count()
    admin_client.post(url_of_novelty_to_comment_to, data=TRY_TO_COMMENT_FORM)
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
    comments_count_before_request = Comment.objects.count()
    response = admin_client.post(
        url_of_novelty_to_comment_to,
        data=bad_words_data
    )
    comments_count_after_request = Comment.objects.count()
    assertFormError(response, 'form', 'text', errors=(WARNING))
    assert comments_count_after_request == comments_count_before_request


@pytest.mark.django_db
def test_author_can_edit_comment(comment, author_client):
    '''
    Проверяет, что редактирование комментария разрешено его автору.'''
    url_of_coment_to_edit_to = reverse('news:edit', args=(comment.id,))
    url_of_coment_to_edit_after = reverse(
        'news:detail',
        args=(comment.id,)
    ) + '#comments'
    response = author_client.post(url_of_coment_to_edit_to, NEW_FORM_DATA)
    comment.refresh_from_db()
    assert response.url == url_of_coment_to_edit_after
    assert comment.text == NEW_COMMENT_TEXT


@pytest.mark.django_db
def test_alien_cant_edit_comment(comment, client):
    '''
    Проверяет, что редактирование комментария запрещено его неавтору.'''
    url_of_coment_to_edit_to = reverse('news:edit', args=(comment.id,))
    url_of_coment_to_edit_after = reverse(
        'news:detail',
        args=(comment.id,)
    ) + '#comments'
    response = client.post(url_of_coment_to_edit_to, NEW_FORM_DATA)
    comment.refresh_from_db()
    assert response.url != url_of_coment_to_edit_after
    assert comment.text != NEW_COMMENT_TEXT


@pytest.mark.django_db
def test_author_can_delete_comment(id_for_args, comment, author_client):
    '''
    Проверяет, что удаление комментария разрешено его автору.'''
    url_of_coment_to_delete_to = reverse('news:delete', args=(comment.id,))
    url_of_coment_to_delete_after = reverse(
        'news:detail',
        args=id_for_args
    ) + '#comments'
    response = author_client.post(url_of_coment_to_delete_to)
    assert response.url == url_of_coment_to_delete_after


@pytest.mark.django_db
def test_alien_cant_delete_comment(id_for_args, comment, client):
    '''
    Проверяет, что удаление комментария запрещено его неавтору.'''
    url_of_coment_to_delete_to = reverse('news:delete', args=(comment.id,))
    url_of_coment_to_delete_after = reverse(
        'news:detail',
        args=id_for_args
    ) + '#comments'
    response = client.post(url_of_coment_to_delete_to)
    assert response.url != url_of_coment_to_delete_after
