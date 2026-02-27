import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from flask import Flask
from threading import Thread

# --- KONFIGURATSIYA ---
API_TOKEN = '8780777165:AAHHedUqoviqra8xQggzowB_raAKrQWeh5k'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- RENDER UCHUN WEB SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- BYPASS FUNKSIYASI ---
async def bypass_link(url):
    # API manzili
    api_endpoint = f"https://api.bypass.vip/bypass?url={url}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_endpoint, timeout=20) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("result") or data.get("destination") or "Kalit topilmadi."
                return f"Xatolik: Server status {response.status}"
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# --- BOT HANDLERLARI ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🔗 **Bot guruhlarda ham ishlaydi!**\nPlatorelay linkini yuboring.")

# Guruhda yoki lichkada Platorelay linki bo'lsa ushlab olish
@dp.message(F.text.contains("auth.platorelay"))
async def handle_platorelay(message: types.Message):
    # Avval xabar yuboramiz
    status_msg = await message.reply("⏳ **Bypass boshlandi, Biroz Kuting.....**")
    
    # Linkni xabardan ajratib olish (agar xabarda boshqa so'zlar bo'lsa)
    words = message.text.split()
    link = ""
    for word in words:
        if "auth.platorelay" in word:
            link = word
            break
            
    if link:
        result = await bypass_link(link)
        await status_msg.edit_text(f"✅ **Bypass yakunlandi:**\n\n`{result}`", parse_mode="Markdown")
    else:
        await status_msg.edit_text("Xatolik: Linkni aniqlab bo'lmadi.")

# Boshqa linklar uchun (ixtiyoriy)
@dp.message(F.text.contains("http"))
async def handle_other_links(message: types.Message):
    # Faqat shaxsiy yozishmada yoki botga reply qilinganda ishlashi mumkin
    if message.chat.type == "private":
        status_msg = await message.answer("🔄 **Tekshirilmoqda...**")
        result = await bypass_link(message.text)
        await status_msg.edit_text(f"Natija:\n`{result}`", parse_mode="Markdown")

# --- ISHGA TUSHIRISH ---
async def main():
    Thread(target=run_web).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
