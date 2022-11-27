from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import pandas as pd
from math import pi
import numpy as np
from models import User
from peewee import *


def forming_test_result_pdf(pdf_num, interest, flexibility, confidence, discipline, stunt, goal, plan, environment):
    df = pd.DataFrame({'group': ['A', 'B'],
                       'Окружение': [round(environment, 1) * 10 * 2, 0],
                       'План': [round(plan, 1) * 10 * 2, 0],
                       'Цель': [round(goal, 1) * 10 * 2, 0],
                       'Фокус': [round(stunt, 1) * 10 * 2, 0],
                       'Дисциплина': [round(discipline, 1) * 10 * 2, 0],
                       'Уверенность': [round(confidence, 1) * 10 * 2, 0],
                       'Гибкость': [round(flexibility, 1) * 10 * 2, 0],
                       'Интерес': [round(interest, 1) * 10 * 2, 0]})

    categories = list(df)[1:]
    N = len(categories)
    angles = np.linspace(0, 2 * pi, N, endpoint=False)
    angles_mids = angles + (angles[1] / 2)

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles_mids)
    ax.set_xticklabels(categories)
    ax.xaxis.set_minor_locator(FixedLocator(angles))

    # Draw ylabels
    ax.set_rlabel_position(0)
    ax.set_yticks([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], color="black", size=8)
    ax.set_ylim(0, 100)

    values0 = df.loc[0].drop('group').values
    ax.bar(angles_mids, values0, width=angles[1] - angles[0],
           facecolor='g', alpha=0.7, edgecolor='k', linewidth=1)

    ax.grid(True, axis='x', which='minor')
    ax.grid(False, axis='x', which='major')
    ax.grid(True, axis='y', which='major')

    canvas = Canvas(f"{pdf_num}.pdf", pagesize=A4)

    image = BytesIO()
    fig.savefig(image, format="png")
    image.seek(0)
    image = ImageReader(image)

    canvas.drawImage('./images/8 факторов.JPG', x=75, y=700, height=150, width=450)
    canvas.drawImage(image, x=170, y=170, height=225, width=225)
    canvas.drawImage("./images/таблица2.JPG", x=100, y=70, height=75, width=375)

    pdfmetrics.registerFont(TTFont('Arial Cyr', 'ofont.ru_Arial Cyr.ttf'))
    pdfmetrics.registerFont(TTFont('Arial Cyr Bold', 'Arial Cyr Bold.ttf'))
    canvas.setFont('Arial Cyr Bold', 20)
    canvas.drawString(x=165, y=695, text='ПЕРСОНАЛЬНЫЙ ОТЧЕТ')
    canvas.setFont('Arial Cyr', 17)
    canvas.drawString(x=50, y=630, text='Мне важно, чтобы жизнь каждого человека имела свой плод.')
    canvas.setFont('Arial Cyr Bold', 17)
    canvas.drawString(x=50, y=605, text='Плод')
    canvas.setFont('Arial Cyr', 17)
    canvas.drawString(x=100, y=605, text='- это смысл и результат жизни человека, реализация его')
    canvas.drawString(x=50, y=580, text='призвания. Для того, чтобы это стало возможно, человеку')
    canvas.setFont('Arial Cyr Bold', 17)
    canvas.drawString(x=50, y=555, text='необходимо постоянно расти.')
    canvas.setFont('Arial Cyr', 17)
    canvas.drawString(x=50, y=515, text='В результате анализа более                                с клиентами, я')
    canvas.setFont('Arial Cyr Bold', 17)
    canvas.drawString(x=285, y=515, text='450 коуч-сессий')
    canvas.setFont('Arial Cyr', 17)
    canvas.drawString(x=50, y=490, text='выделила                        которые способствуют быстрому росту.')
    canvas.setFont('Arial Cyr Bold', 17)
    canvas.drawString(x=135, y=490, text='8 факторов,')
    canvas.setFont('Arial Cyr', 17)
    canvas.drawString(x=50, y=450, text='Этот персональный отчет поможет осознать, что        ')
    canvas.setFont('Arial Cyr Bold', 17)
    canvas.drawString(x=445, y=450, text='мешает росту,')
    canvas.setFont('Arial Cyr', 17)
    canvas.drawString(x=50, y=425, text='какие сорняки надо убрать в первую очередь.')

    red = './images/красный.JPG'
    yellow = './images/желтый.JPG'
    green = './images/зеленый.JPG'

    avg_question_1 = round(User.select(fn.AVG(User.quest_1)).scalar(), 1)
    avg_question_2 = round(User.select(fn.AVG(User.quest_2)).scalar(), 1)
    avg_question_3 = round(User.select(fn.AVG(User.quest_3)).scalar(), 1)
    avg_question_4 = round(User.select(fn.AVG(User.quest_4)).scalar(), 1)
    avg_question_5 = round(User.select(fn.AVG(User.quest_5)).scalar(), 1)
    avg_question_6 = round(User.select(fn.AVG(User.quest_6)).scalar(), 1)
    avg_question_7 = round(User.select(fn.AVG(User.quest_7)).scalar(), 1)
    avg_question_8 = round(User.select(fn.AVG(User.quest_8)).scalar(), 1)
    avg_all_question = round(User.select(fn.AVG(User.avg_all_shore)).scalar(), 1)

    if avg_question_1 <= 2:
        canvas.drawImage(red, x=148, y=72.3, height=23.5, width=34.5)
    elif 2.1 <= avg_question_1 <= 3.9:
        canvas.drawImage(yellow, x=148, y=72.3, height=23.5, width=34.5)
    else:
        canvas.drawImage(green, x=148, y=72.3, height=23.5, width=34.5)

    if avg_question_2 <= 2:
        canvas.drawImage(red, x=183.5, y=72.2, height=23.5, width=32)
    elif 2.1 <= avg_question_2 <= 3.9:
        canvas.drawImage(yellow, x=183.5, y=72.2, height=23.5, width=32)
    else:
        canvas.drawImage(green, x=183.5, y=72.2, height=23.5, width=32)

    if avg_question_3 <= 2:
        canvas.drawImage(red, x=217, y=72.3, height=23.5, width=29)
    elif 2.1 <= avg_question_3 <= 3.9:
        canvas.drawImage(yellow, x=217, y=72.3, height=23.5, width=29)
    else:
        canvas.drawImage(green, x=217, y=72.3, height=23.5, width=29)

    if avg_question_4 <= 2:
        canvas.drawImage(red, x=247, y=72.2, height=23.5, width=32.2)
    elif 2.1 <= avg_question_4 <= 3.9:
        canvas.drawImage(yellow, x=247, y=72.2, height=23.5, width=32.2)
    else:
        canvas.drawImage(green, x=247, y=72.2, height=23.5, width=32.2)

    if avg_question_5 <= 2:
        canvas.drawImage(red, x=281, y=72.3, height=23.7, width=37)
    elif 2.1 <= avg_question_5 <= 3.9:
        canvas.drawImage(yellow, x=281, y=72.3, height=23.7, width=37)
    else:
        canvas.drawImage(green, x=281, y=72.3, height=23.7, width=37)

    if avg_question_6 <= 2:
        canvas.drawImage(red, x=319.5, y=72.2, height=23.7, width=38.5)
    elif 2.1 <= avg_question_6 <= 3.9:
        canvas.drawImage(yellow, x=319.5, y=72.2, height=23.7, width=38.5)
    else:
        canvas.drawImage(green, x=319.5, y=72.2, height=23.7, width=38.5)

    if avg_question_7 <= 2:
        canvas.drawImage(red, x=359.7, y=72.3, height=24, width=38)
    elif 2.1 <= avg_question_7 <= 3.9:
        canvas.drawImage(yellow, x=359.7, y=72.3, height=24, width=38)
    else:
        canvas.drawImage(green, x=359.7, y=72.3, height=24, width=38)

    if avg_question_8 <= 2:
        canvas.drawImage(red, x=399, y=72.3, height=24, width=34.5)
    elif 2.1 <= avg_question_8 <= 3.9:
        canvas.drawImage(yellow, x=399, y=72.3, height=24, width=34.5)
    else:
        canvas.drawImage(green, x=399, y=72.3, height=24, width=34.5)

    if round(environment, 1) <= 2:
        canvas.drawImage(red,  x=148, y=97.2, height=26, width=34.5)
    elif 2.1 <= round(environment, 1) <= 3.9:
        canvas.drawImage(yellow,  x=148, y=97.2, height=26, width=34.5)
    else:
        canvas.drawImage(green,  x=148, y=97.2, height=26, width=34.5)
    if round(plan, 1) <= 2:
        canvas.drawImage(red, x=183.5, y=97.2, height=26, width=32)
    elif 2.1 <= round(plan, 1) <= 3.9:
        canvas.drawImage(yellow, x=183.5, y=97.2, height=26, width=32)
    else:
        canvas.drawImage(green, x=183.5, y=97.2, height=26, width=32)
    if round(goal, 1) <= 2:
        canvas.drawImage(red, x=217, y=97.2, height=26, width=29)
    elif 2.1 <= round(goal, 1) <= 3.9:
        canvas.drawImage(yellow, x=217, y=97.2, height=26, width=29)
    else:
        canvas.drawImage(green, x=217, y=97.2, height=26, width=29)
    if round(stunt, 1) <= 2:
        canvas.drawImage(red, x=247, y=97.6, height=26, width=32.4)
    elif 2.1 <= round(stunt, 1) <= 3.9:
        canvas.drawImage(yellow, x=247, y=97.6, height=26, width=32.4)
    else:
        canvas.drawImage(green, x=247, y=97.6, height=26, width=32.4)
    if round(discipline, 1) <= 2:
        canvas.drawImage(red, x=281, y=97.6, height=26, width=37)
    elif 2.1 <= round(discipline, 1) <= 3.9:
        canvas.drawImage(yellow, x=281, y=97.6, height=26, width=37)
    else:
        canvas.drawImage(green, x=281, y=97.6, height=26, width=37)
    if round(confidence, 1) <= 2:
        canvas.drawImage(red, x=319.5, y=97.65, height=25.5, width=38.5)
    elif 2.1 <= round(confidence, 1) <= 3.9:
        canvas.drawImage(yellow, x=319.5, y=97.65, height=25.5, width=38.5)
    else:
        canvas.drawImage(green, x=319.5, y=97.65, height=25.5, width=38.5)
    if round(flexibility, 1) <= 2:
        canvas.drawImage(red, x=359.5, y=97.7, height=25.7, width=38.5)
    elif 2.1 <= round(flexibility, 1) <= 3.9:
        canvas.drawImage(yellow, x=359.5, y=97.7, height=25.7, width=38.5)
    else:
        canvas.drawImage(green, x=359.5, y=97.7, height=25.7, width=38.5)
    if round(interest, 1) <= 2:
        canvas.drawImage(red, x=399, y=97.7, height=25.5, width=34.5)
    elif 2.1 <= round(interest, 1) <= 3.9:
        canvas.drawImage(yellow, x=399, y=97.7, height=25.5, width=34.5)
    else:
        canvas.drawImage(green, x=399, y=97.7, height=25.5, width=34.5)

    canvas.drawString(153, 79, f"{round(avg_question_1 * 2, 1)}")
    canvas.drawString(188, 79, f"{round(avg_question_2 * 2, 1)}")
    canvas.drawString(220, 79, f"{round(avg_question_3 * 2, 1)}")
    canvas.drawString(252, 79, f"{round(avg_question_4 * 2, 1)}")
    canvas.drawString(287, 79, f"{round(avg_question_5 * 2, 1)}")
    canvas.drawString(328, 79, f"{round(avg_question_6 * 2, 1)}")
    canvas.drawString(368, 79, f"{round(avg_question_7 * 2, 1)}")
    canvas.drawString(403, 79, f"{round(avg_question_8 * 2, 1)}")
    canvas.drawString(442, 79, f"{round(avg_all_question * 2, 1)}")
    canvas.drawString(153, 105, f'{round(environment * 2, 1)}')
    canvas.drawString(188, 105, f'{round(plan * 2, 1)}')
    canvas.drawString(220, 105, f'{round(goal * 2, 1)}')
    canvas.drawString(252, 105, f'{round(stunt * 2, 1)}')
    canvas.drawString(287, 105, f'{round(discipline * 2, 1)}')
    canvas.drawString(328, 105, f'{round(confidence * 2, 1)}')
    canvas.drawString(368, 105, f'{round(flexibility * 2, 1)}')
    canvas.drawString(403, 105, f'{round(interest * 2, 1)}')
    average = round((plan + goal + stunt + discipline + confidence + flexibility + interest) * 2 / 8, 1)
    canvas.drawString(442, 105, f'{average}')

    canvas.showPage()
    canvas.setPageSize(A4)

    canvas.drawImage('./images/удобрение.jpg', x=30, y=650, height=150, width=100)
    canvas.drawImage('./images/удобрения.JPG', x=135, y=680, height=65, width=440)
    canvas.drawImage('./images/сорняк.jpg', x=30, y=270, height=150, width=100)
    canvas.drawImage('./images/сорняки.JPG', x=135, y=287, height=80, width=440)

    canvas.setFont('Arial Cyr', 15)

    environment_more = True
    plan_more = True
    goal_more = True
    stunt_more = True
    discipline_more = True
    confidence_more = True
    flexibility_more = True
    interest_more = True

    print(environment, plan, goal, stunt, discipline, confidence, flexibility, interest)

    if round(environment, 1) >= 3:
        environment_more = False
        print('тут1 line_more_1')
        canvas.drawString(x=50, y=630, text='• Люди и среда, способствующие достижению цели, благоприятная почва ')
    elif round(plan, 1) >= 3:
        plan_more = False
        print('тут2 line_more_1')
        canvas.drawString(x=50, y=630, text='• Четкое видение дорожной карты, кратчайшего пути до цели ')
    elif round(goal, 1) >= 3:
        goal_more = False
        print('тут3 line_more_1')
        canvas.drawString(x=50, y=630, text='• Конкретная и вдохновляющая цель, ясный образ желаемого будущего ')
    elif round(stunt, 1) >= 3:
        stunt_more = False
        print('тут4 line_more_1 ')
        canvas.drawString(x=50, y=630, text='• Выверенный приоритет и концентрация во время работы  ')
    elif round(discipline, 1) >= 3:
        discipline_more = False
        print('тут5 line_more_1')
        canvas.drawString(x=50, y=630, text='• Системность режима выполнения маленьких задач, приводящих к цели   ')
    elif round(confidence, 1) >= 3:
        confidence_more = False
        print('тут6 line_more_1')
        canvas.drawString(x=50, y=630,  text='• Твердость намерения и вера в правильность своих решений    ')
    elif round(flexibility, 1) >= 3:
        flexibility_more = False
        print('тут7 line_more_1')
        canvas.drawString(x=50, y=630, text='• Адаптивность и предприимчивость, умение чувствовать момент ')
    elif round(interest, 1) >= 3:
        interest_more = False
        print('тут8 line_more_1')
        canvas.drawString(x=50, y=630, text='• Состояние потока и увлеченности  ')

    if round(plan, 1) >= 3 and plan_more is True:
        plan_more = False
        print('тут2 line_more_2')
        canvas.drawString(x=50, y=605, text='• Четкое видение дорожной карты, кратчайшего пути до цели ')
    elif round(goal, 1) >= 3 and goal_more is True:
        goal_more = False
        print('тут3 line_more_2')
        canvas.drawString(x=50, y=605, text='• Конкретная и вдохновляющая цель, ясный образ желаемого будущего ')
    elif round(stunt, 1) >= 3 and stunt_more is True:
        stunt_more = False
        print('тут4 line_more_2')
        canvas.drawString(x=50, y=605, text='• Выверенный приоритет и концентрация во время работы  ')
    elif round(discipline, 1) >= 3 and discipline_more is True:
        discipline_more = False
        print('тут5 line_more_2')
        canvas.drawString(x=50, y=605, text='• Системность режима выполнения маленьких задач, приводящих к цели   ')
    elif round(confidence, 1) >= 3 and confidence_more is True:
        confidence_more = False
        print('тут6 line_more_2')
        canvas.drawString(x=50, y=605, text='• Твердость намерения и вера в правильность своих решений    ')
    elif round(flexibility, 1) >= 3 and flexibility_more is True:
        flexibility_more = False
        print('тут7 line_more_2')
        canvas.drawString(x=50, y=605, text='• Адаптивность и предприимчивость, умение чувствовать момент ')
    elif round(interest, 1) >= 3 and interest_more is True:
        interest_more = False
        print('тут8 line_more_2')
        canvas.drawString(x=50, y=605, text='• Состояние потока и увлеченности  ')

    if round(goal, 1) >= 3 and goal_more is True:
        goal_more = False
        print('тут3 line_more_3')
        canvas.drawString(x=50, y=580, text='• Конкретная и вдохновляющая цель, ясный образ желаемого будущего ')
    elif round(stunt, 1) >= 3 and stunt_more is True:
        stunt_more = False
        print('тут4 line_more_3')
        canvas.drawString(x=50, y=580, text='• Выверенный приоритет и концентрация во время работы  ')
    elif round(discipline, 1) >= 3 and discipline_more is True:
        discipline_more = False
        print('тут5 line_more_3')
        canvas.drawString(x=50, y=580, text='• Системность режима выполнения маленьких задач, приводящих к цели   ')
    elif round(confidence, 1) >= 3 and confidence_more is True:
        confidence_more = False
        print('тут6 line_more_3')
        canvas.drawString(x=50, y=580, text='• Твердость намерения и вера в правильность своих решений    ')
    elif round(flexibility, 1) >= 3 and flexibility_more is True:
        flexibility = False
        print('тут7 line_more_3')
        canvas.drawString(x=50, y=580, text='• Адаптивность и предприимчивость, умение чувствовать момент ')
    elif round(interest, 1) >= 3 and interest_more is True:
        interest_more = False
        print('тут8 line_more_3')
        canvas.drawString(x=50, y=580, text='• Состояние потока и увлеченности  ')

    if round(stunt, 1) >= 3 and stunt_more is True:
        stunt_more = False
        print('тут4 line_more_4')
        canvas.drawString(x=50, y=555, text='• Выверенный приоритет и концентрация во время работы  ')
    elif round(discipline, 1) >= 3 and discipline_more is True:
        discipline_more = False
        print('тут5 line_more_4')
        canvas.drawString(x=50, y=555, text='• Системность режима выполнения маленьких задач, приводящих к цели   ')
    elif round(confidence, 1) >= 3 and confidence_more is True:
        confidence_more = False
        print('тут6 line_more_4')
        canvas.drawString(x=50, y=555, text='• Твердость намерения и вера в правильность своих решений    ')
    elif round(flexibility, 1) >= 3 and flexibility_more is True:
        flexibility_more = False
        print('тут7 line_more_4')
        canvas.drawString(x=50, y=555, text='• Адаптивность и предприимчивость, умение чувствовать момент ')
    elif round(interest, 1) >= 3 and interest_more is True:
        interest_more = False
        print('тут8 line_more_4')
        canvas.drawString(x=50, y=555, text='• Состояние потока и увлеченности  ')

    if round(discipline, 1) >= 3 and discipline_more is True:
        discipline_more = False
        print('тут5 line_more_5')
        canvas.drawString(x=50, y=530, text='• Системность режима выполнения маленьких задач, приводящих к цели   ')
    elif round(confidence, 1) >= 3 and confidence_more is True:
        confidence_more = False
        print('тут6 line_more_5')
        canvas.drawString(x=50, y=530, text='• Твердость намерения и вера в правильность своих решений    ')
    elif round(flexibility, 1) >= 3 and flexibility_more is True:
        flexibility_more = False
        print('тут7 line_more_5')
        canvas.drawString(x=50, y=530, text='• Адаптивность и предприимчивость, умение чувствовать момент ')
    elif round(interest, 1) >= 3 and interest_more is True:
        interest_more = False
        print('тут8 line_more_5')
        canvas.drawString(x=50, y=530, text='• Состояние потока и увлеченности  ')

    if round(confidence, 1) >= 3 and confidence_more is True:
        confidence_more = False
        print('тут6 line_more_6')
        canvas.drawString(x=50, y=505, text='• Твердость намерения и вера в правильность своих решений    ')
    elif round(flexibility, 1) >= 3 and flexibility_more is True:
        flexibility_more = False
        print('тут7 line_more_6')
        canvas.drawString(x=50, y=505, text='• Адаптивность и предприимчивость, умение чувствовать момент ')
    elif round(interest, 1) >= 3 and interest_more is True:
        interest_more = False
        print('тут8 line_more_6')
        canvas.drawString(x=50, y=505, text='• Состояние потока и увлеченности  ')

    if round(flexibility, 1) >= 3 and flexibility_more is True:
        flexibility_more = False
        print('тут7 line_more_7')
        canvas.drawString(x=50, y=480, text='• Адаптивность и предприимчивость, умение чувствовать момент ')
    elif round(interest, 1) >= 3 and interest_more is True:
        interest_more = False
        print('тут8 line_more_7')
        canvas.drawString(x=50, y=480, text='• Состояние потока и увлеченности  ')

    if round(interest, 1) >= 3 and interest_more is True:
        interest_more = False
        print('тут8 line_more_8')
        canvas.drawString(x=50, y=455, text='• Состояние потока и увлеченности  ')

    print(environment_more, plan_more, stunt_more, goal_more, confidence_more, discipline_more, flexibility_more, interest_more)

    environment_less = True
    plan_less = True
    goal_less = True
    stunt_less = True
    discipline_less = True
    confidence_less = True
    flexibility_less = True
    interest_less = True

    if round(environment, 1) < 3:
        environment_less = False
        canvas.drawString(x=50, y=260, text='• Люди и среда, препятствующие достижению цели / забирающие энергию')
        print('тут1 line_less_1')
    elif round(plan, 1) < 3:
        plan_less = False
        canvas.drawString(x=50, y=260, text='• Расплывчатая дорожная карта до цели')
        print('тут2 line_less_1')
    elif round(goal, 1) < 3:
        goal_less = False
        canvas.drawString(x=50, y=260, text='• Абстрактная / не вдохновляющая цель')
        print('тут3 line_less_1')
    elif round(stunt, 1) < 3:
        stunt_less = False
        canvas.drawString(x=50, y=260, text='• Расфокус и погоня за несколькими зайцами')
        print('тут4 line_less_1')
    elif round(discipline, 1) < 3:
        discipline_less = False
        canvas.drawString(x=50, y=260, text='• Хаотичность и непланомерность в достижении цели')
        print('тут5 line_less_1')
    elif round(confidence, 1) < 3:
        confidence_less = False
        canvas.drawString(x=50, y=260, text='• Колебания в принятии решений / сомнения в победе')
        print('тут6 line_less_1')
    elif round(flexibility, 1) < 3:
        flexibility_less = False
        canvas.drawString(x=50, y=260, text='• Трудность в адаптации к изменениям')
        print('тут6 line_less_1')
    elif round(interest, 1) < 3:
        interest_less = False
        print('тут8 line_less_1')
        canvas.drawString(x=50, y=260, text='• Скука, низкий уровень вдохновения ')

    if round(plan, 1) < 3 and plan_less is True:
        plan_less = False
        print('тут2 line_less_2')
        canvas.drawString(x=50, y=235, text='• Расплывчатая дорожная карта до цели')
    elif round(goal, 1) < 3 and goal_less is True:
        goal_less = False
        print('тут3 line_less_2')
        canvas.drawString(x=50, y=235, text='• Абстрактная / не вдохновляющая цель')
    elif round(stunt, 1) < 3 and stunt_less is True:
        stunt_less = False
        print('тут4 line_less_2')
        canvas.drawString(x=50, y=235, text='• Расфокус и погоня за несколькими зайцами')
    elif round(discipline, 1) < 3 and discipline_less is True:
        discipline_less = False
        print('тут5 line_less_2')
        canvas.drawString(x=50, y=235, text='• Хаотичность и непланомерность в достижении цели')
    elif round(confidence, 1) < 3 and confidence_less is True:
        confidence_less = False
        print('тут6 line_less_2')
        canvas.drawString(x=50, y=235, text='• Колебания в принятии решений / сомнения в победе')
    elif round(flexibility, 1) < 3 and flexibility_less is True:
        flexibility_less = False
        print('тут7 line_less_2')
        canvas.drawString(x=50, y=235, text='• Трудность в адаптации к изменениям')
    elif round(interest, 1) < 3 and interest_less is True:
        interest_less = False
        print('тут8 line_less_2')
        canvas.drawString(x=50, y=235, text='• Скука, низкий уровень вдохновения ')

    if round(goal, 1) < 3 and goal_less is True:
        goal_less = False
        print('тут3 line_less_3')
        canvas.drawString(x=50, y=210, text='• Абстрактная / не вдохновляющая цель')
    elif round(stunt, 1) < 3 and stunt_less is True:
        stunt_less = False
        print('тут4 line_less_3')
        canvas.drawString(x=50, y=210, text='• Расфокус и погоня за несколькими зайцами')
    elif round(discipline, 1) < 3 and discipline_less is True:
        discipline_less = False
        print('тут5 line_less_3')
        canvas.drawString(x=50, y=210, text='• Хаотичность и непланомерность в достижении цели')
    elif round(confidence, 1) < 3 and confidence_less is True:
        confidence_less = False
        print('тут6 line_less_3')
        canvas.drawString(x=50, y=210, text='• Колебания в принятии решений / сомнения в победе')
    elif round(flexibility, 1) < 3 and flexibility_less is True:
        flexibility_less = False
        print('тут7 line_less_3')
        canvas.drawString(x=50, y=210, text='• Трудность в адаптации к изменениям')
    elif round(interest, 1) < 3 and interest_less is True:
        interest_less = False
        print('тут8 line_less_3')
        canvas.drawString(x=50, y=210, text='• Скука, низкий уровень вдохновения ')

    if round(stunt, 1) < 3 and stunt_less is True:
        stunt_less = False
        print('тут4 line_less_4')
        canvas.drawString(x=50, y=185, text='• Расфокус и погоня за несколькими зайцами')
    elif round(discipline, 1) < 3 and discipline_less is True:
        discipline_less = False
        print('тут5 line_less_4')
        canvas.drawString(x=50, y=185, text='• Хаотичность и непланомерность в достижении цели')
    elif round(confidence, 1) < 3 and confidence_less is True:
        confidence_less = False
        print('тут6 line_less_4')
        canvas.drawString(x=50, y=185, text='• Колебания в принятии решений / сомнения в победе')
    elif round(flexibility, 1) < 3 and flexibility_less is True:
        flexibility_less = False
        print('тут7 line_less_4')
        canvas.drawString(x=50, y=185, text='• Трудность в адаптации к изменениям')
    elif round(interest, 1) < 3 and interest_less is True:
        interest_less = False
        print('тут8 line_less_4')
        canvas.drawString(x=50, y=185, text='• Скука, низкий уровень вдохновения ')

    if round(discipline, 1) < 3 and discipline_less is True:
        discipline_less = False
        print('тут5 line_less_5')
        canvas.drawString(x=50, y=160, text='• Хаотичность и непланомерность в достижении цели')
    elif round(confidence, 1) < 3 and confidence_less is True:
        confidence_less = False
        print('тут6 line_less_5')
        canvas.drawString(x=50, y=160, text='• Колебания в принятии решений / сомнения в победе')
    elif round(flexibility, 1) < 3 and flexibility_less is True:
        flexibility_less = False
        print('тут7 line_less_5')
        canvas.drawString(x=50, y=160, text='• Трудность в адаптации к изменениям')
    elif round(interest, 1) < 3 and interest_less is True:
        interest_less = False
        print('тут8 line_less_5')
        canvas.drawString(x=50, y=160, text='• Скука, низкий уровень вдохновения ')

    if round(confidence, 1) < 3 and confidence_less is True:
        confidence_less = False
        print('тут6 line_less_6')
        canvas.drawString(x=50, y=135, text='• Колебания в принятии решений / сомнения в победе')
    elif round(flexibility, 1) < 3 and flexibility_less is True:
        flexibility_less = False
        print('тут7 line_less_6')
        canvas.drawString(x=50, y=135, text='• Трудность в адаптации к изменениям')
    elif round(interest, 1) < 3 and interest_less is True:
        interest_less = False
        print('тут8 line_less_6')
        canvas.drawString(x=50, y=135, text='• Скука, низкий уровень вдохновения ')

    if round(flexibility, 1) < 3 and flexibility_less is True:
        flexibility_less = False
        print('тут7 line_less_7')
        canvas.drawString(x=50, y=110, text='• Трудность в адаптации к изменениям')
    elif round(interest, 1) < 3 and interest_less is True:
        interest_less = False
        print('тут8 line_less_7')
        canvas.drawString(x=50, y=110, text='• Скука, низкий уровень вдохновения ')

    if round(interest, 1) < 3 and interest_less is True:
        print('тут8 line_less_8')
        canvas.drawString(x=50, y=85, text='• Скука, низкий уровень вдохновения ')

    print(environment_less, plan_less, goal_less, stunt_less, discipline_less, confidence_less, flexibility_less, interest_less)

    canvas.showPage()
    canvas.setPageSize(A4)

    canvas.drawImage('./images/описание.JPG', x=45, y=730, height=100, width=520)
    canvas.drawImage('./images/росточек.jpg', x=210, y=-32, height=230, width=200)
    canvas.drawImage('./images/окружение.jpg', x=25, y=670, height=65, width=65)
    canvas.drawImage('./images/план.jpg', x=25, y=600, height=65, width=65)
    canvas.drawImage('./images/цель.jpg', x=25, y=530, height=65, width=65)
    canvas.drawImage('./images/фокус.jpg', x=25, y=460, height=65, width=65)
    canvas.drawImage('./images/дисциплина.jpg', x=25, y=390, height=65, width=65)
    canvas.drawImage('./images/уверенность.jpg', x=25, y=320, height=65, width=65)
    canvas.drawImage('./images/гибкость.jpg', x=25, y=250, height=65, width=65)
    canvas.drawImage('./images/интерес.jpg', x=25, y=180, height=65, width=65)

    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=710, text='Окружение')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=180, y=710, text='- среда, внутри которой находится человек, в т.ч люди, с которыми он')
    canvas.drawString(x=110, y=695,
                      text='чаще всего взаимодействует, ресурсы, к которым имеет доступ. Окружение может быть')
    canvas.drawString(x=110, y=680, text='поддерживающим, то есть содействующим достижению вашей цели, а также,')
    canvas.drawString(x=110, y=665, text='негативным, то есть препятствующим движению к ней.')
    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=625, text='План')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=145, y=625, text='- предварительно обдуманная последовательность действий человека, которая')
    canvas.drawString(x=110, y=610, text='приводит к намеченной цели в заданные сроки.')
    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=570, text='Цель')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=145, y=570, text='– четко сформулированный конечный результат, который соотносится с')
    canvas.drawString(x=110, y=555, text='ценностями человека и вдохновляет его на движение')
    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=510, text='Фокус')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=150, y=510, text='- концентрация на решении конкретной задачи в определенный период')
    canvas.drawString(x=110, y=495, text='времени, а также определение того, что именно наиболее важно в данных')
    canvas.drawString(x=110, y=480, text='обстоятельствах для достижения цели')
    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=435, text='Дисциплина')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=187, y=435, text='– систематичность, постоянство в выполнении регулярных действий,')
    canvas.drawString(x=110, y=420, text='приводящих человека к достижению цели при повторении их продолжительный')
    canvas.drawString(x=110, y=405, text='период времени')
    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=360, text='Уверенность')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=188.5, y=360, text='- свойство личности, ядром которого выступает позитивная оценка')
    canvas.drawString(x=110, y=345,
                      text='собственных навыков, способностей, как достаточных для достижения значимых для')
    canvas.drawString(x=110, y=330, text='него целей')
    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=285, text='Гибкость')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=170, y=285, text='– адаптивность, умение человека приспосабливаться к различным условиям')
    canvas.drawString(x=110, y=270,
                      text='окружающей среды, которая имеет тенденцию меняться, а также, умение извлекать')
    canvas.drawString(x=110, y=255, text='выгоду из происходящих перемен')
    canvas.setFont('Arial Cyr Bold', 12)
    canvas.drawString(x=110, y=220, text='Интерес')
    canvas.setFont('Arial Cyr', 11.5)
    canvas.drawString(x=170, y=220, text='– адаптивность, умение человека приспосабливаться к различным условиям')
    canvas.drawString(x=110, y=205, text='потребностью узнать что-то новое об объекте интереса, повышенным вниманием к')
    canvas.drawString(x=110, y=190,
                      text='нему. Другими словами, увлеченность не только результатом, но и самим процессом')
    canvas.drawString(x=110, y=175, text='движения к цели')

    canvas.showPage()
    canvas.setPageSize(A4)

    canvas.drawImage('./images/деревце.jpg', x=40, y=-130, width=500, height=700)
    canvas.drawImage('./images/что дальше.JPG', x=150, y=750, width=300, height=100)
    canvas.setFont('Arial Cyr', 17)
    canvas.drawString(x=35, y=720, text='После того, как выяснились факторы, препятствующие')
    canvas.drawString(x=35, y=695, text='быстрому роста, есть несколько стратегий:')
    canvas.drawString(x=35, y=650, text='• Работать над удалением сорняков')
    canvas.drawString(x=35, y=625, text='• Работать над усилением своей силы – позитивных факторов')
    canvas.drawString(x=35, y=580, text='Я буду рада поддержать тебя на пути движения к цели в ')
    canvas.drawString(x=35, y=555, text='любой из стратегий.')
    canvas.setFont('Arial Cyr Bold', 17)
    canvas.drawString(x=35, y=505, text='Записывайся на бесплатную диагностику! БОТ поможет :)')

    canvas.save()
