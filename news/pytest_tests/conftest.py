import pytest

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    '''
    Создает и возвращает какого-то автора.'''
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    '''
    Логинит автора в клиенте и возвращает
    клиента с залогиненным в нем автором.'''
    client.force_login(author)
    return client


@pytest.fixture
def novelty():
    '''
    Создает и возвращает объект новости.'''
    novelty = News.objects.create(
        title='Заголовок новости',
        text='Текстовка новости',
    )
    return novelty


@pytest.fixture
def id_for_args(novelty):
    '''
    Возвращает от объекта новости только id.'''
    return (novelty.id,)


@pytest.fixture
def comment(novelty, author):
    '''
    Создает и возвращает камент
    тестового автора к тестовой новости.'''
    comment = Comment.objects.create(
        news=novelty,
        author=author,
        text='Блаблабла',
    )
    return comment
