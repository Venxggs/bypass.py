import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from flask import Flask
from threading import Thread

# --- KONFIGURATSIYA ---
API_TOKEN = '8780777165:AAFMcDyoJjAAreB5DhtHrbgJIDwy0qB5EzQ'
LOOTLABS_KEY = '1f806ed103988474dfc8e4061fcb12432e3160c7eb7e7152f6807231447b0b43'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = Flask('')

@app.route('/')
def home():
    return "Bot is running on Lootlabs API!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- LOOTLABS BYPASS FUNKSIYASI ---
async def bypass_link(url):
    # Lootlabs va uning API hamkorlari uchun umumiy endpoint
    # Eslatma: Agar bu endpoint o'zgarsa, faqat URL'ni yangilash kifoya
    api_url = f"https://api.lootlabs.gg/bypass?url={url}&key={LOOTLABS_KEY}"
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            async with session.get(api_url, headers=headers, timeout=25) as response:
                if response.status == 200:
                    data = await response.json()
                    # Lootlabs odatda 'result' ichida linkni qaytaradi
                    if data.get("success") or data.get("status") == "success":
                        return data.get("result") or data.get("destination")
                    return f"Xatolik: {data.get('message', 'Noma\'lum xato')}"
                elif response.status == 401:
                    return "Xatolik: API kalitingiz noto'g'ri yoki faollashtirilmagan."
                elif response.status == 429:
                    return "Xatolik: Limit tugadi (Too many requests)."
                else:
                    # Agar Lootlabs API xato bersa, zaxira tizimga o'tish
                    return "Hozirda API band. Birozdan so'ng urinib ko'ring."
    except Exception as e:
        return f"Xatolik: {str(e)}"

# --- BOT HANDLERLARI ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ **Bot faol!**\n\nMen Platorelay va Linkvertise linklarini bypass qilib beraman.\nLinkni guruhga yoki bu yerga tashlang!")

@dp.message(F.text.contains("auth.platorelay") | F.text.contains("linkvertise") | F.text.contains("loot-link"))
async def handle_platorelay(message: types.Message):
    status_msg = await message.reply("⏳ **Bypass boshlandi, Biroz Kuting.....**")
    
    # Linkni xabardan tozalab olish
    words = message.text.split()
    url = next((w for w in words if "http" in w), None)
            
    if url:
        result = await bypass_link(url)
        # Markdown formatida javob qaytarish
        await status_msg.edit_text(f"✅ **Bypass yakunlandi:**\n\n`{result}`", parse_mode="Markdown")
    else:
        await status_msg.edit_text("Xatolik: Xabardan link topilmadi.")

# --- ISHGA TUSHIRISH ---
async def main():
    Thread(target=run_web).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
