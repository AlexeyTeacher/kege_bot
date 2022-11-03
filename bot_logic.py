import logging
from datetime import datetime
import random

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

from db import session
from config import FIRST, SECOND, FOURTH, FIFTH, END, THREE, ONE, TWO, THIRD, LOG_FORMAT, HELP
from models import User, Statistic, Task, EGENumber, Document, Video

USER_BASE = {}
N_EXAMPLE = ''

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger('app')


def start(update, context):
    """Стартовый диалог. Автоматически запоминает пользователя и добавляет его в словарь."""
    try:
        login = update.message.from_user.name
        old_user = session.query(User).filter(User.login == login).first()
        if old_user is None:
            new_user = User(
                login=login,
                name=update.message.from_user.full_name,
                created_at=datetime.now()
            )
            session.add(new_user)
            session.commit()
        logger.info(f'{login} >>> Начал сеанс')
        keyboard = [
            [
                InlineKeyboardButton("🎞 Видео", callback_data=str(ONE)),
                InlineKeyboardButton("🏋 Задание‍", callback_data=str(TWO)),
            ],
            [
                InlineKeyboardButton("📁 Текстовый разбор", callback_data=str(THREE)),
                InlineKeyboardButton("🆘 Справка", callback_data=str(HELP))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"🦾 Приветствую, *{update.message.from_user.first_name}*! "
            f"Я бот-помощник для подготовки к ЕГЭ по информатике!\n"
            f"Я могу посоветовать видеоразбор или текстовое объяснение одной из задач, а также дать "
            f"упражнение на тренировку\n\n"
            f"🧠 Все задания и текстовые разборы взяты с "
            f"[сайта](https://kpolyakov.spb.ru/school/ege/generate.htm) *К.Ю. Полякова* _(номера заданий совпадают)_\n"
            f"😅 Видео с разборами задач созданы автором чат-бота или взято лучшее из ютуб \n"
            f"🤝 Отдельное спасибо за помощь с доступом к заданиям *Алексею Кабанову* "
            f"и его [сайту kompege](https://kompege.ru/) \n\n"
            f"Выберите на клавиатуре, что вы сейчас хотите 👇", reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def stop(update, context):
    """Принудительный выход из диалога по команде /stop.
    После выполнения сохраняет в базу данных информацию о сессии пользователя"""
    try:
        name = str(update.message.from_user.name)
        old_user = session.query(User).filter(User.login == name).first()
        stat = session.query(Statistic).filter(Statistic.user_id == old_user.id, Statistic.is_right == True).all()
        update.message.reply_text(f'🖖 Всего доброго, {update.message.from_user.first_name}! \n'
                                  f'🤓 Правильно решенных задач: {len(stat)}! \n\n'
                                  f'Если захотите продолжить подготовку к ЕГЭ, нажмите или напишите /start')
        logger.info(f'{name} >>> /stop')
    except Exception as e:
        logger.error(f'{e}')
    return ConversationHandler.END


def end(update, context):
    """Плановый выход из диалога по кнопке "Хватит".
    После выполнения сохраняет в базу данных информацию о сессии пользователя"""
    try:
        query = update.callback_query
        query.answer()
        name = str(query.from_user.name)
        old_user = session.query(User).filter(User.login == name).first()
        stat = session.query(Statistic).filter(Statistic.user_id == old_user.id, Statistic.is_right == True).all()
        query.edit_message_text(text=f'🖖 Всего доброго, {query.from_user.first_name}! \n'
                                     f'🤓 Правильно решенных задач: {len(stat)}! \n\n'
                                     f'Если захотите продолжить подготовку к ЕГЭ, нажмите или напишите /start')
        logger.info(f'{name} >>> Закончил сеанс')
    except Exception as e:
        logger.error(f'{e}')
    return ConversationHandler.END


def draw_keyboard(update):
    """Рисуем клавиатуру с меню"""
    keyboard = [
            [
                InlineKeyboardButton("🎞 Видео", callback_data=str(ONE)),
                InlineKeyboardButton("🏋 Задание‍", callback_data=str(TWO))
            ],
            [
                InlineKeyboardButton("📁 Текстовый разбор", callback_data=str(THREE)),
                InlineKeyboardButton("💔 Хватит", callback_data=str(END)),
            ],
            [InlineKeyboardButton("🆘 Справка", callback_data=str(HELP))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        update.message.reply_text(text="👇 Выбирайте снова 👇", reply_markup=reply_markup)
    except AttributeError as e:
        logger.error(f'{e}')
        update.callback_query.edit_message_text(text="👇 Выбирайте снова 👇", reply_markup=reply_markup)


def run_doc(update, context):
    """Кнопка Документ"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания, текстовый разбор которого вы хотите получить',
                                parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return FIFTH


def doc(update, context):
    """Возвращает текстовый из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_lesson = update.message.text.strip().replace('№', '')
        if number_lesson in [str(i) for i in range(1, 28)]:
            theme = session.query(EGENumber).filter(EGENumber.task_number == int(number_lesson)).first()
            doc_file = session.query(Document).filter(theme.id == Document.number_id).first()
            comment = ['Отличный выбор! 👍', 'Мне тоже нравится это задание! 😻',
                       'Думаю, вам это пригодится! ✍', 'Такое не грех и два раза посмотреть 👌',
                       'Рекомендую читать внимательнее! ✍✍✍']
            update.message.reply_text(f'*{number_lesson}. {theme.title}*. '
                                      f'\n{random.choice(comment)}',
                                      parse_mode='Markdown')
            update.message.reply_text(f'[Скачать файл 💾]({doc_file.url})\n_Разбор взят с сайта К.Ю. Полякова_',
                                      parse_mode='Markdown')
            logger.info(f'{update.message.from_user.name} listen doc № {number_lesson}')

        else:
            update.message.reply_text('Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
        draw_keyboard(update)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def run_video(update, context):
    """Кнопка видео"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания, видео которого вы хотите посмотреть',
                                parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return FOURTH


def video(update, context):
    """Возвращает видео из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_lesson = update.message.text.strip().replace('№', '')
        if number_lesson in [str(i) for i in range(1, 28)]:
            theme = session.query(EGENumber).filter(EGENumber.task_number == int(number_lesson)).first()
            video_file = session.query(Video).filter(theme.id == Video.number_id).first()

            comment = ['Отличный выбор! 👍', 'Мне тоже нравится это видео! 😻',
                       'Думаю, вам это пригодится! ✍', 'Такое не грех и два раза посмотреть 👌',
                       'Рекомендую повторять за видео! ✍✍✍']
            update.message.reply_text(f'*{number_lesson}. {theme.title}*. '
                                      f'\n{random.choice(comment)}\n\n'
                                      f'[видео]({video_file.url})',
                                      parse_mode='Markdown')
            logger.info(f'{update.message.from_user.name} listen video № {number_lesson}')
        else:
            update.message.reply_text('Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
        draw_keyboard(update)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def run_example(update, context):
    """Кнопка задание"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания',
                                parse_mode='Markdown')
    except Exception as e:
        logger.error(f'{e}')
    return SECOND


def example(update, context):
    """Возвращает случайное задание из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_example = update.message.text.strip().replace('№', '')
        if number_example in [str(i) for i in range(1, 28)]:
            login = update.message.from_user.name
            old_user = session.query(User).filter(User.login == login).first()
            if number_example in ['20', '21']:
                number_example = '19'

            query = f"""SELECT 
                          json_agg(f) AS DATA 
                        FROM 
                          (
                            SELECT 
                              t.id, 
                              t.integrator_id, 
                              n.id as number_id,
                              n.task_number, 
                              n.title, 
                              c.name as category, 
                              c.id as category_id,
                              t.text, 
                              t.answer, 
                              t.files 
                            FROM 
                              ege.tasks t 
                              LEFT JOIN ege.ege_numbers n ON t.number_id = n.id 
                              LEFT JOIN ege.categories c ON t.category_id = c.id 
                            WHERE 
                              n.task_number = {number_example}
                            ORDER BY 
                              RANDOM() 
                            LIMIT 
                              1
                          ) f"""
            task = session.execute(query).first()[0][0]
            stat = Statistic(
                user_id=old_user.id,
                number_id=task.get('number_id'),
                category_id=task.get('category_id'),
                task_id=task.get('id'),
                created_at=datetime.now()
            )
            session.add(stat)
            session.commit()

            text = ''
            gif_url = ''
            if '![](https://' in task.get("text"):
                for line in task.get("text").split('\n'):
                    if '![](https://' in line:
                        gif_url = line.replace('![](https://', '').replace('if)', 'if').strip()
                    else:
                        text += line + '\n'
            else:
                text = task.get("text")
            update.message.reply_text(f"*Задание № {task.get('integrator_id')}* \n"
                                      f"*Тема:* {task.get('title')} \n"
                                      f"*Категория:* {task.get('category')} \n\n"
                                      f"{text}",
                                      parse_mode=ParseMode.MARKDOWN)
            if gif_url:
                context.bot.send_photo(update.message.chat_id, gif_url)
            if task.get('files'):
                if number_example == '27':
                    update.message.reply_text(f'[Скачать файл A 💾]({task.get("files")[0].get("url")})\n'
                                              f'[Скачать файл B 💾]({task.get("files")[1].get("url")})',
                                              parse_mode='Markdown')
                else:
                    update.message.reply_text(f'[Скачать файл 💾]({task.get("files")[0].get("url")})',
                                              parse_mode='Markdown')

            if number_example in ['19', '20', '21']:
                update.message.reply_text(f"✍ Напишите *ответы* на все три вопроса.\n"
                                          f"*Формат:* 1) X 2) Y 3) Z\n"
                                          f"Если ответов на какой-то из вопросов несколько, укажите их через *пробел*",
                                          parse_mode='Markdown')
            else:
                update.message.reply_text(f"✍ Напишите *ответ* на задание. "
                                          f"Если ответов несколько, укажите их через *пробел*",
                                          parse_mode='Markdown')
            return THIRD
        else:
            update.message.reply_text('❌ Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
    except Exception as e:
        logger.error(f'{e}')
        draw_keyboard(update)
        return FIRST


def answer(update, context):
    """Проверяет ответ на задание"""
    try:
        user_answer = update.message.text.strip().upper().split()
        old_user = session.query(User).filter(User.login == update.message.from_user.name).first()
        stat = session.query(Statistic).filter(Statistic.user_id == old_user.id
                                               ).order_by(Statistic.created_at.desc()).limit(1).first()
        stat.user_answer = update.message.text.strip().upper()
        task = session.query(Task).filter(Task.id == stat.task_id).first()
        true_answer = task.answer.upper().split()

        if user_answer == true_answer:
            update.message.reply_text(f'🧐 Правильно, так держать!')
            stat.is_right = True
        else:
            update.message.reply_text(f'🚫 Неправильно, ответ: {" ".join(true_answer)}')
            stat.is_right = False
        session.commit()
        draw_keyboard(update)
    except Exception as e:
        logger.error(f'{e}')
    return FIRST


def help_(update, context):
    """Справка"""
    keyboard = [
        [
            InlineKeyboardButton("🎞 Видео", callback_data=str(ONE)),
            InlineKeyboardButton("🏋 Задание‍", callback_data=str(TWO))
        ],
        [
            InlineKeyboardButton("📁 Текстовый разбор", callback_data=str(THREE)),
            InlineKeyboardButton("💔 Хватит", callback_data=str(END)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update.callback_query
    query.answer()
    nums = session.query(EGENumber).order_by(EGENumber.task_number).all()
    text_nums = '\n'.join([f'{n.task_number}. {n.title}' for n in nums])
    text = f"*Привет!*\n" \
           f"ЕГЭ по информатике с 2021 года сдают на компьютере. " \
           f"В отличие  от практических работ на уроках информатики, " \
           f"вам не нужно предоставлять решения самих задач. Нужны только ответы. " \
           f"Если ответов несколько, то их нужно писать *через пробел*. " \
           f"Даже если это несколько строк, то всё-равно пишите через пробелы.\n" \
           f"Все типы задач в боте называются *\"номера\"*, их в этом году *27!*\n" \
           f"В боте можно посмотреть *видео* или прочитать *текстовый разбор* каждого типа задания. " \
           f"Если вы уже изучили тему, то смело решайте задачи. " \
           f"Сами задачи взяты с сайта К.Ю. Полякова (номера заданий совпадают).\n" \
           f"Бот ведет счет правильно решенных задач.\n\n" \
           f"*Номера задач:*\n"\
           f"```\n{text_nums}\n```"\
           f"\n_(Задания 19, 20, 21 объединены в одно, "\
           f"так как это одна задача с тремя вопросами)_\n\n" \
           f"*Помимо кнопок есть текстовые команды:*\n" \
           f"/start - запускает бота после остановки\n" \
           f"/stop - принудительно завершает работу бота"

    query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
