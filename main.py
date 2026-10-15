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
        text="🚗 Запустить нАмерок", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    await message.answer(
        "🔥 **нАмерок // Официальный клиент** 🔥\n\n"
        "Твой личный профиль, гараж редких госномеров России, Украины и Беларуси, квесты и биржа в одном месте!",
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
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1500000
        elif roll < 0.18:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 600000
        elif roll < 0.40:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 250000
        elif roll < 0.65:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 90000
        elif roll < 0.85:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 35000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 12000
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
        digits = f"{random.randint(1, 999):03d}" if rarity in ["обычный", "редкий"] else random.choice(["777", "001", "999", "333"])
        l23 = "".join(random.choices(RU_LETTERS, k=2))
        reg = random.choice(RU_REGIONS)
        number_str = f"{l1} {digits} {l23}"
        region_str = reg
    elif country == "ua":
        series = random.choice(UA_SERIES)
        digits = f"{random.randint(1, 9999):04d}" if rarity in ["обычный", "редкий"] else str(random.choice([1, 7, 9])) * 4
        number_str = f"{series} {digits}"
        region_str = "UA"
    else:
        digits = f"{random.randint(1, 9999):04d}"
        let = random.choice(BY_LETTERS)
        reg = random.choice(BY_REGIONS)
        number_str = f"{digits} {let}"
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
        </style>
    </head>
    <body class="min-h-screen flex flex-col select-none pb-8 overflow-x-hidden">
        
        <!-- ВЕРХНЯЯ ШАПКА -->
        <header class="bg-slate-900/90 border-b border-slate-800 p-3 flex justify-between items-center sticky top-0 z-50">
            <div class="flex flex-col">
                <span class="text-[10px] text-slate-400 font-semibold uppercase tracking-wider">Баланс</span>
                <span id="balance" class="font-mono font-black text-lg text-emerald-400">1 250 000 ₽</span>
            </div>
            
            <div class="flex items-center gap-2">
                <div class="text-xs bg-slate-800 px-3 py-1.5 rounded-xl border border-slate-700 text-slate-300 font-bold flex items-center gap-1.5">
                    <span>Ур. <span id="level" class="text-white">1</span></span>
                    <span class="text-slate-600">|</span>
                    <span class="flex items-center text-amber-400">🔥 <span id="energy" class="text-white ml-0.5">0</span></span>
                </div>
                <!-- КНОПКА ПРОФИЛЯ / МЕНЮ -->
                <button onclick="showView('profile')" class="bg-indigo-600 hover:bg-indigo-500 p-2 px-3 rounded-xl border border-indigo-400/50 text-white transition flex items-center gap-1 active:scale-95 shadow-md shadow-indigo-950/50">
                    👤 Меню
                </button>
            </div>
        </header>

        <!-- ЭКРАН 1: ПРОФИЛЬ И ХАБ (ГЛАВНЫЙ) -->
        <div id="view-profile" class="p-4 flex flex-col flex-1 max-w-md mx-auto w-full space-y-4">
            <!-- Карточка пользователя -->
            <div class="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-indigo-600/30 border border-indigo-500/50 rounded-2xl flex items-center justify-center text-xl text-indigo-300 font-bold">
                        👤
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <h2 class="text-sm font-bold text-white">Агент Мегаполиса</h2>
                            <!-- Бейдж администратора, появится если ID совпадет -->
                            <span id="admin-badge" class="hidden bg-rose-600 text-white text-[9px] font-black px-2 py-0.5 rounded shadow">⚡ АДМИН</span>
                        </div>
                        <p class="text-[11px] text-slate-400">ID: <span id="user-tg-id">7271568260</span></p>
                    </div>
                </div>
                <div class="text-right">
                    <span class="text-xs text-amber-400 font-bold">⭐ Ур. 1</span>
                </div>
            </div>

            <!-- ГЛАВНОЕ МЕНЮ КНОПОК -->
            <div class="grid grid-cols-2 gap-3">
                <button onclick="showView('slots')" class="glass-panel p-4 rounded-2xl border border-indigo-500/30 bg-indigo-950/20 flex flex-col items-center justify-center gap-2 hover:border-indigo-400 transition active:scale-95">
                    <span class="text-3xl">🎰</span>
                    <span class="text-xs font-bold text-white">Крутить Слоты</span>
                    <span class="text-[10px] text-indigo-300">Открыть рулетку</span>
                </button>
                
                <button onclick="showView('garage')" class="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition active:scale-95">
                    <span class="text-3xl">🚗</span>
                    <span class="text-xs font-bold text-white">Гараж</span>
                    <span class="text-[10px] text-slate-400"><span id="menu-garage-count">0</span> номеров</span>
                </button>

                <button onclick="showView('quests')" class="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition active:scale-95">
                    <span class="text-3xl">🎯</span>
                    <span class="text-xs font-bold text-white">Квесты</span>
                    <span class="text-[10px] text-amber-400">Путь новичка</span>
                </button>

                <button onclick="showView('market')" class="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition active:scale-95">
                    <span class="text-3xl">📈</span>
                    <span class="text-xs font-bold text-white">Биржа</span>
                    <span class="text-[10px] text-emerald-400">Аукцион</span>
                </button>
            </div>

            <!-- Админ-панель кнопка (скрыта по умолчанию) -->
            <button id="admin-menu-btn" onclick="showView('admin')" class="hidden w-full bg-rose-600/20 border border-rose-500/50 text-rose-300 font-bold py-3 rounded-xl text-xs transition flex items-center justify-center gap-2">
                👑 Терминал Администратора
            </button>
        </div>

        <!-- ЭКРАН 2: СЛОТЫ И КРУТКА -->
        <div id="view-slots" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-4">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в профиль
            </button>

            <div class="w-full bg-slate-900/80 border border-slate-800 rounded-xl p-2.5 text-center">
                <span class="text-xs text-amber-400 font-bold">🔥 Страна дня: Россия • мифик x2</span>
            </div>

            <div class="text-center text-xs text-slate-400 pt-2">Крутите реальный госномер</div>

            <!-- НОМЕРНОЙ ЗНАК КАК В ЖИЗНИ -->
            <div class="w-full flex justify-center my-3">
                <div id="plate-box" class="relative bg-white text-black border-4 rounded-xl shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300 glow-gray">
                    <div class="flex-1 text-center font-plate font-black text-3xl tracking-wider overflow-hidden">
                        <span id="plate-text">А 777 АА</span>
                    </div>
                    <div class="border-l-2 border-slate-300 pl-3 flex flex-col items-center justify-center min-w-[70px]">
                        <span id="plate-region" class="text-2xl font-plate font-black leading-none text-slate-900">777</span>
                        <div class="flex items-center gap-1 mt-1">
                            <span id="plate-code-text" class="text-[10px] font-bold tracking-widest text-slate-800">RUS</span>
                            <span id="svg-flag" class="text-sm">🇷🇺</span>
                        </div>
                    </div>
                </div>
            </div>

            <div id="info-box" class="text-center text-xs text-amber-400 hidden font-bold">
                🎉 Поздравляем! Номер добавлен в гараж!
            </div>

            <div class="w-full space-y-3 mt-auto pt-6">
                <div class="flex gap-2">
                    <select id="country-select" class="w-full bg-slate-800/90 border border-slate-700/80 rounded-xl p-3.5 text-xs font-semibold text-white focus:outline-none">
                        <option value="ru">🇷🇺 Россия (ГОСТ)</option>
                        <option value="ua">🇺🇦 Украина (UA-NET)</option>
                        <option value="by">🇧🇾 Беларусь (BY-GRID)</option>
                    </select>
                </div>

                <button onclick="spin()" class="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 text-slate-950 font-black py-4 rounded-xl shadow-lg transition flex items-center justify-center gap-2 active:scale-[0.98]">
                    <span>🎰 Крутить слот (1 000 ₽)</span>
                </button>
            </div>
        </div>

        <!-- ЭКРАН 3: ГАРАЖ -->
        <div id="view-garage" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в профиль
            </button>
            <h2 class="text-sm font-bold text-slate-200">Гараж номеров</h2>
            <div id="garage-list" class="space-y-3">
                <div class="text-center text-slate-500 py-12 text-xs">Гараж пуст. Крутите слоты!</div>
            </div>
        </div>

        <!-- ЭКРАН 4: КВЕСТЫ -->
        <div id="view-quests" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в профиль
            </button>
            <h2 class="text-sm font-bold text-slate-200 mb-2">🎯 Путь новичка (0/6)</h2>
            
            <div class="glass-panel p-3.5 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                    <div class="text-xs font-bold text-slate-200">Сделать первую крутку слота</div>
                    <div class="text-[10px] text-emerald-400">+50 000 ₽ на баланс</div>
                </div>
                <button class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-3 py-1.5 rounded-lg text-xs">Забрать</button>
            </div>
            <div class="glass-panel p-3.5 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                    <div class="text-xs font-bold text-slate-200">Выбить редкий номер</div>
                    <div class="text-[10px] text-emerald-400">+150 000 ₽</div>
                </div>
                <span class="text-xs text-slate-500 font-bold">0/1</span>
            </div>
        </div>

        <!-- ЭКРАН 5: БИРЖА -->
        <div id="view-market" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в профиль
            </button>
            <h2 class="text-sm font-bold text-slate-200 mb-1">📈 Глобальная биржа</h2>
            <div id="market-list" class="space-y-3"></div>
        </div>

        <!-- ЭКРАН 6: АДМИН-ПАНЕЛЬ -->
        <div id="view-admin" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в профиль
            </button>
            <div class="glass-panel p-5 rounded-2xl border border-rose-500/40 space-y-3">
                <div class="flex items-center gap-2">
                    <span class="text-xl">👑</span>
                    <h2 class="text-sm font-black text-rose-400">ТЕРМИНАЛ АДМИНИСТРАТОРА</h2>
                </div>
                <div>
                    <label class="block text-[10px] text-slate-400 mb-1">Telegram ID игрока:</label>
                    <input id="admin-target-id" type="number" value="7271568260" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs">
                </div>
                <div>
                    <label class="block text-[10px] text-slate-400 mb-1">Сумма рублей (₽):</label>
                    <input id="admin-money-amount" type="number" value="500000" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs">
                </div>
                <button onclick="adminGiveMoney()" class="w-full bg-emerald-600/30 border border-emerald-500/60 text-emerald-300 font-bold py-3 rounded-xl text-xs transition">
                    Начислить баланс
                </button>

                <hr class="border-slate-800">

                <div>
                    <label class="block text-[10px] text-slate-400 mb-1">Кастомный номер:</label>
                    <input id="admin-plate-num" type="text" placeholder="Х 777 ХХ" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs mb-2">
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
                    Выдать номер в гараж
                </button>
            </div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            const ADMIN_ID = __ADMIN_ID__;
            let currentUserTgId = tg.initDataUnsafe?.user?.id || 7271568260;

            document.getElementById('user-tg-id').innerText = currentUserTgId;

            if (currentUserTgId === ADMIN_ID) {
                document.getElementById('admin-badge').classList.remove('hidden');
                document.getElementById('admin-menu-btn').classList.remove('hidden');
            }

            let state = {
                balance: 1250000,
                level: 1,
                energy: 0,
                garage: [],
                market: [
                    { id: 1, number: "А 777 АА", region: "777", title: "🔥 МИФИЧЕСКИЙ НОМЕР", price: 600000, seller: "CyberLord", color: "red" },
                    { id: 2, number: "В 111 ВВ", region: "78", title: "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", price: 250000, seller: "Москвич", color: "yellow" }
                ]
            };

            function updateUI() {
                document.getElementById('balance').innerText = state.balance.toLocaleString('ru-RU') + ' ₽';
                document.getElementById('level').innerText = state.level;
                document.getElementById('energy').innerText = state.energy;
                document.getElementById('menu-garage-count').innerText = state.garage.length;
                renderGarage();
                renderMarket();
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
                if (state.balance < 1000) {
                    alert('Недостаточно рублей!');
                    return;
                }
                state.balance -= 1000;
                updateUI();

                let country = document.getElementById('country-select').value;
                let infoBox = document.getElementById('info-box');
                infoBox.classList.add('hidden');

                // Анимация роста и перебора цифр
                let counter = 0;
                let interval = setInterval(() => {
                    let randNum = Math.floor(100 + Math.random() * 900);
                    updatePlateVisual(country, `Х ${randNum} ХХ`, '99', 'gray');
                    counter++;
                    if (counter > 12) clearInterval(interval);
                }, 45);

                let response = await fetch(`/api/spin?country=${country}&tier=normal`);
                if (response.ok) {
                    let data = await response.json();
                    setTimeout(() => {
                        updatePlateVisual(country, data.number, data.region, data.color);
                        infoBox.classList.remove('hidden');

                        state.garage.unshift(data);
                        updateUI();
                        tg.HapticFeedback?.notificationOccurred('success');
                    }, 600);
                }
            }

            function renderGarage() {
                let list = document.getElementById('garage-list');
                if (state.garage.length === 0) {
                    list.innerHTML = '<div class="text-center text-slate-500 py-12 text-xs">Гараж пуст. Крутите слоты!</div>';
                    return;
                }
                list.innerHTML = state.garage.map((item, index) => `
                    <div class="glass-panel p-3.5 rounded-xl flex justify-between items-center border glow-${item.color}">
                        <div>
                            <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-400">${item.title}</span>
                            <div class="text-base font-plate font-black text-white mt-0.5">${item.number} | ${item.region}</div>
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
                    alert("Недостаточно средств!");
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
                alert(`Админ: начислено ${amount.toLocaleString('ru-RU')} ₽ для ID ${targetId}!`);
            }

            function adminGiveCustomPlate() {
                let num = document.getElementById('admin-plate-num').value.trim() || "А 777 АА";
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
                alert(`Номер "${num}" (${rarity}) успешно выдан в ваш гараж!`);
            }

            updateUI();
            updatePlateVisual('ru', 'А 777 АА', '777', 'yellow');
        </script>
    </body>
    </html>
    """
    return html_content.replace("__ADMIN_ID__", str(ADMIN_TG_ID))