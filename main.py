import os
import random
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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
    # Кнопка в самом чате (Reply Keyboard)
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.button(
        text="🚗 Играть в нАмерок", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    reply_markup = reply_builder.as_markup(resize_keyboard=True)

    # Инлайн кнопка в сообщении
    inline_builder = InlineKeyboardBuilder()
    inline_builder.button(
        text="🎮 Запустить игру", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )

    await message.answer(
        "🔥 **нАмерок 2100 // Официальный клиент** 🔥\n\n"
        "Нажми на кнопку **«🚗 Играть в нАмерок»** внизу чата, чтобы открыть игру!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

@app.on_event("startup")
async def on_startup():
    async def run_bot():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    asyncio.create_task(run_bot())

RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
RU_ALL_REGIONS = ['77', '99', '177', '199', '777', '799', '78', '98', '178', '198', '50', '90', '150', '161', '125']

UA_OBLASTS = ['AA', 'KA', 'BC', 'HC', 'AE', 'BH', 'BI', 'AX', 'AP', 'CB', 'AM', 'AO', 'BX']
UA_SUFFIXES = ['AA', 'AB', 'AC', 'BA', 'BB', 'BX', 'CB', 'CE']

BY_LETTERS = ['AB', 'BM', 'CT', 'MH', 'PB', 'OO', 'AK', 'BI']
BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7']

@app.get("/api/spin")
def spin_plates(country: str, region: str = "auto", tier: str = "normal"):
    roll = random.random()
    
    # Расчет вероятностей по уровням круток
    if tier == "legendary":
        # Легендарная крутка (15 000 ₽)
        if roll < 0.0033: # 0.33% Мистический
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 2000000
        elif roll < 0.05:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 800000
        elif roll < 0.20:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 300000
        elif roll < 0.50:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 100000
        else:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 45000
    elif tier == "rare":
        # Редкая крутка (5 000 ₽)
        if roll < 0.001:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1200000
        elif roll < 0.02:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 500000
        elif roll < 0.10:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 200000
        elif roll < 0.35:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 75000
        elif roll < 0.70:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 25000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 8000
    else:
        # Обычная крутка (1 000 ₽) - заниженные шансы
        if roll < 0.0005:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1000000
        elif roll < 0.008:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 350000
        elif roll < 0.05:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 120000
        elif roll < 0.20:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 45000
        elif roll < 0.50:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 15000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 4000

    if country == "ru":
        l1 = random.choice(RU_LETTERS)
        digits = f"{random.randint(1, 999):03d}" if rarity in ["обычный", "редкий"] else random.choice(["777", "001", "999", "333", "555"])
        l23 = "".join(random.choices(RU_LETTERS, k=2))
        reg = region if region != "auto" else random.choice(RU_ALL_REGIONS)
        number_str = f"{l1} {digits} {l23}"
        region_str = reg
    elif country == "ua":
        oblast = region if region != "auto" else random.choice(UA_OBLASTS)
        digits = f"{random.randint(1, 9999):04d}" if rarity in ["обычный", "редкий"] else str(random.choice([1, 7, 9])) * 4
        suf = random.choice(UA_SUFFIXES)
        number_str = f"{oblast} {digits} {suf}"
        region_str = "UA"
    else:
        digits = f"{random.randint(1, 9999):04d}" if rarity in ["обычный", "редкий"] else str(random.choice([7, 5, 9])) * 4
        let = random.choice(BY_LETTERS)
        reg = region if region != "auto" else random.choice(BY_REGIONS)
        number_str = f"{digits} {let}-{reg}"
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
        <title>нАмерок 2100</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=PT+Sans+Caption:wght@700&display=swap');
            body {
                font-family: 'Inter', sans-serif;
                background-color: #0b0f17;
                color: #f3f4f6;
            }
            .font-plate { font-family: 'PT Sans Caption', sans-serif; }
            .glass-panel {
                background: rgba(17, 24, 39, 0.85);
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

            #toast {
                transition: all 0.3s ease;
                transform: translateY(-100%);
                opacity: 0;
            }
            #toast.show {
                transform: translateY(0);
                opacity: 1;
            }
        </style>
    </head>
    <body class="min-h-screen flex flex-col select-none pb-8 overflow-x-hidden">
        
        <!-- ВНУТРИИГРОВОЙ TOAST -->
        <div id="toast" class="fixed top-4 left-1/2 -translate-x-1/2 z-50 pointer-events-none w-11/12 max-w-md">
            <div id="toast-body" class="bg-slate-900/95 border border-indigo-500/50 p-3.5 rounded-2xl shadow-2xl flex items-center gap-3 backdrop-blur-md">
                <span id="toast-icon" class="text-xl">🔔</span>
                <span id="toast-msg" class="text-xs font-bold text-slate-100 flex-1">Сообщение</span>
            </div>
        </div>

        <!-- ВЕРХНЯЯ ШАПКА -->
        <header class="bg-slate-900/90 border-b border-slate-800 p-3 flex justify-between items-center sticky top-0 z-40">
            <div class="flex flex-col">
                <span class="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Баланс</span>
                <span id="balance" class="font-mono font-black text-lg text-emerald-400">1 250 000 ₽</span>
            </div>
            
            <div class="flex items-center gap-2">
                <div class="text-xs bg-slate-800 px-3 py-1.5 rounded-xl border border-slate-700 text-slate-300 font-bold flex items-center gap-1.5">
                    <span>Ур. <span id="level" class="text-white">1</span></span>
                    <span class="text-slate-600">|</span>
                    <span class="text-[10px] text-indigo-400"><span id="exp">0</span>/<span id="max-exp">100</span> EXP</span>
                </div>
                <button onclick="showView('profile')" class="bg-indigo-600 hover:bg-indigo-500 p-2 px-3 rounded-xl border border-indigo-400/50 text-white transition flex items-center gap-1 active:scale-95 shadow-md">
                    👤 Меню
                </button>
            </div>
        </header>

        <!-- ЭКРАН 1: СЛОТЫ И КРУТКА -->
        <div id="view-slots" class="p-4 flex flex-col flex-1 max-w-md mx-auto w-full space-y-4">
            
            <div class="w-full bg-slate-900/80 border border-slate-800 rounded-xl p-2.5 text-center flex justify-between items-center px-4">
                <span class="text-xs text-amber-400 font-bold">🔥 Страна дня: Россия • мифик x2</span>
                <span class="text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded font-bold">БОНУС</span>
            </div>

            <!-- РЕАЛИСТИЧНЫЙ НОМЕРНОЙ ЗНАК -->
            <div class="w-full flex justify-center my-2">
                <div id="plate-box" class="relative bg-white text-black border-4 rounded-xl shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300 glow-gray">
                    
                    <div class="flex-1 text-center font-plate font-black text-2xl tracking-wider overflow-hidden">
                        <span id="plate-text">А 777 АА</span>
                    </div>

                    <div id="region-block" class="border-l-2 border-slate-300 pl-2.5 flex flex-col items-center justify-center min-w-[65px]">
                        <span id="plate-region" class="text-2xl font-plate font-black leading-none text-slate-900">777</span>
                        <div class="flex items-center gap-1 mt-1">
                            <span id="plate-code-text" class="text-[9px] font-bold tracking-widest text-slate-800">RUS</span>
                            <div id="svg-flag-box" class="w-5 h-3.5 rounded-sm overflow-hidden border border-slate-400 shadow-sm flex items-center justify-center"></div>
                        </div>
                    </div>

                    <div id="ua-badge" class="hidden absolute left-0 top-0 bottom-0 bg-blue-700 text-white w-7 flex flex-col items-center justify-center border-r-2 border-black">
                        <div class="w-4 h-3 bg-yellow-400 rounded-sm mb-1"></div>
                        <span class="text-[9px] font-black tracking-widest text-white">UA</span>
                    </div>

                </div>
            </div>

            <div id="info-box" class="text-center my-1 hidden glass-panel p-3 rounded-xl w-full border border-slate-800">
                <p id="res-title" class="text-xs font-bold text-indigo-400 uppercase tracking-widest"></p>
                <p class="text-xs text-slate-300 mt-1">ОЦЕНКА: <span id="res-val" class="text-emerald-400 font-black text-sm">0</span> ₽</p>
            </div>

            <!-- ВЫБОР ТИПА КРУТКИ, СТРАНЫ И РЕГИОНА -->
            <div class="w-full space-y-3 mt-auto pt-2">
                <div>
                    <label class="block text-[10px] text-slate-400 mb-1 font-bold">ТИП КОНТЕЙНЕРА / КРУТКИ:</label>
                    <select id="spin-tier-select" onchange="calculateSpinPrice()" class="w-full bg-slate-800/90 border border-slate-700/80 rounded-xl p-3 text-xs font-bold text-amber-400 focus:outline-none">
                        <option value="normal">📦 Обычная крутка — 1 000 ₽ (с 1 уровня)</option>
                        <option value="rare" id="opt-rare" disabled>🟢 Редкая крутка — 5 000 ₽ (нужен 3 уровень)</option>
                        <option value="legendary" id="opt-legendary" disabled>⚡ Легендарная крутка — 15 000 ₽ (нужен 5 уровень)</option>
                    </select>
                </div>

                <div class="flex gap-2">
                    <select id="country-select" onchange="onCountryChange()" class="bg-slate-800/90 border border-slate-700/80 rounded-xl p-3 text-xs font-bold text-white focus:outline-none flex-1">
                        <option value="ru">🇷🇺 Россия</option>
                        <option value="ua">🇺🇦 Украина</option>
                        <option value="by">🇧🇾 Беларусь</option>
                    </select>

                    <select id="region-select" onchange="calculateSpinPrice()" class="bg-slate-800/90 border border-slate-700/80 rounded-xl p-3 text-xs font-bold text-white focus:outline-none flex-1">
                    </select>
                </div>

                <div class="flex gap-2">
                    <button onclick="spin()" id="spin-btn" class="flex-1 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 text-slate-950 font-black py-4 rounded-xl shadow-lg transition flex items-center justify-between px-5 active:scale-[0.98]">
                        <span>🎰 КРУТИТЬ</span>
                        <span id="spin-price-badge" class="bg-slate-950/20 text-slate-950 border border-slate-950/30 px-2.5 py-1 rounded-lg text-xs font-black">1 000 ₽</span>
                    </button>

                    <button onclick="sellCurrentPlate()" id="sell-btn" class="hidden bg-emerald-600 hover:bg-emerald-500 text-white font-black px-5 py-4 rounded-xl shadow-lg transition active:scale-[0.98] text-xs flex items-center gap-1">
                        💵 Продать
                    </button>
                </div>
            </div>
        </div>

        <!-- МОДАЛЬНОЕ ОКНО ДЛЯ РЕДКИХ НОМЕРОВ С ПОДТВЕРЖДЕНИЕМ ПРОДАЖИ -->
        <div id="rare-modal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
            <div id="modal-step-1" class="glass-panel p-6 rounded-2xl max-w-sm w-full text-center space-y-4 border border-amber-500/50 shadow-2xl">
                <div class="text-3xl">🔥</div>
                <h3 class="text-lg font-black text-amber-400" id="modal-rarity-title">ВЫПАЛ ЛЕГЕНДАРНЫЙ НОМЕР!</h3>
                <p class="text-xs text-slate-300">Вы выбили эксклюзивный госномер <b id="modal-plate-name" class="text-white"></b>!</p>
                <div class="bg-slate-900/90 p-3 rounded-xl border border-slate-800">
                    <span class="text-xs text-slate-400">Рыночная цена:</span>
                    <div id="modal-plate-price" class="text-lg font-black text-emerald-400">250 000 ₽</div>
                </div>
                <div class="flex gap-3 pt-2">
                    <button onclick="confirmSellStep()" class="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 rounded-xl text-xs transition">
                        💵 Продать
                    </button>
                    <button onclick="modalAction('keep')" class="flex-1 bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 rounded-xl text-xs transition">
                        🚗 Забрать в гараж
                    </button>
                </div>
            </div>

            <!-- ОКНО ПОДТВЕРЖДЕНИЯ ПРОДАЖИ -->
            <div id="modal-step-confirm" class="hidden glass-panel p-6 rounded-2xl max-w-sm w-full text-center space-y-4 border border-rose-500/50 shadow-2xl">
                <div class="text-3xl">⚠️</div>
                <h3 class="text-base font-black text-rose-400">ПОДТВЕРЖДЕНИЕ ПРОДАЖИ</h3>
                <p class="text-xs text-slate-300">Вы уверены, что хотите продать редкий номер <b id="confirm-plate-name" class="text-white"></b> за <span id="confirm-plate-price" class="text-emerald-400 font-bold"></span>?</p>
                <div class="flex gap-3 pt-2">
                    <button onclick="modalAction('sell')" class="flex-1 bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 rounded-xl text-xs transition">
                        Да, продать
                    </button>
                    <button onclick="backToStep1()" class="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-bold py-3 rounded-xl text-xs transition">
                        Назад / В гараж
                    </button>
                </div>
            </div>
        </div>

        <!-- ЭКРАН 2: ПРОФИЛЬ / МЕНЮ -->
        <div id="view-profile" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-4">
            <button onclick="showView('slots')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад к крутке
            </button>

            <div class="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-indigo-600/30 border border-indigo-500/50 rounded-2xl flex items-center justify-center text-xl text-indigo-300 font-bold">
                        👤
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <h2 class="text-sm font-bold text-white">Коллекционер</h2>
                            <span id="admin-status-badge" class="hidden bg-rose-600 text-white text-[9px] font-black px-2 py-0.5 rounded shadow tracking-wider">⚡ СТАТУС: АДМИН</span>
                        </div>
                        <p class="text-[11px] text-slate-400">ID: <span id="user-tg-id">7271568260</span></p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <button onclick="showView('garage')" class="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition active:scale-95">
                    <span class="text-3xl">🚗</span>
                    <span class="text-xs font-bold text-white">Гараж номеров</span>
                    <span class="text-[10px] text-slate-400"><span id="menu-garage-count">0</span> штук</span>
                </button>

                <button onclick="showView('quests')" class="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition active:scale-95">
                    <span class="text-3xl">🎯</span>
                    <span class="text-xs font-bold text-white">Квесты</span>
                    <span class="text-[10px] text-amber-400">Задания</span>
                </button>

                <button onclick="showView('market')" class="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition active:scale-95">
                    <span class="text-3xl">📈</span>
                    <span class="text-xs font-bold text-white">Биржа</span>
                    <span class="text-[10px] text-emerald-400">Аукцион</span>
                </button>

                <button onclick="showView('slots')" class="glass-panel p-4 rounded-2xl border border-indigo-500/30 bg-indigo-950/20 flex flex-col items-center justify-center gap-2 hover:border-indigo-400 transition active:scale-95">
                    <span class="text-3xl">🎰</span>
                    <span class="text-xs font-bold text-white">Крутить Слоты</span>
                    <span class="text-[10px] text-indigo-300">Перейти</span>
                </button>
            </div>

            <button id="admin-menu-btn" onclick="showView('admin')" class="hidden w-full bg-rose-600/20 border border-rose-500/50 text-rose-300 font-bold py-3.5 rounded-xl text-xs transition flex items-center justify-center gap-2">
                👑 Терминал Администратора
            </button>
        </div>

        <!-- ЭКРАН 3: ГАРАЖ -->
        <div id="view-garage" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <h2 class="text-sm font-bold text-slate-200">Гараж госномеров</h2>
            <div id="garage-list" class="space-y-3"></div>
        </div>

        <!-- ЭКРАН 4: КВЕСТЫ -->
        <div id="view-quests" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <h2 class="text-sm font-bold text-slate-200 mb-2">🎯 Квесты и Задания</h2>
            <div id="quests-list" class="space-y-3"></div>
        </div>

        <!-- ЭКРАН 5: БИРЖА -->
        <div id="view-market" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <h2 class="text-sm font-bold text-slate-200 mb-1">📈 Глобальная биржа</h2>
            <div id="market-list" class="space-y-3"></div>
        </div>

        <!-- ЭКРАН 6: АДМИН-ПАНЕЛЬ -->
        <div id="view-admin" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <div class="glass-panel p-5 rounded-2xl border border-rose-500/40 space-y-3">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">👑</span>
                        <h2 class="text-sm font-black text-rose-400">ТЕРМИНАЛ АДМИНИСТРАТОРА</h2>
                    </div>
                    <span class="bg-rose-600/30 border border-rose-500 text-rose-300 text-[9px] font-black px-2 py-0.5 rounded">⚡ АДМИН</span>
                </div>
                
                <div class="space-y-3 pt-2">
                    <div>
                        <label class="block text-[10px] text-slate-400 mb-1">Telegram ID игрока:</label>
                        <input id="admin-target-id" type="number" value="7271568260" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs">
                    </div>
                    
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="block text-[10px] text-slate-400 mb-1">Сумма рублей (₽):</label>
                            <input id="admin-money-amount" type="number" value="500000" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs">
                        </div>
                        <div>
                            <label class="block text-[10px] text-slate-400 mb-1">Опыт (EXP):</label>
                            <input id="admin-exp-amount" type="number" value="100" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs">
                        </div>
                    </div>

                    <div class="flex gap-2">
                        <button onclick="adminGiveMoney()" class="flex-1 bg-emerald-600/30 border border-emerald-500/60 text-emerald-300 font-bold py-2.5 rounded-xl text-xs transition">
                            + Рубли
                        </button>
                        <button onclick="adminGiveExp()" class="flex-1 bg-indigo-600/30 border border-indigo-500/60 text-indigo-300 font-bold py-2.5 rounded-xl text-xs transition">
                            + Опыт (EXP)
                        </button>
                    </div>

                    <hr class="border-slate-800 my-2">

                    <div>
                        <label class="block text-[10px] text-slate-400 mb-1">Кастомный номерной знак:</label>
                        <input id="admin-plate-num" type="text" placeholder="А 777 АА 777" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs mb-2">
                        
                        <label class="block text-[10px] text-slate-400 mb-1">Редкость:</label>
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
                        Выдать номер и очистить поля
                    </button>
                </div>
            </div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            const ADMIN_ID = __ADMIN_ID__;
            let currentUserTgId = tg.initDataUnsafe?.user?.id || 7271568260;

            document.getElementById('user-tg-id').innerText = currentUserTgId;

            if (currentUserTgId === ADMIN_ID) {
                document.getElementById('admin-status-badge').classList.remove('hidden');
                document.getElementById('admin-menu-btn').classList.remove('hidden');
            }

            let state = {
                balance: 1250000,
                level: 1,
                exp: 0,
                garage: [],
                lastDroppedPlate: null,
                pendingRarePlate: null,
                quests: [
                    { id: 1, title: "Первая крутка слота", rewardMoney: 50000, rewardExp: 30, progress: 0, target: 1, done: false, claimed: false },
                    { id: 2, title: "Выбить 3 редких номера", rewardMoney: 150000, rewardExp: 50, progress: 0, target: 3, done: false, claimed: false },
                    { id: 3, title: "Продать номер на бирже", rewardMoney: 200000, rewardExp: 70, progress: 0, target: 1, done: false, claimed: false }
                ],
                market: [
                    { id: 1, number: "А 777 АА", region: "777", title: "🔥 МИФИЧЕСКИЙ НОМЕР", price: 600000, seller: "CyberLord", color: "red" },
                    { id: 2, number: "В 111 ВВ", region: "78", title: "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", price: 250000, seller: "Москвич", color: "yellow" }
                ]
            };

            const RU_REGIONS = ['77', '99', '177', '199', '777', '799', '78', '98', '178', '198', '50', '90', '150', '161', '125'];
            const RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х'];
            const UA_OBLASTS = ['AA', 'KA', 'BC', 'HC', 'AE', 'BH', 'BI', 'AX', 'AP', 'CB', 'AM', 'AO', 'BX'];
            const BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7'];

            function showToast(msg, icon = "🔔") {
                let toast = document.getElementById('toast');
                document.getElementById('toast-msg').innerText = msg;
                document.getElementById('toast-icon').innerText = icon;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 3000);
            }

            function getMaxExpForLevel(lvl) {
                return lvl * 100; // Прогрессия опыта
            }

            function animateBalance(targetValue) {
                let currentVal = state.balance;
                let step = Math.ceil(Math.abs(targetValue - currentVal) / 12);
                let timer = setInterval(() => {
                    if (currentVal < targetValue) {
                        currentVal = Math.min(currentVal + step, targetValue);
                    } else if (currentVal > targetValue) {
                        currentVal = Math.max(currentVal - step, targetValue);
                    }
                    document.getElementById('balance').innerText = currentVal.toLocaleString('ru-RU') + ' ₽';
                    if (currentVal === targetValue) {
                        clearInterval(timer);
                        state.balance = targetValue;
                    }
                }, 25);
            }

            function onCountryChange() {
                let country = document.getElementById('country-select').value;
                let regionSelect = document.getElementById('region-select');
                regionSelect.innerHTML = '';

                let list = country === 'ru' ? RU_REGIONS : (country === 'ua' ? UA_OBLASTS : BY_REGIONS);
                
                let defaultOpt = document.createElement('option');
                defaultOpt.value = "auto";
                defaultOpt.innerText = country === 'ua' ? "🎲 Любая область" : "🎲 Любой регион";
                regionSelect.appendChild(defaultOpt);

                list.forEach(r => {
                    let opt = document.createElement('option');
                    opt.value = r;
                    opt.innerText = country === 'ua' ? `Область ${r}` : `Регион ${r}`;
                    regionSelect.appendChild(opt);
                });

                calculateSpinPrice();
                updatePlateVisual(country, country === 'ua' ? 'AA 7777 AB' : 'А 777 АА', list[0], 'yellow');
            }

            function calculateSpinPrice() {
                let tier = document.getElementById('spin-tier-select').value;
                let reg = document.getElementById('region-select').value;
                
                let basePrice = 1000;
                if (tier === 'rare') basePrice = 5000;
                else if (tier === 'legendary') basePrice = 15000;

                if (['777', '799', '199', '77', 'AA', 'KA', '7'].includes(reg)) {
                    basePrice = Math.round(basePrice * 1.2);
                }

                document.getElementById('spin-price-badge').innerText = basePrice.toLocaleString('ru-RU') + ' ₽';
                return basePrice;
            }

            function addExp(amount) {
                state.exp += amount;
                let maxExp = getMaxExpForLevel(state.level);
                
                if (state.exp >= maxExp) {
                    state.level += 1;
                    state.exp -= maxExp;
                    let reward = state.level * 150000;
                    animateBalance(state.balance + reward);
                    showToast(`🎉 НОВЫЙ УРОВЕНЬ ${state.level}! Награда: +${reward.toLocaleString('ru-RU')} ₽!`, "⭐");
                }
                updateUI();
            }

            function updateUI() {
                // Разблокировка уровней круток
                let rareOpt = document.getElementById('opt-rare');
                let legOpt = document.getElementById('opt-legendary');

                if (state.level >= 3) {
                    rareOpt.disabled = false;
                    rareOpt.innerText = "🟢 Редкая крутка — 5 000 ₽ (Доступно)";
                } else {
                    rareOpt.disabled = true;
                    rareOpt.innerText = "🟢 Редкая крутка — 5 000 ₽ (нужен 3 уровень)";
                }

                if (state.level >= 5) {
                    legOpt.disabled = false;
                    legOpt.innerText = "⚡ Легендарная крутка — 15 000 ₽ (Доступно)";
                } else {
                    legOpt.disabled = true;
                    legOpt.innerText = "⚡ Легендарная крутка — 15 000 ₽ (нужен 5 уровень)";
                }

                document.getElementById('level').innerText = state.level;
                document.getElementById('exp').innerText = state.exp;
                document.getElementById('max-exp').innerText = getMaxExpForLevel(state.level);
                document.getElementById('menu-garage-count').innerText = state.garage.length;
                
                renderGarage();
                renderMarket();
                renderQuests();
            }

            function showView(viewName) {
                ['profile', 'slots', 'garage', 'quests', 'market', 'admin'].forEach(v => {
                    let el = document.getElementById(`view-${v}`);
                    if (el) el.classList.add('hidden');
                });
                let target = document.getElementById(`view-${viewName}`);
                if (target) target.classList.remove('hidden');
            }

            function updatePlateVisual(country, numberText, regionText, colorClass) {
                let plateBox = document.getElementById('plate-box');
                let codeText = document.getElementById('plate-code-text');
                let svgBox = document.getElementById('svg-flag-box');
                let regionBlock = document.getElementById('region-block');
                let uaBadge = document.getElementById('ua-badge');

                plateBox.className = `relative bg-white text-black border-4 rounded-xl shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300 glow-${colorClass}`;
                document.getElementById('plate-text').innerText = numberText;
                document.getElementById('plate-region').innerText = regionText;

                if (country === 'ua') {
                    regionBlock.classList.add('hidden');
                    uaBadge.classList.remove('hidden');
                } else {
                    regionBlock.classList.remove('hidden');
                    uaBadge.classList.add('hidden');

                    if (country === 'ru') {
                        codeText.innerText = 'RUS';
                        svgBox.innerHTML = '<svg class="w-full h-full" viewBox="0 0 36 24"><rect width="36" height="8" fill="#fff"/><rect y="8" width="36" height="8" fill="#0039a6"/><rect y="16" width="36" height="8" fill="#d52b1e"/></svg>';
                    } else if (country === 'by') {
                        codeText.innerText = 'BY';
                        svgBox.innerHTML = '<svg class="w-full h-full" viewBox="0 0 36 24"><rect width="36" height="15" fill="#d52b1e"/><rect y="15" width="36" height="9" fill="#008751"/><rect width="10" height="24" fill="#fff"/></svg>';
                    }
                }
            }

            async function spin() {
                let price = calculateSpinPrice();
                if (state.balance < price) {
                    showToast('Недостаточно рублей на балансе!', '❌');
                    return;
                }
                
                animateBalance(state.balance - price);

                let country = document.getElementById('country-select').value;
                let region = document.getElementById('region-select').value;
                let tier = document.getElementById('spin-tier-select').value;
                let infoBox = document.getElementById('info-box');
                infoBox.classList.add('hidden');

                // Анимация перебора БУКВ И ЦИФР
                let counter = 0;
                let interval = setInterval(() => {
                    let randNum = Math.floor(100 + Math.random() * 900);
                    let l1 = RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)];
                    let l2 = RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)];
                    let l3 = RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)];
                    
                    let animatedText = country === 'ua' 
                        ? `АА ${randNum} ВХ` 
                        : `${l1} ${randNum} ${l2}${l3}`;

                    updatePlateVisual(country, animatedText, '99', 'gray');
                    counter++;
                    if (counter > 14) clearInterval(interval);
                }, 40);

                let response = await fetch(`/api/spin?country=${country}&region=${region}&tier=${tier}`);
                if (response.ok) {
                    let data = await response.json();
                    setTimeout(() => {
                        updatePlateVisual(country, data.number, data.region, data.color);
                        
                        document.getElementById('res-title').innerText = data.title;
                        infoBox.classList.remove('hidden');
                        
                        let startVal = 0;
                        let valInterval = setInterval(() => {
                            startVal += Math.round(data.value / 10);
                            if (startVal >= data.value) {
                                startVal = data.value;
                                clearInterval(valInterval);
                            }
                            document.getElementById('res-val').innerText = startVal.toLocaleString('ru-RU');
                        }, 25);

                        addExp(tier === 'legendary' ? 50 : (tier === 'rare' ? 25 : 15));
                        
                        state.quests[0].progress = 1;
                        if (state.quests[0].progress >= state.quests[0].target) state.quests[0].done = true;

                        if (['green', 'blue', 'yellow', 'red', 'purple'].includes(data.color)) {
                            state.quests[1].progress += 1;
                            if (state.quests[1].progress >= state.quests[1].target) state.quests[1].done = true;
                        }

                        state.lastDroppedPlate = data;
                        document.getElementById('sell-btn').classList.remove('hidden');

                        if (['yellow', 'red', 'purple'].includes(data.color)) {
                            state.pendingRarePlate = data;
                            document.getElementById('modal-rarity-title').innerText = `ВЫПАЛ ${data.title}!`;
                            document.getElementById('modal-plate-name').innerText = `${data.number} | ${data.region}`;
                            document.getElementById('modal-plate-price').innerText = `${data.value.toLocaleString('ru-RU')} ₽`;
                            
                            document.getElementById('modal-step-1').classList.remove('hidden');
                            document.getElementById('modal-step-confirm').classList.add('hidden');
                            document.getElementById('rare-modal').classList.remove('hidden');
                        } else {
                            state.garage.unshift(data);
                            updateUI();
                        }

                        tg.HapticFeedback?.notificationOccurred('success');
                    }, 650);
                }
            }

            function confirmSellStep() {
                if (!state.pendingRarePlate) return;
                document.getElementById('confirm-plate-name').innerText = `${state.pendingRarePlate.number} | ${state.pendingRarePlate.region}`;
                document.getElementById('confirm-plate-price').innerText = `${state.pendingRarePlate.value.toLocaleString('ru-RU')} ₽`;
                
                document.getElementById('modal-step-1').classList.add('hidden');
                document.getElementById('modal-step-confirm').classList.remove('hidden');
            }

            function backToStep1() {
                document.getElementById('modal-step-confirm').classList.add('hidden');
                document.getElementById('modal-step-1').classList.remove('hidden');
            }

            function sellCurrentPlate() {
                if (!state.lastDroppedPlate) return;
                let val = state.lastDroppedPlate.value;
                animateBalance(state.balance + val);
                
                let index = state.garage.indexOf(state.lastDroppedPlate);
                if (index > -1) state.garage.splice(index, 1);

                showToast(`💵 Продано! +${val.toLocaleString('ru-RU')} ₽`, '💰');
                document.getElementById('sell-btn').classList.add('hidden');
                document.getElementById('info-box').classList.add('hidden');
                state.lastDroppedPlate = null;
                updateUI();
            }

            function modalAction(action) {
                document.getElementById('rare-modal').classList.add('hidden');
                if (!state.pendingRarePlate) return;

                if (action === 'sell') {
                    animateBalance(state.balance + state.pendingRarePlate.value);
                    showToast(`💵 Продано! +${state.pendingRarePlate.value.toLocaleString('ru-RU')} ₽`, '💰');
                } else {
                    state.garage.unshift(state.pendingRarePlate);
                    showToast('🚗 Номер сохранен в ваш гараж!', '✅');
                }
                document.getElementById('sell-btn').classList.add('hidden');
                state.pendingRarePlate = null;
                updateUI();
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
                            <div class="text-base font-plate font-black text-white mt-0.5">${item.number} ${item.region !== "UA" ? "| " + item.region : ""}</div>
                            <span class="text-xs text-emerald-400 font-semibold">Ценность: ${item.value.toLocaleString('ru-RU')} ₽</span>
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
                animateBalance(state.balance + item.value);
                state.garage.splice(index, 1);
                showToast(`💵 Продано! +${item.value.toLocaleString('ru-RU')} ₽`, '💰');
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
                    price: Math.round(item.value * 1.3),
                    seller: "Вы",
                    color: item.color
                });
                state.garage.splice(index, 1);
                
                state.quests[2].progress = 1;
                state.quests[2].done = true;

                showToast("Номер выставлен на биржу!", "📈");
                updateUI();
            }

            function renderMarket() {
                let list = document.getElementById('market-list');
                list.innerHTML = state.market.map((item, index) => `
                    <div class="glass-panel p-3.5 rounded-xl flex justify-between items-center border border-slate-800">
                        <div>
                            <span class="text-[10px] text-slate-400">Продавец: ${item.seller}</span>
                            <div class="text-base font-plate font-black text-amber-400 mt-0.5">${item.number} ${item.region !== "UA" ? "| " + item.region : ""}</div>
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
                    showToast("Недостаточно средств на балансе!", "❌");
                    return;
                }
                animateBalance(state.balance - item.price);
                state.garage.unshift({ number: item.number, region: item.region, title: item.title, value: item.price, color: item.color || 'blue' });
                state.market.splice(index, 1);
                showToast("Номер успешно куплен!", "✅");
                updateUI();
            }

            function renderQuests() {
                let list = document.getElementById('quests-list');
                list.innerHTML = state.quests.map((q, idx) => `
                    <div class="glass-panel p-3.5 rounded-xl border border-slate-800 flex justify-between items-center">
                        <div>
                            <div class="text-xs font-bold text-slate-200">${q.title}</div>
                            <div class="text-[10px] text-emerald-400">+${q.rewardMoney.toLocaleString('ru-RU')} ₽ • +${q.rewardExp} EXP</div>
                        </div>
                        ${q.claimed 
                            ? `<span class="text-xs text-slate-500 font-bold">Выполнено</span>` 
                            : (q.done 
                                ? `<button onclick="claimQuest(${idx})" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-3 py-1.5 rounded-lg text-xs">Забрать</button>` 
                                : `<span class="text-xs text-slate-400 font-bold">${q.progress}/${q.target}</span>`
                            )
                        }
                    </div>
                `).join('');
            }

            function claimQuest(idx) {
                let q = state.quests[idx];
                q.claimed = true;
                animateBalance(state.balance + q.rewardMoney);
                addExp(q.rewardExp);
                showToast(`🎯 Задание выполнено: +${q.rewardMoney.toLocaleString('ru-RU')} ₽!`, "🎉");
                updateUI();
            }

            function adminGiveMoney() {
                let targetId = document.getElementById('admin-target-id').value;
                let amount = parseInt(document.getElementById('admin-money-amount').value) || 0;
                animateBalance(state.balance + amount);
                showToast(`⚡ [АДМИН] Начислено +${amount.toLocaleString('ru-RU')} ₽ для ID ${targetId}!`, "👑");
            }

            function adminGiveExp() {
                let targetId = document.getElementById('admin-target-id').value;
                let amount = parseInt(document.getElementById('admin-exp-amount').value) || 0;
                addExp(amount);
                showToast(`⚡ [АДМИН] Начислено +${amount} EXP для ID ${targetId}!`, "👑");
            }

            function adminGiveCustomPlate() {
                let numInput = document.getElementById('admin-plate-num');
                let rarityInput = document.getElementById('admin-plate-rarity');
                
                let num = numInput.value.trim() || "А 777 АА";
                let rarity = rarityInput.value;
                
                let colorMap = { "обычный": "gray", "редкий": "green", "сверхредкий": "blue", "легендарный": "yellow", "мифический": "red", "мистический": "purple" };
                let color = colorMap[rarity] || "blue";

                state.garage.unshift({
                    number: num,
                    region: "777",
                    title: `👑 ЭКСКЛЮЗИВ (${rarity.toUpperCase()})`,
                    value: rarity === 'мистический' ? 1500000 : 400000,
                    color: color
                });
                
                numInput.value = '';
                rarityInput.selectedIndex = 0;

                showToast(`⚡ Номер "${num}" (${rarity}) выдан! Поля очищены.`, "👑");
                updateUI();
            }

            onCountryChange();
            updateUI();
        </script>
    </body>
    </html>
    """
    return html_content.replace("__ADMIN_ID__", str(ADMIN_TG_ID))