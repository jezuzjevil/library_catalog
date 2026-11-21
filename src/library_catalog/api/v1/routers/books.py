from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from ...dependencies import BookServiceDep
from ..schemas.book import (
    BookCreate,
    BookUpdate,
    ShowBook,
)
from ..schemas.common import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/books", tags=["Books"])


@router.post(
    "/",
    response_model=ShowBook,
    status_code=status.HTTP_201_CREATED,
    summary="Создать книгу",
    description="Создать новую книгу в каталоге с автоматическим обогащением из Open Library",
    responses={
        400: {"description": "Некорректные данные книги"},
        409: {"description": "Книга с таким ISBN уже существует"},
    },
)
async def create_book(
    book_data: BookCreate,
    service: BookServiceDep,
) -> ShowBook:
    """
    Создать новую книгу.

    Автоматически обогащает данные из Open Library API:
    - Обложка книги
    - Темы/subjects
    - Издатель
    - Рейтинг

    Если Open Library недоступен, книга всё равно будет создана.

    Returns:
        ShowBook: Созданная книга.
    """
    return await service.create_book(book_data)


@router.get(
    "/",
    response_model=PaginatedResponse[ShowBook],
    summary="Получить список книг",
    description="Получить список книг с фильтрацией и пагинацией",
)
async def get_books(
    service: BookServiceDep,
    pagination: Annotated[PaginationParams, Depends()],
    title: str | None = Query(None, description="Поиск по названию"),
    author: str | None = Query(None, description="Поиск по автору"),
    genre: str | None = Query(None, description="Фильтр по жанру"),
    year: int | None = Query(None, description="Фильтр по году"),
    available: bool | None = Query(
        None,
        description="Фильтр по доступности",
    ),
) -> PaginatedResponse[ShowBook]:
    """
    Получить список книг с фильтрацией.

    Поддерживаемые фильтры:
    - title: частичное совпадение (регистронезависимо)
    - author: частичное совпадение (регистронезависимо)
    - genre: точное совпадение
    - year: точное совпадение
    - available: True/False

    Пагинация:
    - page: номер страницы (начиная с 1)
    - page_size: размер страницы (1-100, по умолчанию 20)

    Returns:
        PaginatedResponse[ShowBook]: Список книг с информацией о пагинации.
    """
    books, total = await service.search_books(
        title=title,
        author=author,
        genre=genre,
        year=year,
        available=available,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    return PaginatedResponse.create(books, total, pagination)


@router.get(
    "/{book_id}",
    response_model=ShowBook,
    summary="Получить книгу",
    description="Получить информацию о конкретной книге по ID",
    responses={
        404: {"description": "Книга не найдена"},
    },
)
async def get_book(
    book_id: UUID,
    service: BookServiceDep,
) -> ShowBook:
    """
    Получить книгу по ID.

    Args:
        book_id: UUID идентификатор книги.

    Returns:
        ShowBook: Полная информация о книге.

    Raises:
        BookNotFoundException: Если книга не найдена.
    """
    return await service.get_book(book_id)


@router.patch(
    "/{book_id}",
    response_model=ShowBook,
    summary="Обновить книгу",
    description="Частичное обновление книги (передаются только изменяемые поля)",
    responses={
        400: {"description": "Некорректные данные книги"},
        404: {"description": "Книга не найдена"},
        409: {"description": "Книга с таким ISBN уже существует"},
    },
)
async def update_book(
    book_id: UUID,
    book_data: BookUpdate,
    service: BookServiceDep,
) -> ShowBook:
    """
    Обновить книгу.

    Передаются только те поля, которые нужно изменить.
    Остальные поля остаются без изменений.

    Args:
        book_id: UUID идентификатор книги.
        book_data: Данные для обновления.

    Returns:
        ShowBook: Обновлённая книга.

    Raises:
        BookNotFoundException: Если книга не найдена.
        InvalidYearException: Если год издания некорректен.
        InvalidPagesException: Если количество страниц некорректно.
    """
    return await service.update_book(book_id, book_data)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить книгу",
    description="Удалить книгу из каталога",
    responses={
        404: {"description": "Книга не найдена"},
    },
)
async def delete_book(
    book_id: UUID,
    service: BookServiceDep,
) -> None:
    """
    Удалить книгу.

    Args:
        book_id: UUID идентификатор книги.

    Raises:
        BookNotFoundException: Если книга не найдена.

    Returns:
        None: Успешное удаление без тела ответа.
    """
    await service.delete_book(book_id)
