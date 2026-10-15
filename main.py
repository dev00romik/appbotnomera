import os
import random
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "8609625925:AAF72Vk5wI1oJJ5_QlztYq6CZqGiZBN3F6w"
DATABASE_URL = os.getenv("DATABASE_URL")

# 👑 ТВОЙ TELEGRAM ID АДМИНА
ADMIN_TG_ID = 7271568260

logging.basicConfig(level=logging.INFO)
app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🚗 Играть в нАмерок", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    await message.answer(
        "🔥 **нАмерок // Официальный клиент** 🔥\n\n"
        "Открывай контейнеры, крути госномера, выполняй квесты пути новичка и стань топ-коллекционером мегаполиса!",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@app.on_event("startup")
async def on_startup():
    async def run_bot():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    asyncio.create_task(run_bot())

RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
RU_REGIONS = ['77', '99', '177', '777', '78', '98', '161', '50']
UA_SERIES = ['AA', 'KA', 'BC', 'HC', 'AE', 'BH', 'BI', 'AX', 'AP', 'CB']
BY_LETTERS = ['AB', 'BM', 'CT', 'MH', 'PB', 'OO']
BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7']

@app.get("/api/spin")
def spin_plates(country: str, tier: str = "normal"):
    roll = random.random()
    
    if tier == "elite":
        if roll < 0.05:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1200000
        elif roll < 0.18:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 500000
        elif roll < 0.40:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 200000
        elif roll < 0.65:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 80000
        elif roll < 0.85:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 30000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 10000
    else:
        if roll < 0.01:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1000000
        elif roll < 0.05:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 400000
        elif roll < 0.15:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 150000
        elif roll < 0.35:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 60000
        elif roll < 0.65:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 20000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 5000

    if country == "ru":
        l1 = random.choice(RU_LETTERS)
        l23 = "".join(random.choices(RU_LETTERS, k=2))
        reg = random.choice(RU_REGIONS)
        dig = f"{random.randint(1, 999):03d}" if rarity in ["обычный", "редкий"] else random.choice(["777", "001", "999", "333"])
        number_str = f"{l1} {dig} {l23}"
        region_str = reg
    elif country == "ua":
        series = random.choice(UA_SERIES)
        dig = f"{random.randint(1, 9999):04d}" if rarity in ["обычный", "редкий"] else str(random.choice([1, 7, 9])) * 4
        number_str = f"{series} {dig}"
        region_str = "UA"
    else:
        dig = f"{random.randint(1, 9999):04d}"
        let = random.choice(BY_LETTERS)
        reg = random.choice(BY_REGIONS)
        number_str = f"{dig} {let}"
        region_str = reg

    return {
        "number": number_str,
        "region": region_str,
        "title": title,
        "value": val_mult,
        "country": country,
        "rarity": rarity,
        "color": color
    }

@app.get("/", response_class=HTMLResponse)
def get_webapp():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>нАмерок</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=PT+Sans+Caption:wght@700&display=swap');
            body {
                font-family: 'Inter', sans-serif;
                background-color: #0b0f17;
                color: #f3f4f6;
            }
            .font-plate {
                font-family: 'PT Sans Caption', sans-serif;
            }
            .glass-panel {
                background: rgba(17, 24, 39, 0.75);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            @keyframes grayGlow { 0%, 100% { border-color: #4b5563; box-shadow: 0 0 5px rgba(156,163,175,0.2); } 50% { border-color: #9ca3af; box-shadow: 0 0 15px rgba(156,163,175,0.4); } }
            @keyframes greenGlow { 0%, 100% { border-color: #10b981; box-shadow: 0 0 10px rgba(16,185,129,0.4); } 50% { border-color: #34d399; box-shadow: 0 0 25px rgba(16,185,129,0.8); } }
            @keyframes blueGlow { 0%, 100% { border-color: #3b82f6; box-shadow: 0 0 15px rgba(59,130,246,0.5); } 50% { border-color: #60a5fa; box-shadow: 0 0 30px rgba(59,130,246,0.9); } }
            @keyframes yellowGlow { 0%, 100% { border-color: #eab308; box-shadow: 0 0 20px rgba(234,179,8,0.6); } 50% { border-color: #facc15; box-shadow: 0 0 40px rgba(234,179,8,1); } }
            @keyframes redGlow { 0%, 100% { border-color: #ef4444; box-shadow: 0 0 25px rgba(239,68,68,0.7); } 50% { border-color: #f87171; box-shadow: 0 0 45px rgba(239,68,68,1); } }
            @keyframes purpleGlow { 0%, 100% { border-color: #a855f7; box-shadow: 0 0 30px rgba(168,85,247,0.8); } 50% { border-color: #ec4899; box-shadow: 0 0 60px rgba(236,72,153,1); } }

            .glow-gray { animation: grayGlow 3s infinite; }
            .glow-green { animation: greenGlow 2s infinite; }
            .glow-blue { animation: blueGlow 2s infinite; }
            .glow-yellow { animation: yellowGlow 1.5s infinite; }
            .glow-red { animation: redGlow 1s infinite; }
            .glow-purple { animation: purpleGlow 0.8s infinite; }
        </style>
    </head>
    <body class="min-h-screen flex flex-col select-none pb-24 overflow-x-hidden">
        
        <!-- ВЕРХНЯЯ ШАПКА -->
        <header class="bg-slate-900/90 border-b border-slate-800 p-3 flex justify-between items-center sticky top-0 z-50">
            <div class="flex flex-col">
                <span class="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Баланс</span>
                <span id="balance" class="font-mono font-black text-lg text-emerald-400">1 250 000 ₽</span>
            </div>
            
            <div class="flex items-center gap-2">
                <button id="admin-tab-btn" onclick="switchTab('admin')" class="hidden bg-rose-950/80 border border-rose-500/50 text-rose-400 px-2.5 py-1.5 rounded-xl font-bold text-xs tracking-wider active:scale-95 transition">
                    👑 АДМИН
                </button>
                <div class="text-xs bg-slate-800 px-3 py-1.5 rounded-xl border border-slate-700 text-slate-300 font-bold flex items-center gap-1.5">
                    <span>Ур. <span id="level" class="text-white">1</span></span>
                    <span class="text-slate-600">|</span>
                    <span class="flex items-center text-amber-400">🔥 <span id="energy" class="text-white ml-0.5">0</span></span>
                </div>
                <!-- КНОПКА С ЧЕЛОВЕЧКОМ (ПРОФИЛЬ И МЕНЮ) -->
                <button onclick="switchTab('profile')" id="btn-profile" class="bg-indigo-600 hover:bg-indigo-500 p-2 px-3 rounded-xl border border-indigo-400/50 text-white transition flex items-center gap-1 active:scale-95 shadow-md shadow-indigo-950/50">
                    👤
                </button>
                <button onclick="switchTab('garage')" class="bg-slate-800 hover:bg-slate-700 p-2 rounded-xl border border-slate-700 text-slate-200 transition">
                    ☰
                </button>
            </div>
        </header>

        <!-- ВКЛАДКИ НАВИГАЦИИ -->
        <nav class="flex border-b border-slate-800 bg-slate-900/40 text-xs font-semibold">
            <button onclick="switchTab('game')" id="tab-game-btn" class="flex-1 py-2.5 text-center text-indigo-400 border-b-2 border-indigo-500 transition">🎰 Слоты</button>
            <button onclick="switchTab('garage')" id="tab-garage-btn" class="flex-1 py-2.5 text-center text-slate-400 transition">🚗 Гараж (<span id="garage-count">0</span>)</button>
            <button onclick="switchTab('quests')" id="tab-quests-btn" class="flex-1 py-2.5 text-center text-slate-400 transition">🎯 Квесты</button>
            <button onclick="switchTab('market')" id="tab-market-btn" class="flex-1 py-2.5 text-center text-slate-400 transition">📈 Биржа</button>
        </nav>

        <!-- ВКЛАДКА 1: ИГРОВОЙ ЭКРАН -->
        <div id="tab-game" class="p-4 flex flex-col items-center flex-1 max-w-md mx-auto w-full space-y-3">
            
            <div class="w-full bg-slate-900/80 border border-slate-800 rounded-xl p-2.5 text-center shadow-sm">
                <span class="text-xs text-amber-400 font-bold">🔥 Страна дня: <span id="day-country">Россия</span> • мифик x2</span>
            </div>

            <!-- Путь новичка -->
            <div onclick="switchTab('quests')" class="w-full glass-panel rounded-xl p-3 flex justify-between items-center cursor-pointer hover:border-indigo-500/50 transition">
                <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 font-bold text-xs">🎯</div>
                    <div>
                        <div class="text-xs font-bold text-slate-200">Путь новичка</div>
                        <div class="text-[10px] text-slate-400">Выполни 6 целей и получи легендарный контейнер</div>
                    </div>
                </div>
                <div class="text-xs font-bold text-slate-400 bg-slate-800 px-2 py-1 rounded-lg border border-slate-700">0/6</div>
            </div>

            <div class="w-full glass-panel rounded-xl p-3 flex justify-between items-center">
                <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-lg bg-blue-500/20 border border-blue-500/40 flex items-center justify-center text-blue-400 font-bold text-xs">📅</div>
                    <div>
                        <div class="text-xs font-bold text-slate-200">Ивент «Столичный уикенд»</div>
                        <div class="text-[10px] text-slate-400">Старт в пятницу в 18:00 • через 1 д 1 ч</div>
                    </div>
                </div>
                <span class="text-[10px] font-bold text-slate-400 bg-slate-800/80 px-2 py-1 rounded-lg">скоро</span>
            </div>

            <div class="text-center text-xs text-slate-400 pt-1">Крутите номер</div>

            <!-- НОМЕРНОЙ ЗНАК -->
            <div class="w-full flex justify-center my-2">
                <div id="plate-box" class="relative bg-white text-black border-4 rounded-xl shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300 glow-gray">
                    <div class="flex-1 text-center font-plate font-black text-3xl tracking-wider overflow-hidden">
                        <span id="plate-text">? ????? ?</span>
                    </div>
                    <div class="border-l-2 border-slate-300 pl-3 flex flex-col items-center justify-center min-w-[70px]">
                        <span id="plate-region" class="text-2xl font-plate font-black leading-none text-slate-900">??</span>
                        <div class="flex items-center gap-1 mt-1">
                            <span id="plate-code-text" class="text-[10px] font-bold tracking-widest text-slate-800">RUS</span>
                            <span id="svg-flag" class="text-sm">🇷🇺</span>
                        </div>
                    </div>
                </div>
            </div>

            <div id="info-box" class="text-center text-xs text-slate-400 hidden">
                Нажми «Крутить» внизу: первая крутка бесплатная 🎁
            </div>

            <div class="w-full space-y-3 mt-auto pt-4">
                <div class="flex gap-2">
                    <button class="bg-slate-800/90 border border-slate-700/80 rounded-xl p-3 flex-1 flex justify-between items-center text-xs font-semibold text-slate-300">
                        <span>📦 Обычный</span>
                        <span class="text-slate-500">▼</span>
                    </button>
                    <select id="country-select" class="bg-slate-800/90 border border-slate-700/80 rounded-xl p-3 w-28 text-xs font-semibold text-white focus:outline-none focus:border-indigo-500">
                        <option value="ru">🇷🇺 RU</option>
                        <option value="ua">🇺🇦 UA</option>
                        <option value="by">🇧🇾 BY</option>
                    </select>
                    <button class="bg-slate-800/90 border border-slate-700/80 rounded-xl p-3 px-4 flex items-center justify-center text-slate-300">
                        📍
                    </button>
                </div>

                <button onclick="spin()" class="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-black py-4 rounded-xl shadow-lg shadow-orange-950/40 transition flex items-center justify-center gap-2 active:scale-[0.98]">
                    <span>🎁 Бесплатная крутка • ещё 51</span>
                </button>
            </div>
        </div>

        <!-- ВКЛАДКА: ПРОФИЛЬ / ЧЕЛОВЕЧЕК (НОВАЯ) -->
        <div id="tab-profile" class="p-4 hidden flex-1 max-w-md mx-auto w-full space-y-4">
            <div class="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center gap-4">
                <div class="w-14 h-14 bg-indigo-600/30 border border-indigo-500/50 rounded-2xl flex items-center justify-center text-2xl text-indigo-300">
                    👤
                </div>
                <div>
                    <h2 class="text-base font-bold text-white" id="profile-name">Профиль Игрока</h2>
                    <p class="text-xs text-slate-400">ID: <span id="profile-id">7271568260</span></p>
                    <span class="inline-block mt-1 bg-amber-500/20 text-amber-300 text-[10px] font-bold px-2 py-0.5 rounded-md border border-amber-500/30">
                        VIP Коллекционер
                    </span>
                </div>
            </div>

            <!-- БЫСТРЫЕ КНОПКИ МЕНЮ -->
            <div class="grid grid-cols-2 gap-3">
                <button onclick="switchTab('garage')" class="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col items-center justify-center gap-1 hover:border-indigo-500/50 transition">
                    <span class="text-2xl">🚗</span>
                    <span class="text-xs font-bold text-slate-200">Гараж номеров</span>
                    <span class="text-[10px] text-slate-400"><span id="profile-garage-count">0</span> номеров</span>
                </button>
                
                <button onclick="switchTab('quests')" class="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col items-center justify-center gap-1 hover:border-indigo-500/50 transition">
                    <span class="text-2xl">🎯</span>
                    <span class="text-xs font-bold text-slate-200">Задания и Квесты</span>
                    <span class="text-[10px] text-amber-400 font-bold">6 доступно</span>
                </button>
            </div>

            <!-- СТАТИСТИКАИ -->
            <div class="glass-panel p-4 rounded-xl border border-slate-800 space-y-3">
                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Статистика аккаунта</h3>
                <div class="flex justify-between items-center text-xs">
                    <span class="text-slate-400">Текущий уровень:</span>
                    <span class="font-bold text-white">Ур. <span id="profile-level">1</span></span>
                </div>
                <div class="flex justify-between items-center text-xs">
                    <span class="text-slate-400">Баланс рублей:</span>
                    <span class="font-bold text-emerald-400" id="profile-balance">1 250 000 ₽</span>
                </div>
                <div class="flex justify-between items-center text-xs">
                    <span class="text-slate-400">Пламя / Энергия:</span>
                    <span class="font-bold text-amber-400">🔥 0</span>
                </div>
            </div>
        </div>

        <!-- ВКЛАДКА: КВЕСТЫ (НОВАЯ) -->
        <div id="tab-quests" class="p-4 hidden flex-1 max-w-md mx-auto w-full space-y-3">
            <h2 class="text-sm font-bold text-slate-200 mb-2">🎯 Квесты: Путь новичка</h2>
            
            <div class="glass-panel p-3.5 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                    <div class="text-xs font-bold text-slate-200">Сделать первую крутку</div>
                    <div class="text-[10px] text-emerald-400">+50 000 ₽</div>
                </div>
                <button class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-3 py-1.5 rounded-lg text-xs">Выполнить</button>
            </div>

            <div class="glass-panel p-3.5 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                    <div class="text-xs font-bold text-slate-200">Выбить редкий номер (Зеленый)</div>
                    <div class="text-[10px] text-emerald-400">+150 000 ₽</div>
                </div>
                <span class="text-xs text-slate-500 font-bold">0/1</span>
            </div>

            <div class="glass-panel p-3.5 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                    <div class="text-xs font-bold text-slate-200">Продать номер на бирже</div>
                    <div class="text-[10px] text-emerald-400">+100 000 ₽</div>
                </div>
                <span class="text-xs text-slate-500 font-bold">0/1</span>
            </div>
        </div>

        <!-- ВКЛАДКА 2: ГАРАЖ -->
        <div id="tab-garage" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <h2 class="text-sm font-bold text-slate-200 mb-4">Ваш гараж номеров</h2>
            <div id="garage-list" class="space-y-3">
                <div class="text-center text-slate-500 py-12 text-xs">Гараж пуст. Начните крутить номера!</div>
            </div>
        </div>

        <!-- ВКЛАДКА 3: БИРЖА -->
        <div id="tab-market" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <h2 class="text-sm font-bold text-slate-200 mb-1">Рынок и Биржа</h2>
            <p class="text-xs text-slate-400 mb-4">Покупайте редкие экземпляры у других игроков.</p>
            <div id="market-list" class="space-y-3"></div>
        </div>

        <!-- ВКЛАДКА 4: АДМИН-ПАНЕЛЬ -->
        <div id="tab-admin" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <div class="glass-panel p-5 rounded-2xl border border-rose-500/40">
                <div class="flex items-center gap-2 mb-4">
                    <span class="text-xl">👑</span>
                    <h2 class="text-sm font-black text-rose-400">ТЕРМИНАЛ АДМИНИСТРАТОРА</h2>
                </div>
                <p class="text-xs text-slate-400 mb-4">Доступ разрешен для ID: <code class="text-rose-300 font-bold">__ADMIN_ID__</code></p>
                
                <div class="space-y-3">
                    <div>
                        <label class="block text-[10px] text-slate-400 mb-1">ТЕЛЕГРАМ ID ИГРОКА:</label>
                        <input id="admin-target-id" type="number" value="7271568260" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs">
                    </div>
                    <div>
                        <label class="block text-[10px] text-slate-400 mb-1">СУММА В РУБЛЯХ (₽):</label>
                        <input id="admin-money-amount" type="number" value="500000" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs">
                    </div>
                    <button onclick="adminGiveMoney()" class="w-full bg-emerald-600/30 border border-emerald-500/60 text-emerald-300 font-bold py-3 rounded-xl text-xs transition">
                        Начислить рубли по ID
                    </button>

                    <hr class="border-slate-800 my-2">

                    <div>
                        <label class="block text-[10px] text-slate-400 mb-1">НОМЕРНОЙ ЗНАК:</label>
                        <input id="admin-plate-num" type="text" placeholder="А777АА" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs mb-2">
                        <label class="block text-[10px] text-slate-400 mb-1">РЕДКОСТЬ:</label>
                        <select id="admin-plate-rarity" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs mb-3">
                            <option value="обычный">Обычный (Серый)</option>
                            <option value="редкий">Редкий (Зеленый)</option>
                            <option value="сверхредкий">Сверхредкий (Синий)</option>
                            <option value="легендарный">Легендарный (Желтый)</option>
                            <option value="мифический">Мифический (Красный)</option>
                            <option value="мистический">Мистический (Пурпурный)</option>
                        </select>
                    </div>
                    <button onclick="adminGiveCustomPlate()" class="w-full bg-purple-600/30 border border-purple-500/60 text-purple-300 font-bold py-3 rounded-xl text-xs transition">
                        Выдать кастомный номер
                    </button>
                </div>
            </div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            const ADMIN_ID = __ADMIN_ID__;
            let currentUserTgId = tg.initDataUnsafe?.user?.id || 7271568260;

            if (currentUserTgId === ADMIN_ID) {
                document.getElementById('admin-tab-btn').classList.remove('hidden');
            }

            let state = {
                balance: 1250000,
                level: 1,
                energy: 0,
                garage: [],
                market: [
                    { id: 1, number: "А777АА", region: "777", title: "🔥 МИФИЧЕСКИЙ НОМЕР", price: 500000, seller: "Игрок #812", rarity: "мифический", color: "red" },
                    { id: 2, number: "В111ВВ", region: "78", title: "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", price: 250000, seller: "Москвич", rarity: "легендарный", color: "yellow" }
                ]
            };

            function updateUI() {
                document.getElementById('balance').innerText = state.balance.toLocaleString('ru-RU') + ' ₽';
                document.getElementById('level').innerText = state.level;
                document.getElementById('energy').innerText = state.energy;
                document.getElementById('garage-count').innerText = state.garage.length;
                document.getElementById('profile-garage-count').innerText = state.garage.length;
                document.getElementById('profile-balance').innerText = state.balance.toLocaleString('ru-RU') + ' ₽';
                document.getElementById('profile-level').innerText = state.level;
                renderGarage();
                renderMarket();
            }

            function switchTab(tab) {
                ['game', 'garage', 'quests', 'market', 'profile', 'admin'].forEach(t => {
                    let el = document.getElementById(`tab-${t}`);
                    let btn = document.getElementById(`tab-${t}-btn`);
                    if (el) el.classList.add('hidden');
                    if (btn) btn.className = "flex-1 py-2.5 text-center text-slate-400 transition";
                });
                
                let target = document.getElementById(`tab-${tab}`);
                if (target) target.classList.remove('hidden');
                let activeBtn = document.getElementById(`tab-${tab}-btn`);
                if (activeBtn) activeBtn.className = "flex-1 py-2.5 text-center text-indigo-400 border-b-2 border-indigo-500 transition font-bold";
            }

            function updatePlateVisual(country, numberText, regionText, colorClass) {
                let plateBox = document.getElementById('plate-box');
                let codeText = document.getElementById('plate-code-text');
                let svgFlag = document.getElementById('svg-flag');
                
                plateBox.className = `relative bg-white text-black border-4 rounded-xl shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300 glow-${colorClass}`;
                document.getElementById('plate-text').innerText = numberText;
                document.getElementById('plate-region').innerText = regionText;

                if (country === 'ru') {
                    codeText.innerText = 'RUS';
                    svgFlag.innerText = '🇷🇺';
                } else if (country === 'ua') {
                    codeText.innerText = 'UA';
                    svgFlag.innerText = '🇺🇦';
                } else if (country === 'by') {
                    codeText.innerText = 'BY';
                    svgFlag.innerText = '🇧🇾';
                }
            }

            document.getElementById('country-select').addEventListener('change', (e) => {
                let c = e.target.value;
                if (c === 'ru') updatePlateVisual('ru', 'А 777 АА', '777', 'yellow');
                else if (c === 'ua') updatePlateVisual('ua', 'AA 7777', 'UA', 'yellow');
                else if (c === 'by') updatePlateVisual('by', '7777 AB', '7', 'blue');
            });

            async function spin() {
                let country = document.getElementById('country-select').value;
                let infoBox = document.getElementById('info-box');

                let counter = 0;
                let interval = setInterval(() => {
                    let randNum = Math.floor(100 + Math.random() * 900);
                    updatePlateVisual(country, `Х ${randNum} ХХ`, '99', 'gray');
                    counter++;
                    if (counter > 10) clearInterval(interval);
                }, 40);

                let response = await fetch(`/api/spin?country=${country}&tier=normal`);
                if (response.ok) {
                    let data = await response.json();
                    setTimeout(() => {
                        updatePlateVisual(country, data.number, data.region, data.color);
                        infoBox.classList.remove('hidden');

                        state.garage.unshift(data);
                        updateUI();
                        tg.HapticFeedback?.notificationOccurred('success');
                    }, 500);
                }
            }

            function renderGarage() {
                let list = document.getElementById('garage-list');
                if (state.garage.length === 0) {
                    list.innerHTML = '<div class="text-center text-slate-500 py-12 text-xs">Гараж пуст. Начните крутить номера!</div>';
                    return;
                }
                list.innerHTML = state.garage.map((item, index) => `
                    <div class="glass-panel p-3.5 rounded-xl flex justify-between items-center border glow-${item.color}">
                        <div>
                            <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400">${item.title}</span>
                            <div class="text-base font-plate font-black text-white mt-0.5">${item.number} | ${item.region}</div>
                            <span class="text-xs text-emerald-400 font-semibold">Цена: ${item.value.toLocaleString('ru-RU')} ₽</span>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="sellItem(${index})" class="bg-emerald-600/20 border border-emerald-500/40 text-emerald-300 px-2.5 py-1.5 rounded-lg text-xs font-bold transition">Продать</button>
                            <button onclick="listToMarket(${index})" class="bg-indigo-600/20 border border-indigo-500/40 text-indigo-300 px-2.5 py-1.5 rounded-lg text-xs font-bold transition">Биржа</button>
                        </div>
                    </div>
                `).join('');
            }

            function sellItem(index) {
                let item = state.garage[index];
                state.balance += item.value;
                state.garage.splice(index, 1);
                updateUI();
                tg.HapticFeedback?.impactOccurred('medium');
            }

            function listToMarket(index) {
                let item = state.garage[index];
                state.market.unshift({
                    id: Date.now(),
                    number: item.number,
                    region: item.region,
                    title: item.title,
                    price: Math.round(item.value * 1.25),
                    seller: "Вы",
                    color: item.color
                });
                state.garage.splice(index, 1);
                updateUI();
                alert("Номер успешно выставлен на биржу!");
            }

            function renderMarket() {
                let list = document.getElementById('market-list');
                list.innerHTML = state.market.map((item, index) => `
                    <div class="glass-panel p-3.5 rounded-xl flex justify-between items-center border border-slate-800">
                        <div>
                            <span class="text-[10px] text-slate-400">Продавец: ${item.seller}</span>
                            <div class="text-base font-plate font-black text-amber-400 mt-0.5">${item.number} | ${item.region}</div>
                            <span class="text-xs text-slate-300">${item.title}</span>
                        </div>
                        <div class="text-right">
                            <div class="text-emerald-400 font-bold mb-1 text-xs">${item.price.toLocaleString('ru-RU')} ₽</div>
                            ${item.seller !== "Вы" ? `<button onclick="buyMarketItem(${index})" class="bg-indigo-600 hover:bg-indigo-500 px-3 py-1 rounded-lg text-xs font-bold transition">Купить</button>` : `<span class="text-[10px] text-slate-500">Ваш лот</span>`}
                        </div>
                    </div>
                `).join('');
            }

            function buyMarketItem(index) {
                let item = state.market[index];
                if (state.balance < item.price) {
                    alert("Недостаточно средств на балансе!");
                    return;
                }
                state.balance -= item.price;
                state.garage.unshift({ number: item.number, region: item.region, title: item.title, value: item.price, color: item.color || 'blue' });
                state.market.splice(index, 1);
                updateUI();
                tg.HapticFeedback?.notificationOccurred('success');
            }

            function adminGiveMoney() {
                let targetId = document.getElementById('admin-target-id').value;
                let amount = parseInt(document.getElementById('admin-money-amount').value) || 0;
                state.balance += amount;
                updateUI();
                alert(`Админ: успешно начислено ${amount.toLocaleString('ru-RU')} ₽ для ID ${targetId}!`);
            }

            function adminGiveCustomPlate() {
                let num = document.getElementById('admin-plate-num').value.trim() || "А777АА";
                let rarity = document.getElementById('admin-plate-rarity').value;
                
                let colorMap = { "обычный": "gray", "редкий": "green", "сверхредкий": "blue", "легендарный": "yellow", "мифический": "red", "мистический": "purple" };
                let color = colorMap[rarity] || "blue";

                state.garage.unshift({
                    number: num,
                    region: "777",
                    title: `👑 ЭКСКЛЮЗИВ (${rarity.toUpperCase()})`,
                    value: rarity === 'мистический' ? 1000000 : 300000,
                    color: color
                });
                updateUI();
                alert(`Номер "${num}" (${rarity}) успешно выдан в гараж!`);
            }

            updateUI();
            updatePlateVisual('ru', 'А 777 АА', '777', 'yellow');
        </script>
    </body>
    </html>
    """
    return html_content.replace("__ADMIN_ID__", str(ADMIN_TG_ID))