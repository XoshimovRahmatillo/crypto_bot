import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = "8953369399:AAFiOLRIxORb_vbD9HBKpee1xhKUvzta3KA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

COINS = {
    "TON": "the-open-network",
    "BTC": "bitcoin",
    "ETH": "ethereum"
}

user_state = {}  # foydalanuvchi tanlagan coin saqlanadi


async def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.json()
            return data[coin_id]["usd"]


async def get_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return await r.json()


# START
@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="TON", callback_data="TON")],
        [types.InlineKeyboardButton(text="BTC", callback_data="BTC")],
        [types.InlineKeyboardButton(text="ETH", callback_data="ETH")]
    ])

    await message.answer("🚀 Coin tanla:", reply_markup=keyboard)


# COIN TANLASH
@dp.callback_query()
async def coin_select(callback: types.CallbackQuery):
    coin = callback.data
    user_state[callback.from_user.id] = coin

    await callback.message.answer(
        f"💰 {coin} tanlandi\n\n"
        f"Endi summa yoz: masalan 1.5 yoki 10"
    )
    await callback.answer()


# SUMMA KIRITISH
@dp.message()
async def convert(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_state:
        await message.answer("Avval coin tanla: /start")
        return

    try:
        amount = float(message.text)
        coin = user_state[user_id]

        price = await get_price(COINS[coin])
        rates = await get_rates()

        usd = amount * price

        uzs = usd * rates["rates"]["UZS"]
        rub = usd * rates["rates"]["RUB"]
        stars = usd / 0.013

        text = (
            f"💱 {amount} {coin}\n\n"
            f"USD: {usd:.2f}\n"
            f"UZS: {uzs:.2f}\n"
            f"RUB: {rub:.2f}\n"
            f"STARS: {stars:.2f}"
        )

        await message.answer(text)

    except:
        await message.answer("Faqat raqam yoz (masalan 1.5)")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
