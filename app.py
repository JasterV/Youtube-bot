import telebot
import time
import pafy
import os
from flask import Flask


bot_token = '837420348:AAEY2WT04zBjpCHYvOzCdy4FHhZf8jX6udE'
bot = telebot.TeleBot(token=bot_token)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome! Send me a youtube video and i will send you an mp3 file!')


@bot.message_handler(func=lambda msg: msg.text is not None and ("youtube.com" in msg.text or "youtu.be" in msg.text))
def send_song(message):
    filename = download_song(message)
    path = os.path.join(os.getcwd(), filename)
    while not os.path.exists(path):
        continue
    bot.send_message(message.chat.id, "Song downloaded")
    song = open(filename, 'rb')
    bot.send_message(message.chat.id, "Sending...")
    bot.send_audio(message.chat.id, song)
    bot.send_message(message.chat.id, "Enjoy it!")
    os.remove(filename)


def download_song(message):
    youtube_url = message.text
    bot.send_message(message.chat.id, "downloading...")
    video = pafy.new(youtube_url)
    bestaudio = video.getbestaudio()
    filename = bestaudio.download()
    return filename


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
