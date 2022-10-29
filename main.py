"""Чат-бот в Telegram. Для запуска нужно открыть специально созданный чат @ege_easy_bot
    или создать свой. Тогда не забудь-те поменять TOKEN на свой"""
import logging
import random
import datetime
from pprint import pprint

import requests
from telegram.ext import Updater, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext import CommandHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from db import session
from models import EGENumber
from video_url import return_url
from config import TOKEN, LOG_FORMAT

with open('log_and_users.txt', 'a', encoding='utf-8') as f:
    f.write(f'{datetime.datetime.now()} >>> Перезапуск приложения\n')

USER_BASE = {}
N_EXAMPLE = ''
# Этапы/состояния разговора
FIRST, SECOND, THIRD, FOURTH, FIFTH = range(5)
# Данные обратного вызова
ONE, TWO, THREE, END = range(4)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger('app')


def start(update, context):
    """Стартовый диалог. Автоматически запоминает пользователя и добавляет его в словарь."""
    try:
        USER_BASE[update.message.from_user.name] = [str(update.message.date)]
        keyboard = [
            [
                InlineKeyboardButton("🎞 Видео", callback_data=str(ONE)),
                InlineKeyboardButton("🏋 Задание‍", callback_data=str(TWO)),
            ],
            [InlineKeyboardButton("📁 Текстовый разбор", callback_data=str(THREE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            f"🦾 Приветствую, *{update.message.from_user.first_name}*! "
            f"Я бот-помощник для подготовки к ЕГЭ по информатике!\n"
            f"Я могу посоветовать видеоразбор или текстовое объяснение одной из задач, а также дать "
            f"упражнение на тренировку\n\n"
            f"*P.S.:*_Все задания и текстовые разборы взяты с сайта К.Ю. Полякова. Видео созданы авторами чат-бота._\n\n"
            f"Выберите на клавиатуре, что вы сейчас хотите 👇", reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> START >>> {e}!\n')
    return FIRST


def stop(update, context):
    """Принудительный выход из диалога по команде /stop.
    После выполнения сохраняет в базу данных информацию о сессии пользователя"""
    try:
        name = str(update.message.from_user.name)
        date = datetime.datetime.now()
        other = '; '.join(USER_BASE[update.message.from_user.name][1:])
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{date} >>> {name} >>> {other}\n')
        update.message.reply_text(f'🖖 Всего доброго, {update.message.from_user.first_name}! \n'
                                  f'🤓 Правильно решенных задач: {other.count("+")}! \n\n'
                                  f'Если захотите продолжить подготовку к ЕГЭ, нажмите или напишите /start')
        USER_BASE.pop(update.message.from_user.name, 'ошибка')
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> STOP >>> {e}!\n')
    return ConversationHandler.END


def end(update, context):
    """Плановый выход из диалога по кнопке "Хватит".
    После выполнения сохраняет в базу данных информацию о сессии пользователя"""
    try:
        query = update.callback_query
        query.answer()
        name = str(query.from_user.name)
        date = datetime.datetime.now()
        other = '; '.join(USER_BASE[query.from_user.name][1:])
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{date} >>> {name} >>> {other}\n')
        query.edit_message_text(text=f'🖖 Всего доброго, {query.from_user.first_name}! \n'
                                     f'🤓 Правильно решенных задач: {other.count("+")}! \n\n'
                                     f'Если захотите продолжить подготовку к ЕГЭ, нажмите или напишите /start')
        USER_BASE.pop(query.from_user.first_name, 'ошибка')
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> END >>>{e}!\n')
    return ConversationHandler.END


def draw_keyboard(update):
    """Рисуем клавиатуру с меню"""
    try:
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
        update.message.reply_text(text="👇 Выбирайте снова 👇", reply_markup=reply_markup)
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> DRAW_KEYBOARD >>>{e}!\n')


def run_doc(update, context):
    """Кнопка Документ"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания, текстовый разбор которого вы хотите получить',
                                parse_mode='Markdown')
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> RUN_DOC >>> {e}!\n')
    return FIFTH


def doc(update, context):
    """Возвращает текстовый из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_lesson = update.message.text.strip().replace('№', '')
        if number_lesson in [str(i) for i in range(1, 28)]:
            USER_BASE[update.message.from_user.name] += [f'Просмотрен текстовый разбор №{number_lesson}']
            result = return_url(int(number_lesson), url_answer='doc')
            comment = ['Отличный выбор! 👍', 'Мне тоже нравится это задание! 😻',
                       'Думаю, вам это пригодится! ✍', 'Такое не грех и два раза посмотреть 👌',
                       'Рекомендую читать внимательнее! ✍✍✍']
            update.message.reply_text(f'*{number_lesson}. {result[0]}*. '
                                      f'\n{random.choice(comment)}',
                                      parse_mode='Markdown')
            update.message.reply_text(f'[Скачать файл 💾]({result[1]})\n_Разбор взят с сайта К.Ю. Полякова_',
                                      parse_mode='Markdown')
        else:
            update.message.reply_text('Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
        draw_keyboard(update)
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> DOC >>> {e}!\n')
    return FIRST


def run_video(update, context):
    """Кнопка видео"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания, видео которого вы хотите посмотреть',
                                parse_mode='Markdown')
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> RUN_VIDEO >>> {e}!\n')
    return FOURTH


def video(update, context):
    """Возвращает видео из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_lesson = update.message.text.strip().replace('№', '')
        if number_lesson in [str(i) for i in range(1, 28)]:
            USER_BASE[update.message.from_user.name] += [f'Просмотрено видео №{number_lesson}']
            result = return_url(int(number_lesson))
            if 'http' not in result[1]:
                update.message.reply_text(f'*{number_lesson}. {result[0]}*. ',
                                          parse_mode='Markdown')
                update.message.reply_text(result[1])
            else:
                comment = ['Отличный выбор! 👍', 'Мне тоже нравится это видео! 😻',
                           'Думаю, вам это пригодится! ✍', 'Такое не грех и два раза посмотреть 👌',
                           'Рекомендую повторять за видео! ✍✍✍']
                update.message.reply_text(f'*{number_lesson}. {result[0]}*. '
                                          f'\n{random.choice(comment)}',
                                          parse_mode='Markdown')
                update.message.reply_text(result[1])
        else:
            update.message.reply_text('Некорректный номер задания, '
                                      'нужно было ввести число от 1 до 27')
        draw_keyboard(update)
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> VIDEO >>> {e}!\n')
    return FIRST


def run_example(update, context):
    """Кнопка задание"""
    try:
        query = update.callback_query
        query.answer()
        query.edit_message_text('Напишите *числом* номер задания',
                                parse_mode='Markdown')
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> RUN_EXAMPLE >>> {e}!\n')
    return SECOND


def example(update, context):
    """Возвращает случайное задание из базы данных по введенному номеру из ЕГЭ"""
    try:
        number_example = update.message.text.strip().replace('№', '')
        if number_example in [str(i) for i in range(1, 28)]:
            USER_BASE[update.message.from_user.name + " N_EXAMPLE"] = number_example
            query = f"""SELECT 
                          json_agg(f) AS DATA 
                        FROM 
                          (
                            SELECT 
                              t.id, 
                              t.integrator_id, 
                              n.task_number, 
                              n.title, 
                              c.name as category, 
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
            logger.info(text)
            logger.info(gif_url)
            update.message.reply_text(f"*Задание № {task.get('integrator_id')}* "
                                      f"Тема: {task.get('title')} \n"
                                      f"Категория: {task.get('category')} \n"
                                      f"{text}",
                                      parse_mode='Markdown')
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

            USER_BASE[update.message.from_user.name + " ANSWER"] = str(task.get('answer')).upper()
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
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> EXAMPLE >>> {e}!\n')
        draw_keyboard(update)
        return FIRST


def answer(update, context):
    """Проверяет ответ на задание"""
    try:
        if update.message.text.strip().upper() == USER_BASE[update.message.from_user.name + " ANSWER"]:
            update.message.reply_text(f'🧐 Правильно, ответ: {USER_BASE[update.message.from_user.name + " ANSWER"]}')
            USER_BASE[update.message.from_user.name] += [
                f'Задача №{USER_BASE[update.message.from_user.name + " N_EXAMPLE"]} +']
        else:
            update.message.reply_text(f'🚫 Неправильно, ответ: {USER_BASE[update.message.from_user.name + " ANSWER"]}')
            USER_BASE[update.message.from_user.name] += [
                f'Задача №{USER_BASE[update.message.from_user.name + " N_EXAMPLE"]} -']

        draw_keyboard(update)
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> ANSWER >>> {e}!\n')
    return FIRST


def main():
    try:
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher

        conv_handler = ConversationHandler(
            # Точка входа в диалог.
            # В данном случае — команда /start. Она задаёт первый вопрос.
            entry_points=[CommandHandler('start', start)],
            states={
                FIRST: [
                    CallbackQueryHandler(run_video, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(run_example, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(run_doc, pattern='^' + str(THREE) + '$'),
                    CallbackQueryHandler(end, pattern='^' + str(END) + '$')
                ],
                SECOND: [MessageHandler(Filters.text, example)],
                THIRD: [MessageHandler(Filters.text, answer)],
                FOURTH: [MessageHandler(Filters.text, video)],
                FIFTH: [MessageHandler(Filters.text, doc)]
            },

            # Точка прерывания диалога. В данном случае — команда /stop.
            fallbacks=[CommandHandler('stop', stop)]
        )
        dp.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()
    except Exception as e:
        with open('log_and_users.txt', 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()} >>> MAIN >>> {e}!\n')


if __name__ == '__main__':
    main()