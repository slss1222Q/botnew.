import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Ma'lumotlaringiz
API_TOKEN = "8631752606:AAFc7dYPA5oWH-EPku1bNZMRN1xkqPE756c"
ADMIN_ID = 8638691846
# Siz bergan kanallar
MANDATORY_CHANNELS = ["@footnewsuz", "-1002047805218"] # Biri username, ikkinchisi ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# SQLite bazasi
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
cursor.execute("INSERT OR IGNORE INTO settings VALUES ('welcome_text', 'Xush kelibsiz! Futbolni ko''rish uchun quyidagi kanallarga obuna bo''ling.')")
conn.commit()

async def check_sub(user_id):
    for ch in MANDATORY_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False, ch
        except: continue
    return True, None

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1-kanalga obuna", url="https://t.me/footnewsuz")],
        [InlineKeyboardButton(text="2-kanalga obuna", url="https://t.me/+syFFOzTeWUY5NDc0")],
        [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check")]
    ])
    await message.answer("Xush kelibsiz! Futbolni ko'rish uchun kanallarga obuna bo'ling.", reply_markup=kb)

@dp.callback_query(F.data == "check")
async def check(callback: types.CallbackQuery):
    is_subbed, ch = await check_sub(callback.from_user.id)
    if is_subbed:
        # Siz so'ragan maxsus xabar
        text = ("Tabriklaymiz! Endi siz futbolni bemalol ko'rishingiz mumkin.\n\n"
                "UZ TV LIVE botiga o'tib, O'zbekiston va Portugaliya o'yinini tomosha qiling: @uztvlivebot")
        await callback.message.answer(text)
    else:
        await callback.answer(f"❌ Siz {ch} kanaliga hali obuna bo'lmagansiz!", show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())