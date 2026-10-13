import os
import random
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройки
BOT_TOKEN = "8609625925:AAF72Vk5wI1oJJ5_QlztYq6CZqGiZBN3F6w"
DATABASE_URL = os.getenv("DATABASE_URL")  # двухступенчатая проверка

logging.basicConfig(level=logging.INFO)
app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ТЕЛЕГРАМ-БОТ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    # Сюда Render автоматически подставит твой публичный URL сайта, 
    # но пока для теста можно указать заглушку или относительный путь, 
    # когда Render выдаст домен — заменим его.
    builder.button(
        text="🚗 Открыть генератор номеров", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    await message.answer(
        "👋 Привет! Это генератор автономеров Украины, Беларуси и России.\n\n"
        "Нажми кнопку ниже, чтобы запустить приложение:",
        reply_markup=builder.as_markup()
    )

# Фоновая задача для запуска Telegram-бота вместе с FastAPI
@app.on_event("startup")
async def on_startup():
    async def run_bot():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    
    # Запускаем бота асинхронно в фоне
    asyncio.create_task(run_bot())

# --- БАЗОВЫЕ ДАННЫЕ ДЛЯ ГЕНЕРАЦИИ ---
UA_LETTERS = ['AA', 'KA', 'BC', 'HC', 'AE', 'BH', 'BI', 'AX', 'AP', 'CB']
RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
RU_REGIONS = [77, 99, 177, 199, 777, 78, 98, 161, 102, 50, 90, 150]
BY_REGIONS = [1, 2, 3, 4, 5, 6, 7]

@app.get("/api/generate")
def generate_number(country: str, type: str):
    if country == "ua":
        series = random.choice(UA_LETTERS)
        suffix = "".join(random.choices(['AA', 'AB', 'AC', 'BA', 'BB', 'BX'], k=1))
        if type == "regular":
            return {"number": f"{series} {random.randint(1, 9999):04d} {suffix}", "title": "🇺🇦 Украина | Обычный"}
        elif type == "elite":
            d = random.choice([1, 2, 3, 5, 7])
            return {"number": f"AA {str(d)*4} AA", "title": "🇺🇦 Украина | Блатный"}
    elif country == "ru":
        l1 = random.choice(RU_LETTERS)
        l23 = "".join(random.choices(RU_LETTERS, k=2))
        region = random.choice(RU_REGIONS)
        if type == "regular":
            return {"number": f"{l1}{random.randint(1, 999):03d}{l23} {region}", "title": "🇷🇺 Россия | Обычный"}
        elif type == "elite":
            digits = random.choice(["111", "333", "555", "777", "999", "001"])
            return {"number": f"А{digits}АА {region}", "title": "🇷🇺 Россия | Блатный"}
    elif country == "by":
        digits = f"{random.randint(1, 9999):04d}"
        region = random.choice(BY_REGIONS)
        return {"number": f"{digits} AB-{region}", "title": "🇧🇾 Беларусь | Стандарт"}
    
    raise HTTPException(status_code=400, detail="Ошибка параметров")

# --- ВЕБ-ИНТЕРФЕЙС (MINI APP) ---
@app.get("/", response_class=HTMLResponse)
def get_webapp():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Генератор номеров</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white min-h-screen flex flex-col items-center justify-center p-4">
        <div class="w-full max-w-md bg-slate-800 rounded-2xl p-6 shadow-xl border border-slate-700">
            <h1 class="text-2xl font-bold text-center mb-6">🚗 Автономера</h1>
            
            <label class="block text-sm text-slate-400 mb-2">Страна:</label>
            <select id="country" class="w-full bg-slate-700 border border-slate-600 rounded-xl p-3 mb-4 text-white">
                <option value="ua">🇺🇦 Украина</option>
                <option value="ru">🇷🇺 Россия</option>
                <option value="by">🇧🇾 Беларусь</option>
            </select>

            <label class="block text-sm text-slate-400 mb-2">Тип номера:</label>
            <select id="type" class="w-full bg-slate-700 border border-slate-600 rounded-xl p-3 mb-6 text-white">
                <option value="regular">Обычный</option>
                <option value="elite">🔥 Блатный</option>
            </select>

            <button onclick="generate()" class="w-full bg-indigo-600 hover:bg-indigo-500 font-semibold py-3 rounded-xl transition shadow-lg mb-6">
                Сгенерировать
            </button>

            <div id="result-box" class="hidden bg-slate-900 border border-slate-700 rounded-xl p-4 text-center">
                <p id="res-title" class="text-xs text-slate-400 mb-1"></p>
                <p id="res-number" class="text-2xl font-mono font-bold tracking-widest text-emerald-400"></p>
            </div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            async function generate() {
                let country = document.getElementById('country').value;
                let type = document.getElementById('type').value;

                let response = await fetch(`/api/generate?country=${country}&type=${type}`);
                if (response.ok) {
                    let data = await response.json();
                    document.getElementById('res-title').innerText = data.title;
                    document.getElementById('res-number').innerText = data.number;
                    document.getElementById('result-box').classList.remove('hidden');
                    tg.HapticFeedback.impactOccurred('medium');
                }
            }
        </script>
    </body>
    </html>
    """