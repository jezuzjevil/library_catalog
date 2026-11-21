from pydantic import BaseModel, ConfigDict, Field


class OpenLibrarySearchDoc(BaseModel):
    """Документ из поиска Open Library."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    author_name: list[str] | None = None
    cover_i: int | None = None
    subject: list[str] | None = None
    publisher: list[str] | None = None
    language: list[str] | None = None
    ratings_average: float | None = None
    first_sentence: list[str] | str | None = None


class OpenLibrarySearchResponse(BaseModel):
    """Ответ от /search.json."""

    numFound: int
    docs: list[OpenLibrarySearchDoc] = Field(default_factory=list)
