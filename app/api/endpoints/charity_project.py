from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectDB,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.investment import distribute_donations
from app.services.project_service import prepare_project_update_data

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создание нового благовторительного проекта',
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    await check_project_name_duplicate(project.name, session)
    return await distribute_donations(
        distributed=await charity_project_crud.create(project, session),
        destinations=await donation_crud.get_opens(session),
        session=session
    )


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Получение списка всех благотворительных проектов',
)
async def get_charity_projects(
        session: AsyncSession = Depends(get_async_session)
) -> List[CharityProjectDB]:
    return await charity_project_crud.get_all(session)


@router.get(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Получение информации о конкретном проекте',
)
async def get_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    return await charity_project_crud.get_or_404(project_id, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Обновление информации о благотворительном проекте',
)
async def update_project(
        project_id: int,
        project_data: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    project = await charity_project_crud.get_or_404(project_id, session)
    update_data = project_data.dict(exclude_unset=True)
    update_data = await prepare_project_update_data(project,
                                                    update_data, session)
    return await charity_project_crud.update(project, update_data, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Удаление благотовительного проекта',
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    project = await charity_project_crud.get_or_404(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail=f'{project} - были внесены средства, не подлежит удалению!'
        )
    return await charity_project_crud.delete(project, session)
