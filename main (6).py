import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram.types import Message, Sticker
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from booot import TOKEN, idishnik, sekret

client_id = idishnik

client_secret = sekret

bot = aiogram.Bot(token=TOKEN)
dp = aiogram.Dispatcher(bot=bot, storage=MemoryStorage())

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("привет пж введи название песни которую ты хоч найти.")


@dp.message_handler(content_types=types.ContentTypes.STICKER)
async def handle_sticker(message: Message):
    await message.answer("класный стикер но музыка важнее)")


@dp.message_handler()
async def search_track(message):
    query = message.text
    results = sp.search(q=query, type='track', limit=1)

    if results['tracks']['items']:
        track_url = results['tracks']['items'][0]['external_urls']['spotify']
        await message.answer(f"Вот ссылка на песню '{query}' в спотифае:\n{track_url}")
    else:
        await message.answer("введи пожалуйсто коректное название песни")


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
