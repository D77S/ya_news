import pytest

from news.models import News


# Модель юзера для авторства нам пока не нужна,
# если будет нужна - потом и импортируем.


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
