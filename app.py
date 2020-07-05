import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,Dispatcher
from flask import Flask,request
from telegram import Bot,Update,ReplyKeyboardMarkup
from utils import get_reply,fetch_news,topics_Keyboard,Corona_topic
from Corona_cases import get_cases
from city_corona import get_cases_by_city
#enable logging

logging.basicConfig(format='%(asctime)s-%(name)-%(levelname)s-%(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = 'your token'

app = Flask(__name__)

@app.route('/')

def index():
    return "Project is working !"

@app.route(f'/{TOKEN}',methods=['GET','POST'])

def webhook():
    """webhook view which recieves update from telegram"""
    update = Update.de_json(request.get_json(),bot)

    dp.process_update(update)

    return "ok"


def start(bot,update):
    print(update)
    author = update.message.from_user.first_name
    reply = "Hi {} \n How Can I Help you".format(author)
    bot.send_message(chat_id= update.message.chat_id,text=reply)

def news(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text="Choose a category :",
        reply_markup = ReplyKeyboardMarkup(keyboard=topics_Keyboard,one_time_keyboard=True))

def corona_cases(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text="Choose your State :",
        reply_markup = ReplyKeyboardMarkup(keyboard=Corona_topic,one_time_keyboard=True))

def help(bot,update):
    help_text= "Hey I am Help section"
    bot.send_message(chat_id=update.message.chat_id,text = help_text)



def reply_text(bot,update):
    intent,reply = get_reply(update.message.text,update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id,text=article['link'])
    elif intent == "Corona":
        Total,Active,Death,Recoverd = get_cases()
        cases = " 🇮🇳 India: Total  \n Confirmed: {} \n Active: {} \n Deaths: {} \n Recovered: {}".format(Total,Active,Death,Recoverd)
        city = reply.get('geo-state')
        if city is not '':
            City_name,Total_city,Active_city,Death_city,Recoverd_city = get_cases_by_city(city)
            cases_by_city = " In {} Total \n Confirmed: {} \n Active: {} \n Deaths: {} \n Recovered: {}".format(City_name,Total_city,Active_city,Death_city,Recoverd_city)
            final = cases + "\n\n" + cases_by_city
            bot.send_message(chat_id=update.message.chat_id,text=final)
        else:
            bot.send_message(chat_id=update.message.chat_id,text=cases)
    else:
        bot.send_message(chat_id = update.message.chat_id,text=reply)

def echo_stricker(bot,update):
    bot.send_message(chat_id=update.message.chat_id,stricker=update.message.stricker.file_id)


def error(bot,update):
    logger.error("update '%s' caused error '%s'",update,update.error)
    bot.send_message(chat_id=update.message.chat_id,text="Sorry ! Please try something other /n Its Error from Server side")

    
bot = Bot(TOKEN)
try:
    bot.set_webhook("url"+TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot,None)
    
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",help))
dp.add_handler(CommandHandler("news",news))
dp.add_handler(CommandHandler("corona_cases",corona_cases))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker,echo_stricker))

dp.add_error_handler(error)

if __name__ == "__main__":
    app.run(port=8443)

