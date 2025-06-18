from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_not_less_than_invested,
                                check_project_name_duplicate,
                                check_project_not_fully_invested)
from app.models import CharityProject
from app.services.close_service import CloseService


async def prepare_project_update_data(
    project: CharityProject,
    update_data: dict,
    session: AsyncSession
) -> dict:
    """Подготавливает и валидирует данные для обновления проекта.

    Выполняет проверки перед обновлением проекта:
    - Уникальность нового имени проекта
    - Возможность изменения суммы (проект не закрыт)
    - Новую сумму нельзя установить меньше уже инвестированной
    - Автоматическое закрытие проекта при полном сборе средств
    """
    new_full_amount = update_data.get('full_amount')
    new_name = update_data.get('name')

    if new_name is not None:
        await check_project_name_duplicate(new_name, session)

    if new_full_amount is not None:
        await check_project_not_fully_invested(project.id, session)
        await check_full_amount_not_less_than_invested(
            project.id, new_full_amount, session
        )
        if new_full_amount == project.invested_amount:
            await CloseService.close_investment(project, session)

    return update_data
