from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, DonationForAdminDB,
                                  DonationForUserDB)
from app.services.investment import \
    distribute_donations as donations_distribution

router = APIRouter()


@router.post(
    '/',
    response_model=DonationForUserDB,
    response_model_exclude_none=True,
    summary='Создание нового пожертвования',
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    donation = await donation_crud.create(donation, session, user)
    donation = await donations_distribution(
        distributed=donation,
        destinations=await charity_project_crud.get_opens(session),
        session=session,
    )
    return donation


@router.get(
    '/',
    response_model=list[DonationForAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Получение списка всех пожертвований'
            ' (доступно только администратору)',
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=list[DonationForUserDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
    summary='Получение списка пожертвований текущего пользователя',
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(user, session)
