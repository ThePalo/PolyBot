from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters

import sys
from antlr4 import *
sys.path.append("../cl")
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from EvalVisitor import EvalVisitor

def start(update, context):
    botname = context.bot.username
    missatge = "Hola! Aquest es el bot %s.\n" % (botname)
    missatge += "En aquest bot pots operar amb poligons convexos. Les operacions permeses són: \
    \n/assignPolygon \n/area \n/perimeter \n/numVertices \n/centroid \n/setColor \n/inside \n/equal \
    \n/draw \n/operation \nSi vols saber informació extra pots usar /info."
    context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)


def info(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Bot creat per Gerard Palomares Castells")

def tr(update, context):
    complete_msg = update.message.text
    set_msg = complete_msg.split('\n')

    for msg in set_msg:

        input_stream = InputStream(msg)
        lexer = ExprLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = ExprParser(token_stream)
        tree = parser.root()

        visitor = EvalVisitor(dictionary=context.user_data, buff=True)
        visitor.visit(tree)
        msg_eval = visitor.getMsg()

        if type(msg_eval) is tuple:
            context.bot.send_photo(\
                chat_id=update.message.chat_id,\
                photo=msg_eval[0],\
                caption=msg_eval[1])
        elif type(msg_eval) is str and msg_eval != "":
            context.bot.send_message(chat_id=update.message.chat_id, text=msg_eval)



TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('info', info))

updater.dispatcher.add_handler(MessageHandler(Filters.text, tr))

updater.start_polling()