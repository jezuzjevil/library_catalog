from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ...dependencies import DbSessionDep
from ..schemas.common import HealthCheckResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Проверить состояние сервиса и подключение к БД",
)
async def health_check(db: DbSessionDep) -> HealthCheckResponse:
    """
    Проверить здоровье сервиса.

    Проверяет:
    - Сервис запущен.
    - Подключение к базе данных работает.

    Returns:
        HealthCheckResponse: Статус приложения и подключения к БД.
    """
    try:
        await db.execute(text("SELECT 1"))
        return HealthCheckResponse(
            status="healthy",
            database="connected",
        )

    except SQLAlchemyError:
        return HealthCheckResponse(
            status="healthy",
            database="disconnected",
        )
