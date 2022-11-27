import datetime

from loguru import logger
from asgiref.sync import sync_to_async
from models import User


@sync_to_async()
def add_user(user_id: int, username: str, first_name: str, last_name: str) -> None:
    query = User.select().where(User.user_id == user_id)
    date_today = datetime.datetime.today().date()
    if not query.exists():
        new_user = User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            registration_date=date_today,
        )
        new_user.save()
        logger.info(f'Новый пользователь: {user_id}|@{username}|{first_name}')
    else:
        logger.info(f'Пользователь уже существует: {user_id}|@{username}|{first_name}')


@sync_to_async()
def adding_additional_information(user_id: int, post: str, expert: str) -> None:
    update_data = User.update(post=post, expert=expert).where(User.user_id == user_id)
    update_data.execute()


@sync_to_async()
def update_question_answer(quest_1: float,
                           quest_2: float,
                           quest_3: float,
                           quest_4: float,
                           quest_5: float,
                           quest_6: float,
                           quest_7: float,
                           quest_8: float,
                           user_id: int):
    avg_shore = round((quest_1 + quest_2 + quest_3 + quest_4 + quest_5 + quest_6 + quest_7 + quest_8) / 8, 2)
    update_users_shore = User.update(
        quest_1=round(quest_1, 2),
        quest_2=round(quest_2, 2),
        quest_3=round(quest_3, 2),
        quest_4=round(quest_4, 2),
        quest_5=round(quest_5, 2),
        quest_6=round(quest_6, 2),
        quest_7=round(quest_7, 2),
        quest_8=round(quest_8, 2),
        avg_all_shore=avg_shore
    ).where(User.user_id == user_id)
    update_users_shore.execute()

