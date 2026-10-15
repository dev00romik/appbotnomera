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
        text="🌐 Войти в CyberPlate 2100", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    await message.answer(
        "⚡ **CYBERPLATE 2100 // КВАНТОВЫЙ АВТОРИНОК** ⚡\n\n"
        "Добро пожаловать в мегаполис будущего! Крутите квантовые слоты, выбивайте мистические номера и торгуйте на бирже за **рубли (₽)**!",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@app.on_event("startup")
async def on_startup():
    async def run_bot():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    asyncio.create_task(run_bot())

UA_SERIES = ['AA', 'KA', 'BC', 'HC', 'AE', 'BH', 'BI', 'AX', 'AP', 'CB']
RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
RU_REGIONS = ['77', '99', '177', '777', '78', '98', '161', '50']
BY_LETTERS = ['AB', 'BM', 'CT', 'MH', 'PB', 'OO']
BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7']

@app.get("/api/spin")
def spin_plates(country: str, tier: str = "normal"):
    roll = random.random()
    
    # 6 уровней редкости с нарастающей стоимостью
    if tier == "elite":
        if roll < 0.05:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 500000
        elif roll < 0.18:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 200000
        elif roll < 0.40:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 80000
        elif roll < 0.65:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 30000
        elif roll < 0.85:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 10000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 3000
    else:
        if roll < 0.01:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 400000
        elif roll < 0.05:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 150000
        elif roll < 0.15:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 50000
        elif roll < 0.35:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 18000
        elif roll < 0.65:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 6000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 1500

    if country == "ua":
        series = random.choice(UA_SERIES)
        dig = f"{random.randint(1, 9999):04d}" if rarity in ["обычный", "редкий"] else str(random.choice([1, 7, 9])) * 4
        number_str = f"{series} {dig} {series}"
    elif country == "ru":
        l1 = random.choice(RU_LETTERS)
        l23 = "".join(random.choices(RU_LETTERS, k=2))
        reg = random.choice(RU_REGIONS)
        dig = f"{random.randint(1, 999):03d}" if rarity in ["обычный", "редкий"] else random.choice(["777", "001", "999", "333"])
        number_str = f"{l1}{dig}{l23} {reg}"
    else:
        dig = f"{random.randint(1, 9999):04d}"
        let = random.choice(BY_LETTERS)
        reg = random.choice(BY_REGIONS)
        number_str = f"{dig} {let}-{reg}"

    return {
        "number": number_str,
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
        <title>CyberPlate 2100</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@600;700&display=swap');
            body {
                font-family: 'Rajdhani', sans-serif;
                background-color: #030712;
                color: #f3f4f6;
            }
            .font-cyber {
                font-family: 'Orbitron', sans-serif;
            }
            .glass-cyber {
                background: rgba(10, 15, 30, 0.85);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(0, 240, 255, 0.15);
                box-shadow: 0 0 20px rgba(0, 240, 255, 0.05);
            }

            @keyframes grayGlow { 0%, 100% { border-color: #4b5563; box-shadow: 0 0 5px rgba(156,163,175,0.2); } 50% { border-color: #9ca3af; box-shadow: 0 0 15px rgba(156,163,175,0.4); } }
            @keyframes greenGlow { 0%, 100% { border-color: #10b981; box-shadow: 0 0 10px rgba(16,185,129,0.4); } 50% { border-color: #34d399; box-shadow: 0 0 25px rgba(16,185,129,0.8); } }
            @keyframes blueGlow { 0%, 100% { border-color: #3b82f6; box-shadow: 0 0 15px rgba(59,130,246,0.5); } 50% { border-color: #60a5fa; box-shadow: 0 0 30px rgba(59,130,246,0.9); } }
            @keyframes yellowGlow { 0%, 100% { border-color: #eab308; box-shadow: 0 0 20px rgba(234,179,8,0.6); } 50% { border-color: #facc15; box-shadow: 0 0 40px rgba(234,179,8,1); } }
            @keyframes redGlow { 0%, 100% { border-color: #ef4444; box-shadow: 0 0 25px rgba(239,68,68,0.7); } 50% { border-color: #f87171; box-shadow: 0 0 45px rgba(239,68,68,1); } }
            @keyframes purpleGlow { 0%, 100% { border-color: #a855f7; box-shadow: 0 0 30px rgba(168,85,247,0.8); filter: hue-rotate(0deg); } 50% { border-color: #ec4899; box-shadow: 0 0 60px rgba(236,72,153,1); filter: hue-rotate(90deg); } }

            .glow-gray { animation: grayGlow 3s infinite; }
            .glow-green { animation: greenGlow 2s infinite; }
            .glow-blue { animation: blueGlow 2s infinite; }
            .glow-yellow { animation: yellowGlow 1.5s infinite; }
            .glow-red { animation: redGlow 1s infinite; }
            .glow-purple { animation: purpleGlow 0.8s infinite; }
        </style>
    </head>
    <body class="min-h-screen flex flex-col select-none pb-24 overflow-x-hidden">
        
        <header class="glass-cyber p-4 flex justify-between items-center sticky top-0 z-50 border-b border-cyan-500/20">
            <div class="flex items-center gap-2 bg-cyan-950/40 border border-cyan-500/30 px-3 py-1.5 rounded-xl shadow-[0_0_15px_rgba(0,240,255,0.1)]">
                <span class="text-cyan-400 font-bold">₽</span>
                <span id="balance" class="font-cyber font-black text-lg text-cyan-300">50 000</span>
            </div>
            
            <div class="flex items-center gap-2">
                <button id="admin-tab-btn" onclick="switchTab('admin')" class="hidden bg-rose-950/60 border border-rose-500/50 text-rose-400 px-3 py-1.5 rounded-xl font-bold text-xs tracking-wider shadow-[0_0_15px_rgba(244,63,94,0.3)] active:scale-95 transition">
                    👑 АДМИНКА
                </button>
                <div class="text-xs bg-slate-900/80 px-3 py-1.5 rounded-xl border border-slate-700 text-slate-300 font-bold">
                    LVL <span id="level" class="text-cyan-400">1</span>
                </div>
            </div>
        </header>

        <nav class="flex border-b border-cyan-500/20 bg-slate-950/80 backdrop-blur-md sticky top-[65px] z-40">
            <button onclick="switchTab('game')" id="tab-game-btn" class="flex-1 py-3 text-center font-cyber text-xs tracking-widest text-cyan-400 border-b-2 border-cyan-400 transition">СЛОТЫ</button>
            <button onclick="switchTab('garage')" id="tab-garage-btn" class="flex-1 py-3 text-center font-cyber text-xs tracking-widest text-slate-400 transition">ГАРАЖ (<span id="garage-count">0</span>)</button>
            <button onclick="switchTab('market')" id="tab-market-btn" class="flex-1 py-3 text-center font-cyber text-xs tracking-widest text-slate-400 transition">БИРЖА</button>
        </nav>

        <div id="tab-game" class="p-4 flex flex-col items-center flex-1 max-w-md mx-auto w-full">
            <div class="w-full mb-6">
                <label class="block text-xs font-cyber text-cyan-400 mb-2 uppercase tracking-widest">СЕГМЕНТ СЕТИ:</label>
                <select id="country-select" class="w-full bg-slate-900/90 border border-cyan-500/30 rounded-xl p-3.5 text-white font-bold focus:outline-none focus:border-cyan-400 transition">
                    <option value="ru">🇷🇺 РОССИЯ (ГОСТ 2100)</option>
                    <option value="ua">🇺🇦 УКРАИНА (UA-NET)</option>
                    <option value="by">🇧🇾 БЕЛАРУСЬ (BY-GRID)</option>
                </select>
            </div>

            <div class="w-full my-6 flex justify-center">
                <div id="plate-box" class="relative bg-white text-black border-4 rounded-xl shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300 glow-gray">
                    <div class="flex items-center gap-2">
                        <div id="flag-container" class="flex flex-col items-center justify-center border-r-2 border-slate-300 pr-2">
                            <svg id="svg-flag" class="w-8 h-6 rounded shadow-sm" viewBox="0 0 36 24">
                                <rect width="36" height="8" fill="#fff"/>
                                <rect y="8" width="36" height="8" fill="#0039a6"/>
                                <rect y="16" width="36" height="8" fill="#d52b1e"/>
                            </svg>
                            <span id="country-code" class="text-[10px] font-black mt-0.5 tracking-wider text-red-700">RUS</span>
                        </div>
                    </div>
                    <div class="flex-1 text-center font-cyber font-black text-3xl tracking-widest px-1 overflow-hidden">
                        <span id="plate-text">А777АА 777</span>
                    </div>
                </div>
            </div>

            <div id="info-box" class="text-center my-2 hidden glass-cyber p-3 rounded-xl w-full border border-cyan-500/30">
                <p id="res-title" class="text-xs font-cyber font-bold text-cyan-300 uppercase tracking-widest"></p>
                <p class="text-xs text-slate-300 mt-1">ЦЕННОСТЬ: <span id="res-val" class="text-emerald-400 font-bold font-cyber">0</span> ₽</p>
            </div>

            <div class="w-full space-y-3 mt-auto pt-6">
                <button onclick="spin('normal')" class="w-full bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 font-cyber font-bold py-4 rounded-xl shadow-[0_0_20px_rgba(0,240,255,0.3)] transition flex items-center justify-between px-5 active:scale-[0.98]">
                    <span class="text-xs tracking-wider">КВАНТОВЫЙ СПИН</span>
                    <span class="text-xs bg-black/40 border border-cyan-400/30 px-2.5 py-1 rounded-lg text-cyan-300">1 000 ₽</span>
                </button>
                <button onclick="spin('elite')" class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 font-cyber font-bold py-4 rounded-xl shadow-[0_0_25px_rgba(168,85,247,0.4)] transition flex items-center justify-between px-5 active:scale-[0.98]">
                    <span class="text-xs tracking-wider">ГИПЕР-СПИН (ХОТ-ШАНС)</span>
                    <span class="text-xs bg-black/40 border border-pink-400/30 px-2.5 py-1 rounded-lg text-pink-200">5 000 ₽</span>
                </button>
            </div>
        </div>

        <div id="tab-garage" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <h2 class="text-sm font-cyber text-cyan-400 mb-4 tracking-wider">ВАШ КВАНТОВЫЙ ГАРАЖ</h2>
            <div id="garage-list" class="space-y-3">
                <div class="text-center text-slate-500 py-12 text-xs font-cyber">ГАРАЖ ПУСТ. НАЧНИТЕ КРУТКУ!</div>
            </div>
        </div>

        <div id="tab-market" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <h2 class="text-sm font-cyber text-cyan-400 mb-1 tracking-wider">ГЛОБАЛЬНАЯ КИБЕР-БИРЖА</h2>
            <p class="text-xs text-slate-400 mb-4">Торговля редкими номерами сетевых агентов.</p>
            <div id="market-list" class="space-y-3"></div>
        </div>

        <div id="tab-admin" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <div class="glass-cyber p-5 rounded-2xl border border-rose-500/40 shadow-[0_0_30px_rgba(244,63,94,0.15)]">
                <div class="flex items-center gap-2 mb-4">
                    <span class="text-xl">👑</span>
                    <h2 class="text-sm font-cyber font-black text-rose-400 tracking-wider">ТЕРМИНАЛ АДМИНИСТРАТОРА</h2>
                </div>
                <p class="text-xs text-slate-400 mb-4">Доступ открыт для ID: <code class="text-rose-300 font-bold">__ADMIN_ID__</code></p>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-[10px] font-cyber text-slate-400 mb-1">ЦЕЛЕВОЙ TELEGRAM ID:</label>
                        <input id="admin-target-id" type="number" value="7271568260" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-mono text-sm focus:outline-none focus:border-rose-500">
                    </div>

                    <div>
                        <label class="block text-[10px] font-cyber text-slate-400 mb-1">СУММА РУБЛЕЙ:</label>
                        <input id="admin-money-amount" type="number" value="100000" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-mono text-sm focus:outline-none focus:border-rose-500">
                    </div>
                    <button onclick="adminGiveMoney()" class="w-full bg-emerald-600/30 border border-emerald-500/60 hover:bg-emerald-600/50 text-emerald-300 font-cyber text-xs py-3 rounded-xl transition">
                        ВЫДАТЬ РУБЛИ ПО ID
                    </button>

                    <hr class="border-slate-800 my-2">

                    <div>
                        <label class="block text-[10px] font-cyber text-slate-400 mb-1">КАСТОМНЫЙ НОМЕР:</label>
                        <input id="admin-plate-num" type="text" placeholder="Х777ХХ 777" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-cyber text-sm focus:outline-none focus:border-rose-500 mb-2">
                        
                        <label class="block text-[10px] font-cyber text-slate-400 mb-1">РЕДКОСТЬ:</label>
                        <select id="admin-plate-rarity" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white text-xs mb-3">
                            <option value="обычный">Обычный (Серый)</option>
                            <option value="редкий">Редкий (Зеленый)</option>
                            <option value="сверхредкий">Сверхредкий (Синий)</option>
                            <option value="легендарный">Легендарный (Желтый)</option>
                            <option value="мифический">Мифический (Красный)</option>
                            <option value="мистический">Мистический (Пурпурный)</option>
                        </select>
                    </div>
                    <button onclick="adminGiveCustomPlate()" class="w-full bg-purple-600/30 border border-purple-500/60 hover:bg-purple-600/50 text-purple-300 font-cyber text-xs py-3 rounded-xl transition">
                        СОЗДАТЬ И ВЫДАТЬ НОМЕР
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
                balance: 50000,
                level: 1,
                garage: [],
                market: [
                    { id: 1, number: "Х777ХХ 777", title: "🔥 МИФИЧЕСКИЙ НОМЕР", price: 350000, seller: "CyberLord", rarity: "мифический", color: "red" },
                    { id: 2, number: "AA 7777 AA", title: "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", price: 150000, seller: "KiyvNet", rarity: "легендарный", color: "yellow" }
                ]
            };

            function updateUI() {
                document.getElementById('balance').innerText = state.balance.toLocaleString('ru-RU');
                document.getElementById('level').innerText = state.level;
                document.getElementById('garage-count').innerText = state.garage.length;
                renderGarage();
                renderMarket();
            }

            function switchTab(tab) {
                ['game', 'garage', 'market', 'admin'].forEach(t => {
                    let el = document.getElementById(`tab-${t}`);
                    let btn = document.getElementById(`tab-${t}-btn`);
                    if (el) el.classList.add('hidden');
                    if (btn) btn.className = "flex-1 py-3 text-center font-cyber text-xs tracking-widest text-slate-400 transition";
                });
                
                document.getElementById(`tab-${tab}`).classList.remove('hidden');
                let activeBtn = document.getElementById(`tab-${tab}-btn`);
                if (activeBtn) activeBtn.className = "flex-1 py-3 text-center font-cyber text-xs tracking-widest text-cyan-400 border-b-2 border-cyan-400 transition";
            }

            function updatePlateVisual(country, numberText, colorClass) {
                let svgFlag = document.getElementById('svg-flag');
                let codeSpan = document.getElementById('country-code');
                let plateBox = document.getElementById('plate-box');
                
                plateBox.className = `relative bg-white text-black border-4 rounded-xl shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300 glow-${colorClass}`;
                document.getElementById('plate-text').innerText = numberText;

                if (country === 'ua') {
                    codeSpan.innerText = 'UA';
                    codeSpan.className = "text-[10px] font-black mt-0.5 tracking-wider text-blue-800";
                    svgFlag.innerHTML = '<rect width="36" height="12" fill="#0057b7"/><rect y="12" width="36" height="12" fill="#ffd700"/>';
                } else if (country === 'ru') {
                    codeSpan.innerText = 'RUS';
                    codeSpan.className = "text-[10px] font-black mt-0.5 tracking-wider text-red-700";
                    svgFlag.innerHTML = '<rect width="36" height="8" fill="#fff"/><rect y="8" width="36" height="8" fill="#0039a6"/><rect y="16" width="36" height="8" fill="#d52b1e"/>';
                } else if (country === 'by') {
                    codeSpan.innerText = 'BY';
                    codeSpan.className = "text-[10px] font-black mt-0.5 tracking-wider text-red-600";
                    svgFlag.innerHTML = '<rect width="36" height="15" fill="#d52b1e"/><rect y="15" width="36" height="9" fill="#008751"/><rect width="10" height="24" fill="#fff"/>';
                }
            }

            document.getElementById('country-select').addEventListener('change', (e) => {
                let c = e.target.value;
                if (c === 'ru') updatePlateVisual('ru', 'А777АА 777', 'yellow');
                else if (c === 'ua') updatePlateVisual('ua', 'AA 7777 AA', 'yellow');
                else if (c === 'by') updatePlateVisual('by', '7777 AB-7', 'blue');
            });

            async function spin(tier) {
                let cost = tier === 'normal' ? 1000 : 5000;
                if (state.balance < cost) {
                    alert('Недостаточно квантовых рублей!');
                    return;
                }
                state.balance -= cost;
                updateUI();

                let country = document.getElementById('country-select').value;
                let infoBox = document.getElementById('info-box');
                infoBox.classList.add('hidden');

                let counter = 0;
                let interval = setInterval(() => {
                    let randStr = Math.random().toString(36).substring(2, 8).toUpperCase();
                    updatePlateVisual(country, randStr, 'gray');
                    counter++;
                    if (counter > 10) clearInterval(interval);
                }, 40);

                let response = await fetch(`/api/spin?country=${country}&tier=${tier}`);
                if (response.ok) {
                    let data = await response.json();
                    setTimeout(() => {
                        updatePlateVisual(country, data.number, data.color);
                        document.getElementById('res-title').innerText = data.title;
                        document.getElementById('res-val').innerText = data.value.toLocaleString('ru-RU');
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
                    list.innerHTML = '<div class="text-center text-slate-500 py-12 text-xs font-cyber">ГАРАЖ ПУСТ. НАЧНИТЕ КРУТКУ!</div>';
                    return;
                }
                list.innerHTML = state.garage.map((item, index) => `
                    <div class="glass-cyber p-4 rounded-xl flex justify-between items-center border glow-${item.color}">
                        <div>
                            <span class="text-[10px] font-cyber font-bold uppercase tracking-wider text-cyan-300">${item.title}</span>
                            <div class="text-lg font-cyber font-black text-white mt-0.5">${item.number}</div>
                            <span class="text-xs text-emerald-400 font-bold">ЦЕННОСТЬ: ${item.value.toLocaleString('ru-RU')} ₽</span>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="sellItem(${index})" class="bg-emerald-950/60 border border-emerald-500/50 hover:bg-emerald-900 text-emerald-300 px-3 py-2 rounded-lg text-xs font-cyber transition">ПРОДАТЬ</button>
                            <button onclick="listToMarket(${index})" class="bg-cyan-950/60 border border-cyan-500/50 hover:bg-cyan-900 text-cyan-300 px-3 py-2 rounded-lg text-xs font-cyber transition">НА БИРЖУ</button>
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
                    title: item.title,
                    price: Math.round(item.value * 1.3),
                    seller: "Вы",
                    color: item.color
                });
                state.garage.splice(index, 1);
                updateUI();
                alert("Номер успешно выставлен на глобальную биржу!");
            }

            function renderMarket() {
                let list = document.getElementById('market-list');
                list.innerHTML = state.market.map((item, index) => `
                    <div class="glass-cyber p-4 rounded-xl flex justify-between items-center border border-cyan-500/20">
                        <div>
                            <span class="text-[10px] text-slate-400 font-cyber">АГЕНТ: ${item.seller}</span>
                            <div class="text-lg font-cyber font-black text-cyan-300 mt-0.5">${item.number}</div>
                            <span class="text-xs text-slate-300">${item.title}</span>
                        </div>
                        <div class="text-right">
                            <div class="text-emerald-400 font-bold font-cyber mb-1 text-sm">${item.price.toLocaleString('ru-RU')} ₽</div>
                            ${item.seller !== "Вы" ? `<button onclick="buyMarketItem(${index})" class="bg-cyan-600 hover:bg-cyan-500 text-black px-3 py-1.5 rounded-lg text-xs font-cyber font-bold transition">КУПИТЬ</button>` : `<span class="text-[10px] text-slate-500 font-cyber">ВАШ ЛОТ</span>`}
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
                state.garage.unshift({ number: item.number, title: item.title, value: item.price, color: item.color || 'blue' });
                state.market.splice(index, 1);
                updateUI();
                tg.HapticFeedback?.notificationOccurred('success');
            }

            function adminGiveMoney() {
                let targetId = document.getElementById('admin-target-id').value;
                let amount = parseInt(document.getElementById('admin-money-amount').value) || 0;
                state.balance += amount;
                updateUI();
                alert(`Админ-протокол: успешно начислено ${amount.toLocaleString('ru-RU')} ₽ для ID ${targetId}!`);
            }

            function adminGiveCustomPlate() {
                let num = document.getElementById('admin-plate-num').value.trim() || "VIP 001";
                let rarity = document.getElementById('admin-plate-rarity').value;
                
                let colorMap = { "обычный": "gray", "редкий": "green", "сверхредкий": "blue", "легендарный": "yellow", "мифический": "red", "мистический": "purple" };
                let color = colorMap[rarity] || "blue";

                state.garage.unshift({
                    number: num,
                    title: `👑 ЭКСКЛЮЗИВ СЕТИ (${rarity.toUpperCase()})`,
                    value: rarity === 'мистический' ? 1000000 : 250000,
                    color: color
                });
                updateUI();
                alert(`Слот "${num}" (${rarity}) успешно внедрен в ваш гараж!`);
            }

            updateUI();
            updatePlateVisual('ru', 'А777АА 777', 'yellow');
        </script>
    </body>
    </html>
    """
    return html_content.replace("__ADMIN_ID__", str(ADMIN_TG_ID))