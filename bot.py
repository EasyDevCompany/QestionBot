import logging
import os
import datetime

from random import randint
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
from loguru import logger
from models import User

import keyboards
from keyboards import start_keyboard, answers_keyboard
from db_commands import add_user, adding_additional_information, update_question_answer
from form_pdf import forming_test_result_pdf

dotenv_path = os.path.abspath(os.path.join('.env'))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

logging.basicConfig(level=logging.INFO)
# BOT_API = os.getenv('5481266432:AAFD5JoMTTmfhZrirqLaxK3N4ulFXG2i6F0')
bot = Bot(token='5656589630:AAHhXI2ptopht526dQ3FkYWRJHy4nwMhK-4', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

logger.add('logger.log', format='{time} {level} {message}', level='ERROR')


class Question(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()
    question_11 = State()
    question_12 = State()
    question_13 = State()
    question_14 = State()
    question_15 = State()
    question_16 = State()
    question_17 = State()
    question_18 = State()
    question_19 = State()
    question_20 = State()
    question_21 = State()
    question_22 = State()
    question_23 = State()
    question_24 = State()


class Welcome(StatesGroup):
    name = State()
    post = State()
    expert = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await add_user(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
        )
    await message.answer("Привет 👋🏻\n"
                         "Я - твой помощник в ускорении движения к твоим целям 🚀\n"
                         "Со мной ты узнаёшь, как идти к целям кратчайшим путём.\n"
                         "Как тебя зовут?")

    await Welcome.name.set()


@dp.message_handler(state=Welcome.name)
async def save_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f'{name}, очень приятно!\n\n'
                         f'Прежде, чем мы начнём, расскажи о себе, пожалуйста. '
                         f'Это поможет мне дать более точные результаты 📊\n'
                         f'Какая у тебя должность?', reply_markup=keyboards.post_keyboard)

    await Welcome.post.set()


@dp.callback_query_handler(state=Welcome.post)
async def save_post(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    data = callback_query.data
    await state.update_data(post=data)
    await callback_query.message.answer('В чем ты эксперт?')

    await Welcome.expert.set()


@dp.message_handler(state=Welcome.expert)
async def save_expert(message: types.Message, state: FSMContext):
    await message.answer('Спасибо! Рад, что ты хочешь расти в своей области быстрее 🌱\n\n'
                         'Мне тоже есть чем гордиться!\n'
                         'Меня придумал executive-коуч уровня PCC ICF - София Кузина.\n\n'
                         '🔹 София работает корпоративным коучем для руководителей в Сбербанке\n'
                         '🔹 Выступает в Сколково как приглашённый коуч\n'
                         '🔹 Работает с руководителями со всего мира на английском: США, Англия, Израиль, Тайланд и др\n'
                         '🔹 Создала онлайн-курс на Udemy, более 14 000 студентов\n\n'
                         'После теста будет возможность познакомиться с Софией и пройти бесплатную диагностику 📈')

    await message.answer('Этот тест основан на анализе более 500 коуч-сессий. Было выявлено 8 факторов быстрого роста,'
                         ' которые диагностируются в этом тесте 📊\n\n'
                         'Тест состоит из 24 вопросов, займёт 5-7 минут. В конце теста ты получишь подарок'
                         ' - структурный отчёт о том, какие барьеры мешает твоему росту в первую очередь 🎁'
                         ' p.s обещаю, дизайн тебя приятно удивит :)\n\n'
                         'Приступим?', reply_markup=keyboards.start_keyboard)

    user_id = message.from_user.id
    expert = message.text
    user_data = await state.get_data()
    await adding_additional_information(user_id=user_id, post=user_data["post"], expert=expert)
    await state.finish()


@dp.callback_query_handler(text='start')
async def start(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f'{hbold("Вопрос 1/24")}\n'
                                           f'Близкие мне люди поддерживают мои начинания и'
                                           f' дают возможность их реализовывать')
    await callback_query.message.edit_reply_markup(reply_markup=answers_keyboard)
    await Question.next()


@dp.callback_query_handler(state=Question.question_1)
async def save_first_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.answer("Тест отменен!\n"
                                            "Чтобы начать его проходить нажмите на кнопку ниже👇",
                                            reply_markup=start_keyboard)
        await state.finish()
    else:
        logger.info(f"{data} балл за первый вопрос")
        await state.update_data(question_1=int(data))
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 2/24")}\n'
                                            f'Я нахожусь в окружении, где'
                                            f' более 30% людей добились большего успеха, чем я',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_2)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    logger.info(data)
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 1/24")}\n'
                                            f'Близкие мне люди поддерживают мои начинания и'
                                            f' дают возможность их реализовывать',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_2=int(data))
        logger.info(f"{data} балл за второй вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 3/24")}\n'
                                               f'После общения с моим окружением, у меня'
                                               f' появляется вдохновение и заряд энергии ',
                                               reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_3)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data_2 = callback_query.data
    if data_2 == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 2/24")}\n'
                                            f'Я нахожусь в окружении, где'
                                            f' более 30% людей добились большего успеха, чем я',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_3=int(data_2))
        data = await state.get_data()
        average_number = (data["question_1"] + data["question_2"] + data["question_3"]) / 3
        await state.update_data(environment=average_number)
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 4/24")}\n'
                                            f'Я точно знаю, как именно реализовать поставленную цель',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_4)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 3/24")}\n'
                                            f'После общения с моим окружением, у меня'
                                            f' появляется вдохновение и заряд энергии ',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_4=int(data))
        logger.info(f"{data} балл за четвертый вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 5/24")}\n'
                                            f'Когда я составляю план, я рассматриваю'
                                            f' альтернативные способы достижения цели',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_5)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 4/24")}\n'
                                            f'Я точно знаю, как именно реализовать поставленную цель ',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_5=int(data))
        logger.info(f"{data} балл за пятый вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 6/24")}\n'
                                            f'Каждый день я точно знаю, что именно'
                                            f' надо сделать для того, чтобы приблизиться к цели',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_6)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data_2 = callback_query.data
    if data_2 == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 5/24")}\n'
                                               f'Когда я составляю план, я рассматриваю'
                                               f' альтернативные способы достижения цели',
                                               reply_markup=answers_keyboard
                                               )
        await Question.previous()
    else:
        await state.update_data(question_6=int(data_2))
        data = await state.get_data()
        average_number = (data["question_4"] + data["question_5"] + data["question_6"]) / 3
        await state.update_data(plan=average_number)
        logger.info(f"{data} балл за шестой вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 7/24")}\n'
                                            f'Я могу быстро и четко назвать поставленную мною цель',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_7)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 6/24")}\n'
                                            f'Каждый день я точно знаю, что именно'
                                            f'надо сделать для того, чтобы приблизиться к цели',
                                            reply_markup=answers_keyboard
                                            )
        await Question.previous()
    else:
        await state.update_data(question_7=int(data))
        logger.info(f"{data} балл за седьмой вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 8/24")}\n'
                                               f'Поставленная цель меня вдохновляет и соотносится с моими ценностями',
                                               reply_markup=answers_keyboard
                                               )
        await Question.next()


@dp.callback_query_handler(state=Question.question_8)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 7/24")}\n'
                                            f'Каждый день я точно знаю, что именно'
                                            f'надо сделать для того, чтобы приблизиться к цели',
                                            reply_markup=answers_keyboard
                                            )
        await Question.previous()
    else:
        await state.update_data(question_8=int(data))
        logger.info(f"{data} балл за восьмой вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 9/24")}\n'
                                            f'Моя цель соотносится с долгосрочной стратегией ',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_9)
async def save_first_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data_2 = callback_query.data
    if data_2 == 'back':
        await callback_query.message.answer(f'{hbold("Вопрос 8/24")}\n'
                                            f'Поставленная цель меня вдохновляет и соотносится с моими ценностями ',
                                            reply_markup=answers_keyboard
                                            )
        await state.finish()
    else:
        logger.info(f"{data_2} балл за первый вопрос")
        await state.update_data(question_9=int(data_2))
        data = await state.get_data()
        average_number = (data["question_7"] + data["question_8"] + data["question_9"]) / 3
        await state.update_data(goal=average_number)
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 10/24")}\n'
                                            f'Я точно знаю, на чем концентрироваться '
                                            f'в первую очередь в моей профессиональной деятельности',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_10)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    logger.info(data)
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 9/24")}\n'
                                            f'Моя цель соотносится с долгосрочной стратегией ',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_10=int(data))
        logger.info(f"{data} балл за второй вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 11/24")}\n'
                                            f'При работе я легко держу фокус и не отвлекаюсь на посторонние дела',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_11)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 10/24")}\n'
                                            f'Я точно знаю, на чем концентрироваться в первую очередь'
                                            f' в моей профессиональной деятельности ',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_11=int(data))
        logger.info(f"{data} балл за третий вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 12/24")}\n'
                                            f'В конце дня я  точно знаю, что ценного'
                                            f' сделал за день и как подвинулся к цели ',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_12)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data_2 = callback_query.data
    if data_2 == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 11/24")}\n'
                                            f'При работе я легко держу фокус и не отвлекаюсь на посторонние дела',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_12=int(data_2))
        data = await state.get_data()
        average_number = (data["question_10"] + data["question_11"] + data["question_12"]) / 3
        await state.update_data(stunt=average_number)
        logger.info(f"{data} балл за четвертый вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 13/24")}\n'
                                            f'Я легко внедряю привычки в свою жизнь ',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_13)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 12/24")}\n'
                                            f'В конце дня я точно знаю, что ценного'
                                            f'сделал за день и как подвинулся к цели',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_13=int(data))
        logger.info(f"{data} балл за пятый вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 14/24")}\n'
                                            f'Мне легко изо дня в день выполнять регулярные'
                                            f' действия, приближающие к цели ',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_14)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 13/24")}\n'
                                            f'Я легко внедряю привычки в свою жизнь',
                                            reply_markup=answers_keyboard
                                            )
        await Question.previous()
    else:
        await state.update_data(question_14=int(data))
        logger.info(f"{data} балл за шестой вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 15/24")}\n'
                                            f'Я двигаюсь маленькими шагами к большой цели, не сбивая ритм движения',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_15)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data_2 = callback_query.data
    if data_2 == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 14/24")}\n'
                                            f'Мне легко изо дня в день выполнять регулярные'
                                            f'действия, приближающие к цели',
                                            reply_markup=answers_keyboard
                                            )
        await Question.previous()
    else:
        await state.update_data(question_15=int(data_2))
        data = await state.get_data()
        average_number = (data["question_13"] + data["question_14"] + data["question_15"]) / 3
        await state.update_data(discipline=average_number)
        logger.info(f"{data} балл за 15 вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 16/24")}\n'
                                            f'Я верю в то, что я принимаю верные решения ',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_16)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 15/24")}\n'
                                            f'Я двигаюсь маленькими шагами к большой цели, не сбивая ритм движения ',
                                            reply_markup=answers_keyboard
                                            )
        await Question.previous()
    else:
        await state.update_data(question_16=int(data))
        logger.info(f"{data} балл за восьмой вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 17/24")}\n'
                                            f'Я быстро и уверенно принимаю решения,'
                                            f'так как не сомневаюсь в своём выборе ',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_17)
async def save_first_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.answer(f"{hbold('Вопрос 16/24')}"
                                            "Я верю в том, что я принимаю верные решения",
                                            reply_markup=answers_keyboard)
        await state.finish()
    else:
        logger.info(f"{data} балл за первый вопрос")
        await state.update_data(question_17=int(data))
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 18/24")}\n'
                                            f'Я знаю, что способен добиться желаемого в установленные сроки ',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_18)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data_2 = callback_query.data
    logger.info(data_2)
    if data_2 == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 17/24")}\n'
                                            f'Я быстро и уверенно принимаю решения,'
                                            f' так как не сомневаюсь в своём выборе',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_18=int(data_2))
        data = await state.get_data()
        average_number = (data["question_16"] + data["question_17"] + data["question_18"]) / 3
        await state.update_data(confidence=average_number)
        logger.info(f"{data} балл за 18 вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 19/24")}\n'
                                            f'Я быстро адаптируюсь к меняющимся условиям ',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_19)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 18/24")}\n'
                                            f'Я знаю, что способен добиться желаемого в установленные сроки',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_19=int(data))
        logger.info(f"{data} балл за третий вопрос")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 20/24")}\n'
                                            f'В кризисные времена я мобилизуюсь и легко улавливаю тренды ',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_20)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 19/24")}\n'
                                            f'Я быстро адаптируюсь к меняющимся условиям ',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        logger.info(f"{data} балл за четвертый вопрос")
        await callback_query.message.edit_reply_markup()
        await state.update_data(question_20=int(data))
        await callback_query.message.answer(f'{hbold("Вопрос 21/24")}\n'
                                            f'Я пробую разные способы достижения цели, готов экспериментировать',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_21)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data_2 = callback_query.data
    if data_2 == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 20/24")}\n'
                                            f'В кризисные времена я мобилизуюсь и легко улавливаю тренды ',
                                            reply_markup=answers_keyboard)
        await Question.previous()
    else:
        await state.update_data(question_21=int(data_2))
        data = await state.get_data()
        average_number = (data["question_19"] + data["question_20"] + data["question_21"]) / 3
        await state.update_data(flexibility=average_number)
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 22/24")}\n'
                                            f'Я получаю удовольствие от процесса моей работы',
                                            reply_markup=answers_keyboard)
        await Question.next()


@dp.callback_query_handler(state=Question.question_22)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 21/24")}\n'
                                            f'Я пробую разные способы достижения цели, готов экспериментировать',
                                            reply_markup=answers_keyboard
                                            )
        await Question.previous()
    else:
        await state.update_data(question_22=int(data))
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 23/24")}\n'
                                               f'Когда я работаю, я не замечаю ход времени',
                                               reply_markup=answers_keyboard
                                               )
        await Question.next()


@dp.callback_query_handler(state=Question.question_23)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == 'back':
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 22/24")}\n'
                                            f'Я получаю удовольствие от процесса моей работы',
                                            reply_markup=answers_keyboard
                                            )
        await Question.previous()
    else:
        await state.update_data(question_23=int(data))
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(f'{hbold("Вопрос 24/24")}\n'
                                            f'Я увлечённо изучаю новое по моей профессиональной теме',
                                            reply_markup=answers_keyboard
                                            )
        await Question.next()


@dp.callback_query_handler(state=Question.question_24)
async def save_second_shore(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    data_2 = callback_query.data
    await state.update_data(question_24=int(data_2))
    data = await state.get_data()
    average_number = (data["question_22"] + data["question_23"] + data["question_24"]) / 3
    await state.update_data(interest=average_number)
    user_data = await state.get_data()
    interest = user_data["interest"]  # интерес
    flexibility = user_data["flexibility"]  # гибкость
    confidence = user_data["confidence"]  # уверенность
    discipline = user_data["discipline"]  # дисциплина
    stunt = user_data["stunt"]  # фокус
    goal = user_data["goal"]  # цель
    plan = user_data["plan"]  # план
    environment = user_data["environment"]  # окружение
    logger.info(f'{interest} {flexibility} {confidence} {discipline} {stunt} {goal} {plan} {environment}')
    pdf_num = randint(100, 1000000)

    logger.info(pdf_num)

    forming_test_result_pdf(
        pdf_num=pdf_num,
        interest=interest,
        flexibility=flexibility,
        confidence=confidence,
        discipline=discipline,
        stunt=stunt,
        goal=goal,
        plan=plan,
        environment=environment,
    )
    user_id = callback_query.from_user.id

    await update_question_answer(
        quest_1=float(interest),
        quest_2=float(flexibility),
        quest_3=float(confidence),
        quest_4=float(discipline),
        quest_5=float(stunt),
        quest_6=float(goal),
        quest_7=float(plan),
        quest_8=float(environment),
        user_id=user_id,
    )

    await callback_query.message.answer('Поздравляю с завершением теста!\n'
                                        'Я уважаю людей, которые доводят дело до конца 🤝\n\n'
                                        'В отчете по твоему тесту ты увидишь зоны для развития.\n'
                                        'Обрати на них внимание, эти факторы тормозят твой рост 📌')

    await callback_query.message.answer_document(open(f'{pdf_num}.pdf', 'rb'))
    os.remove(f'{pdf_num}.pdf')

    await callback_query.message.answer('Хочешь быстрее двигаться к целям, получая драйв от процесса? 🤩\n\n'
                                        'Записывайся на индивидуальную консультацию!\n\n'
                                        'София поможет построить кратчайший путь к цели и зажечься любовью к своему делу :)',
                                        reply_markup=keyboards.sign_up_keyboard)

    await state.finish()


@dp.callback_query_handler(text='repost')
async def repost_bot(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Я рад, что тебе понравилось 🌱\n\n'
                                        'Копируй ссылку и отправляй друзьям / коллегам:')
    await callback_query.message.answer('https://t.me/BottecQuestion_bot')


@dp.message_handler(commands=['admin'])
async def admin_start(message: types.Message):
    user_id = message.from_user.id
    if user_id == 688136452 or user_id == 694833645 or user_id == 5217389680:
        await message.answer('Выберите один пункт из меню ниже:', reply_markup=keyboards.new_users_keyboard)


@dp.callback_query_handler(text="users_count")
async def users_count_info(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    count = User.select().count()
    await callback_query.message.answer(f"Всего пользователей в боте: {count}")


@dp.callback_query_handler(text="new_users")
async def chose_time(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer(f"Выберите промежуток времени:", reply_markup=keyboards.stat_keyboard)


@dp.callback_query_handler(text="one_day")
async def one_day_check_info(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    today = datetime.datetime.today().date()
    user_info = User.select().where(User.registration_date == today)
    for user in user_info:
        await callback_query.message.answer(f"Пользователь: {user.first_name}\n"
                                            f"Дата регистрации: {user.registration_date}\n"
                                            f"Имя пользователя: {user.username}")

    await callback_query.message.answer('Все новые пользователи за день,'
                                        ' если ничего нет, значит пользователей не прибавилось')


@dp.callback_query_handler(text="one_week")
async def one_week_check_info(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    today = datetime.datetime.today().date()
    week_ago = today - datetime.timedelta(days=7)
    logger.info(f"{week_ago}")
    user_info = User.select().where(User.registration_date <= today, User.registration_date >= week_ago)
    for user in user_info:
        await callback_query.message.answer(f"Пользователь: {user.first_name}\n"
                                            f"Дата регистрации: {user.registration_date}\n"
                                            f"Имя пользователя: {user.username}")

    await callback_query.message.answer('Все новые пользователи за неделю,'
                                        ' если ничего нет, значит пользователей не прибавилось')


@dp.callback_query_handler(text="one_mouth")
async def one_mouth_check_info(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    today = datetime.datetime.today().date()
    mouth_ago = today - datetime.timedelta(days=30)
    logger.info(f"{mouth_ago}")
    user_info = User.select().where(User.registration_date <= today, User.registration_date >= mouth_ago)
    for user in user_info:
        await callback_query.message.answer(f"Пользователь: {user.first_name}\n"
                                            f"Дата регистрации: {user.registration_date}\n"
                                            f"Имя пользователя: {user.username}")

    await callback_query.message.answer('Все новые пользователи за месяц,'
                                        ' если ничего нет, значит пользователей не прибавилось')


class WaitePostInformation(StatesGroup):
    waite_description = State()
    waite_image_answer = State()
    waite_image = State()


@dp.callback_query_handler(text='add_post')
async def add_post(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer('Отправьте боту текст:', reply_markup=keyboards.cancel_keyboard)
    await WaitePostInformation.waite_description.set()


@dp.message_handler(state=WaitePostInformation.waite_description)
async def save_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Добавить фотографию к посту?", reply_markup=keyboards.yes_or_no)
    await WaitePostInformation.waite_image_answer.set()


@dp.callback_query_handler(state=WaitePostInformation.waite_image_answer)
async def waite_image_answer(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "cancel":
        await state.finish()
        await callback_query.message.answer("Отменено!")
    await callback_query.message.edit_reply_markup()
    user_data = await state.get_data()
    image_answer = callback_query.data
    if image_answer == "yes":
        await callback_query.message.answer("Отправьте боту изображение:", reply_markup=keyboards.cancel_keyboard)
        await WaitePostInformation.waite_image.set()
    elif callback_query.data == "no":
        users = User.select()
        description = user_data["description"]
        for user in users:
            await bot.send_message(user.user_id, f"{description}")
        await state.finish()


@dp.message_handler(state=WaitePostInformation.waite_image, content_types=types.ContentTypes.PHOTO)
async def save_image_and_post(message: types.Message, state: FSMContext):
    image = message.photo[0].file_id
    user_data = await state.get_data()
    users = User.select()
    description = user_data["description"]
    for user in users:
        try:
            await bot.send_photo(user.user_id, image, f"{description}")
        except Exception as exc:
            logger.info(f'{exc} -- {user.user_id} {user.username} - этот пользователь заблокировал бота')
    await state.finish()


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer('Отменено!')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

