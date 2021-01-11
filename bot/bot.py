from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ParseMode

import sys
from antlr4 import *
sys.path.append("../cl")
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from EvalVisitor import EvalVisitor

def start(update, context):
    botname = context.bot.username
    missatge = "Hola! Aquest es el bot %s.\n" % (botname)
    missatge += "En aquest bot pots operar amb polígons convexos. Les operacions permeses són les especificades per la gramàtica del programa: \
            \n - var := _polígon_ ➡ Asigna un polígon convex a una variable.\
            \n - print _polígon_ OR \"_text_\" ➡ printa un polígon o un text.\
            \n - area _polígon_ ➡ àrea del polígon.\
            \n - perimeter _polígon_ ➡ perímetre del polígon.\
            \n - vertices _polígon_ ➡ # de vèrtex del polígon.\
            \n - centroid _polígon_ ➡ centroid del polígon.\
            \n - color _var_, _{0, 1, 0.5}_ ➡ assigna un color al polígon de la variable.\
            \n - inside _polígon1_, _polígon2_ ➡ indica si el polígon 1 està a dintre del 2.\
            \n - equal _polígon1_, _polígon2_ ➡ indica si els dos polígons són iguals.\
            \n - draw _output_, _polígons_ ➡ dibuixa els polígons (seprarats per comes) en un fitxer _output_.\
            \n - operacions ➡ els polígons es poden operar per a formar nous polígons.\
            \n    - _polígon1_ + _polígon2_ ➡ unió convexa dels dos polígons.\
            \n    - _polígon1_ \* _polígon2_ ➡ intersecció dels dos polígons.\
            \n    - # _polígon_ ➡ bounding box del polígon.\
            \n    - _!n_ ➡ retorna un polígon convex format amb n punts random entre ([[0,1]]²).\
            \n Per a definir un polígon es poden usar les operacions o indicant els punts en el format [[x1 y1 x2 y2 ... xn yn]]\
            \n Si vols tornar a veure aquest missatge, usa /start. Si vols tenir més informació sobre el bot, usa /info"
    context.bot.send_message(chat_id=update.effective_chat.id, text=missatge, parse_mode=ParseMode.MARKDOWN)


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