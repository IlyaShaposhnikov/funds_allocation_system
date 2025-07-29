from http import HTTPStatus

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession
) -> None:
    """Проект с указанным именем не должен существовать в системе."""

    project_id = await charity_project_crud.get_id_by_name(name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Проект с именем \'{name}\' уже существует.'
        )


async def check_project_not_fully_invested(
        project_id: int,
        session: AsyncSession
) -> None:
    """Проект должен быть открыт для инвестирования."""

    project = await charity_project_crud.get_or_404(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Проект {project.name} закрыт, редактирование недоступно!'
        )


async def check_full_amount_not_less_than_invested(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession
) -> None:
    """Новая сумма должна быть не меньше уже инвестированной суммы."""

    project = await charity_project_crud.get_or_404(project_id, session)
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Нельзя установить значение full_amount'
                   f' меньше уже вложенной суммы: {project.invested_amount}.'
        )
