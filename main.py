import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, Updater

from config import TOKEN, LOG_FORMAT, FIFTH, SECOND, THIRD, FOURTH, END, THREE, TWO, ONE, FIRST, HELP
from bot_logic import stop, doc, video, answer, example, end, run_video, run_example, run_doc, start, help_

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger('app')
from db import db_init


def main():
    logger.info('restart app')

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
                CallbackQueryHandler(help_, pattern='^' + str(HELP) + '$'),
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


if __name__ == '__main__':
    try:
        db_init()
        main()
    except Exception as e:
        logger.error(f'MAIN {e}')
