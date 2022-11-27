from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_test = InlineKeyboardButton('Начать тест', callback_data='start')
restart_test = InlineKeyboardButton('Пройти заново', callback_data='start')
back_button = InlineKeyboardButton('Назад', callback_data='back')
almost_never = InlineKeyboardButton('Практически никогда', callback_data='1')
rarely = InlineKeyboardButton('Редко', callback_data='2')
sometimes = InlineKeyboardButton('Иногда', callback_data='3')
often = InlineKeyboardButton('Часто', callback_data='4')
almost_always = InlineKeyboardButton('Практически всегда', callback_data='5')
business_owner = InlineKeyboardButton('Собственник бизнеса', callback_data='Собственник бизнеса')
general_manager = InlineKeyboardButton('Генеральный директор', callback_data='Генеральный директор')
head_of_the_department = InlineKeyboardButton('Руководитель подразделения', callback_data='руководитель подразделения')
specialist = InlineKeyboardButton('Специалист', callback_data='Специалист')
freelancer = InlineKeyboardButton('Фрилансер', callback_data='Фрилансер')
other = InlineKeyboardButton('Другое', callback_data='Другое')
sign_up = InlineKeyboardButton('Записаться на консультацию', url='https://t.me/sofia_kuzina')
to_share = InlineKeyboardButton('Рекомендовать другу', callback_data='repost')

new_users = InlineKeyboardButton("Новые пользователи", callback_data='new_users')
users_count = InlineKeyboardButton("Кол-во пользователей", callback_data='users_count')
one_day = InlineKeyboardButton("За день", callback_data='one_day')
one_week = InlineKeyboardButton("За неделю", callback_data='one_week')
one_mouth = InlineKeyboardButton("За месяц", callback_data='one_mouth')
add_post = InlineKeyboardButton("Рассылка", callback_data="add_post")
yes = InlineKeyboardButton("Да", callback_data='yes')
no = InlineKeyboardButton("Нет", callback_data='no')
cancel = InlineKeyboardButton("Отменить", callback_data='cancel')


start_keyboard = InlineKeyboardMarkup().add(start_test)
answers_keyboard = InlineKeyboardMarkup().add(almost_never).add(rarely).add(
    sometimes).add(often).add(almost_always).add(back_button)
post_keyboard = InlineKeyboardMarkup().add(business_owner).add(general_manager).add(
    head_of_the_department).add(specialist).add(freelancer).add(other)
sign_up_keyboard = InlineKeyboardMarkup().add(sign_up).add(restart_test).add(to_share)
new_users_keyboard = InlineKeyboardMarkup().add(new_users, users_count).add(add_post)
stat_keyboard = InlineKeyboardMarkup().add(one_day, one_week, one_mouth)
yes_or_no = InlineKeyboardMarkup().add(yes, no).add(cancel)
cancel_keyboard = InlineKeyboardMarkup().add(cancel)