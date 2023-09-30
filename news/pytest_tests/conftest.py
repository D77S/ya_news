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
def novost():
    '''
    Создает и возвращает объект новости.'''
    novost = News.objects.create(
        title='Заголовок новости',
        text='Текстовка новости',
    )
    return novost


@pytest.fixture
def id_for_args(novost):
    '''
    Возвращает от объекта новости только id.'''
    return (novost.id,)


@pytest.fixture
def comment(novost, author):
    '''
    Создает и возвращает камент
    тестового автора к тестовой новости.'''
    comment = Comment.objects.create(
        news=novost,
        author=author,
        text='Блаблабла',
    )
    return comment
