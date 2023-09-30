import pytest

from django.urls import reverse

from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(id_for_args, client):
    '''
    Проверяет, что анонимус не может отправить коммент.'''
    url_of_novost_to_comment_to = reverse('news:detail', args=id_for_args)
    form_data = {'text': 'Текст попытки анонима комментировать.'}
    client.post(url_of_novost_to_comment_to, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0
