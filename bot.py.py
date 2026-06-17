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

# START MENU
@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="TON", callback_data="TON")],
        [types.InlineKeyboardButton(text="BTC", callback_data="BTC")],
        [types.InlineKeyboardButton(text="ETH", callback_data="ETH")]
    ])

    await message.answer("🚀 Coin tanla:", reply_markup=keyboard)

# BUTTON CLICK
@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    coin = callback.data

    price = await get_price(COINS[coin])
    rates = await get_rates()

    usd = price

    uzs = usd * rates["rates"]["UZS"]
    rub = usd * rates["rates"]["RUB"]

    text = (
        f"💰 {coin}\n\n"
        f"USD: {usd:.2f}\n"
        f"UZS: {uzs:.2f}\n"
        f"RUB: {rub:.2f}"
    )

    await callback.message.answer(text)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
