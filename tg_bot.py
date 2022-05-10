### modules ###
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from natsort import natsorted, ns
from transliterate import slugify
import requests

import json
import re
from datetime import datetime
import glob
import logging


import parser



TOKEN = '5330557380:AAFE5paJ3iBJXDzWZKO68TwqQalrmQG8ibE'



bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# delete html tags from data
def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>')
    cleantext = re.sub(CLEANR, '\n', str(raw_html))
    return cleantext


def get_floats(text):
    text = cleanhtml(text).split()
    for word in text:
        try:
            word = float(word)
            return word
        except:
            pass


# Start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    global search_val, get_item, search_status
    search_val = False
    get_item = False
    search_status = False
    user_id = message.chat.id
    splited = message.text.split()
    await bot.send_message(message.chat.id, text="HELLO", parse_mode='HTML')
    await bot.send_message(message.chat.id, text='<b>Введите исполнителя или трек для поиска</b>', parse_mode='HTML')

async def more(results, chat_id, names, artists, query, page, art=False):
    for result in results:
        ind = results.index(result)
        print(result)
        await bot.send_audio(chat_id, audio=result, caption=f"name: {names[ind]}\nartist: {artists[ind]}")
    buttons = types.InlineKeyboardMarkup(resize_keyboard=True)
    if art==False:
        buttons.add(types.InlineKeyboardButton(text='Ещё', callback_data=str(chat_id) + "_" + str(page) + "_" + query))
    else:
        buttons.add(types.InlineKeyboardButton(text='Ещё', callback_data=str(chat_id) + "_" + str(page) + "_" + query + '::art'))
    await bot.send_message(chat_id, text='Сделайте выбор', reply_markup=buttons)

### menu_logics ###
@dp.message_handler(content_types=['text'])
async def alphabet(message: types.message):
    results, artists, names, page, query = parser.get_tracks(str.lower(message.text))
    artists_ids, artists_names, artists_tracks = parser.get_artists(query=str.lower(message.text))
    chat_id = message.chat.id
    for artists_name in artists_names:
        buttons = types.InlineKeyboardMarkup(resize_keyboard=True)
        buttons.add(types.InlineKeyboardButton(text='К исполнителю', callback_data=str(chat_id)+"_"+str(artists_ids[artists_names.index(artists_name)])))
        await bot.send_message(chat_id, text=f'name: {artists_name}, count tracks:{artists_tracks[artists_names.index(artists_name)]}', reply_markup=buttons)
    try:
        await more(results, chat_id, names, artists, query, page)
    except:
        await bot.send_message(chat_id, text='Треков не найдено')

@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data
    code = code.split('_', 2)

    if callback_query.data.count('_')==2 and not("::art" in callback_query.data):
        results, artists, names, page, query = parser.get_tracks(str.lower(code[2]), int(code[1])+1)
        try:
            await more(results, code[0], names, artists, query, page)
        except:
            await bot.send_message(code[0], text='Треков больше не найдено')
    else:
        if not("::art" in callback_query.data):
            chat_id = code[0]
            data = code[1]
            print(code)
            tracks_art, artists, names, page = parser.get_art_tracks(data)
        else:
            chat_id = code[0]
            page = code[1]
            query = code[2].replace('::art', '')
            print(code)
            tracks_art, artists, names, page = parser.get_art_tracks(query=query, page=page)
        for track in tracks_art:
            name = str(names[tracks_art.index(track)])
            await bot.send_audio(chat_id, audio=track, caption=f"name: {name}\nartist: {artists[0]}")
        if page[0]>=page[1]:
            await bot.send_message(code[0], text='Треков больше не найдено')



executor.start_polling(dp, skip_updates=True)
