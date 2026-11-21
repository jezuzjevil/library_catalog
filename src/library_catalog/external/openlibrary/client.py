import httpx
from pydantic import ValidationError

from ..base.base_client import BaseApiClient
from ...domain.exceptions import (
    OpenLibraryException,
    OpenLibraryTimeoutException,
)
from .schemas import OpenLibrarySearchResponse


class OpenLibraryClient(BaseApiClient):
    """Клиент для Open Library API."""

    def __init__(
        self,
        base_url: str = "https://openlibrary.org",
        timeout: float = 10.0,
    ):
        super().__init__(base_url, timeout=timeout)

    def client_name(self) -> str:
        return "openlibrary"

    async def search_by_isbn(self, isbn: str) -> dict:
        """
        Поиск книги по ISBN-10 или ISBN-13.

        Returns:
            dict: Данные найденной книги или пустой словарь.
        """
        try:
            data = await self._get(
                "/search.json",
                params={"isbn": isbn, "limit": 1},
            )

            response = OpenLibrarySearchResponse.model_validate(data)

            if not response.docs:
                return {}

            return self._extract_book_data(
                response.docs[0].model_dump()
            )

        except httpx.TimeoutException as e:
            raise OpenLibraryTimeoutException(self.timeout) from e

        except (httpx.HTTPError, ValidationError) as e:
            raise OpenLibraryException(str(e)) from e

    async def search_by_title_author(
        self,
        title: str,
        author: str,
    ) -> dict:
        """Поиск книги по названию и автору."""

        try:
            data = await self._get(
                "/search.json",
                params={
                    "title": title,
                    "author": author,
                    "limit": 1,
                },
            )

            response = OpenLibrarySearchResponse.model_validate(data)

            if not response.docs:
                return {}

            return self._extract_book_data(
                response.docs[0].model_dump()
            )

        except httpx.TimeoutException as e:
            raise OpenLibraryTimeoutException(self.timeout) from e

        except (httpx.HTTPError, ValidationError) as e:
            raise OpenLibraryException(str(e)) from e

    async def enrich(
        self,
        title: str,
        author: str,
        isbn: str | None = None,
    ) -> dict:
        """
        Обогатить данные книги.

        Сначала ищет по ISBN, затем по названию и автору.
        """

        # Попытка 1: поиск по ISBN
        if isbn:
            data = await self.search_by_isbn(isbn)

            if data:
                return data

        # Попытка 2: поиск по названию и автору
        return await self.search_by_title_author(title, author)

    def _extract_book_data(self, doc: dict) -> dict:
        """Извлечь нужные поля из ответа Open Library."""

        result = {}

        # Обложка
        if cover_id := doc.get("cover_i"):
            result["cover_url"] = self._get_cover_url(cover_id)

        # Темы книги (не более 10)
        if subjects := doc.get("subject"):
            result["subjects"] = subjects[:10]

        # Издательство
        if publisher := doc.get("publisher"):
            result["publisher"] = publisher[0]

        # Язык
        if language := doc.get("language"):
            result["language"] = language[0]

        # Рейтинг
        if rating := doc.get("ratings_average"):
            result["rating"] = rating

        # Первое предложение книги, если оно есть в ответе API
        if first_sentence := doc.get("first_sentence"):
            if isinstance(first_sentence, list):
                result["description"] = first_sentence[0]
            else:
                result["description"] = first_sentence

        return result

    def _get_cover_url(self, cover_id: int | None) -> str | None:
        """Получить URL обложки по идентификатору."""

        if not cover_id:
            return None

        return (
            f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        )