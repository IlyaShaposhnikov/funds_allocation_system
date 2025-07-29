
from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import (set_user_permissions, create_spreadsheet,
                                     update_spreadsheet)

router = APIRouter()


@router.post(
    '/',
    response_model=List[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    charity_project = await (charity_project_crud.
                             get_projects_by_completion_rate(session))
    spreadsheetid = await create_spreadsheet(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await update_spreadsheet(spreadsheetid,
                                    charity_project, wrapper_services)
    return charity_project
