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
        text="🚗 Запустить Авто-Рынок Номеров", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    await message.answer(
        "👋 **Добро пожаловать в Авто-Рынок Номеров!**\n\n"
        "🎰 Крути рулетку автономеров Украины, России и Беларуси.\n"
        "🔥 Выбивай редкие блатные номера, собирай гараж и продавай их на бирже за **рубли (₽)**!",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@app.on_event("startup")
async def on_startup():
    async def run_bot():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    asyncio.create_task(run_bot())

UA_SERIES = ['AA', 'KA', 'BC', 'HC', 'AE', 'BH', 'BI', 'AX', 'AP', 'CB', 'ІH']
RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
RU_REGIONS = ['77', '99', '177', '777', '78', '98', '161', '50', '190']
BY_LETTERS = ['AB', 'BM', 'CT', 'MH', 'PB', 'OO']
BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7']

@app.get("/api/spin")
def spin_plates(country: str, tier: str = "normal"):
    if country == "ua":
        is_elite = random.random() < (0.18 if tier == "elite" else 0.04)
        series = random.choice(UA_SERIES)
        if is_elite:
            dig = str(random.choice([1, 3, 7, 9])) * 4
            number_str = f"{series} {dig} {series}"
            value = random.randint(50000, 250000)
            title = "🇺🇦 УКРАИНА | ЭЛИТНЫЙ"
        else:
            dig = f"{random.randint(1, 9999):04d}"
            suf = random.choice(['AA', 'AB', 'BA', 'BX'])
            number_str = f"{series} {dig} {suf}"
            value = random.randint(1500, 8000)
            title = "🇺🇦 Украина | Стандарт"

    elif country == "ru":
        is_elite = random.random() < (0.18 if tier == "elite" else 0.04)
        l1 = random.choice(RU_LETTERS)
        l23 = "".join(random.choices(RU_LETTERS, k=2))
        reg = random.choice(RU_REGIONS)
        if is_elite:
            dig = random.choice(["111", "333", "555", "777", "001", "770"])
            number_str = f"А{dig}АА {reg}"
            value = random.randint(70000, 350000)
            title = "🇷🇺 РОССИЯ | БЛАТНОЙ"
        else:
            dig = f"{random.randint(1, 999):03d}"
            number_str = f"{l1}{dig}{l23} {reg}"
            value = random.randint(2000, 9500)
            title = "🇷🇺 Россия | Стандарт"

    elif country == "by":
        is_elite = random.random() < (0.18 if tier == "elite" else 0.04)
        dig = f"{random.randint(1, 9999):04d}"
        let = random.choice(BY_LETTERS)
        reg = random.choice(BY_REGIONS)
        if is_elite:
            dig = str(random.choice([7, 5, 9])) * 4
            number_str = f"{dig} ОО-{reg}"
            value = random.randint(45000, 200000)
            title = "🇧🇾 БЕЛАРУСЬ | ЭЛИТНЫЙ"
        else:
            number_str = f"{dig} {let}-{reg}"
            value = random.randint(1200, 7500)
            title = "🇧🇾 Беларусь | Стандарт"

    return {
        "number": number_str,
        "title": title,
        "value": value,
        "country": country,
        "is_elite": is_elite
    }

@app.get("/", response_class=HTMLResponse)
def get_webapp():
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Авто-Рынок Номеров</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&family=PT+Sans+Caption:wght@700&display=swap');
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #0b0f17;
            }}
            .font-plate {{
                font-family: 'PT Sans Caption', sans-serif;
            }}
            .glass-panel {{
                background: rgba(18, 24, 38, 0.75);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }}
        </style>
    </head>
    <body class="text-slate-100 min-h-screen flex flex-col select-none pb-20">
        
        <!-- Шапка: Баланс в рублях и профиль -->
        <header class="bg-slate-900/80 backdrop-blur-md border-b border-slate-800/80 p-4 flex justify-between items-center sticky top-0 z-50">
            <div class="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-xl">
                <span class="text-base font-bold text-emerald-400">₽</span>
                <span id="balance" class="font-mono font-black text-lg text-emerald-400">15 000</span>
            </div>
            
            <div class="flex items-center gap-2">
                <!-- Секретная кнопка админки (появится только для ID 7271568260) -->
                <button id="admin-tab-btn" onclick="switchTab('admin')" class="hidden bg-rose-600/20 border border-rose-500/40 text-rose-400 px-3 py-1.5 rounded-xl font-bold text-xs flex items-center gap-1 shadow-lg shadow-rose-900/20 active:scale-95 transition">
                    👑 Адмінка
                </button>
                
                <div class="text-xs bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700/60 text-slate-300 font-semibold">
                    ⭐ Уровень: <span id="level" class="font-bold text-indigo-400">1</span>
                </div>
            </div>
        </header>

        <!-- Навигационные вкладки -->
        <nav class="flex border-b border-slate-800/80 bg-slate-900/40 backdrop-blur-md sticky top-[65px] z-40">
            <button onclick="switchTab('game')" id="tab-game-btn" class="flex-1 py-3 text-center font-bold text-indigo-400 border-b-2 border-indigo-500 transition">🎰 Крутка</button>
            <button onclick="switchTab('garage')" id="tab-garage-btn" class="flex-1 py-3 text-center text-slate-400 transition">🚗 Гараж (<span id="garage-count">0</span>)</button>
            <button onclick="switchTab('market')" id="tab-market-btn" class="flex-1 py-3 text-center text-slate-400 transition">📈 Биржа</button>
        </nav>

        <!-- 🎰 ВКЛАДКА 1: КРУТКА НОМЕРОВ -->
        <div id="tab-game" class="p-4 flex flex-col items-center flex-1 max-w-md mx-auto w-full">
            
            <!-- Выбор страны -->
            <div class="w-full mb-6">
                <label class="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Выберите страну автономера:</label>
                <select id="country-select" class="w-full bg-slate-800/90 border border-slate-700/80 rounded-xl p-3.5 text-white font-semibold focus:outline-none focus:border-indigo-500 transition">
                    <option value="ru">🇷🇺 Россия (RUS)</option>
                    <option value="ua">🇺🇦 Украина (UA)</option>
                    <option value="by">🇧🇾 Беларусь (BY)</option>
                </select>
            </div>

            <!-- ИНТЕРФЕЙС АВТОНОМЕРА (РЕАЛИСТИЧНЫЙ ВИЗУАЛ) -->
            <div class="w-full my-4 flex justify-center">
                <div id="plate-container" class="relative bg-white text-black border-[3px] border-black rounded-lg shadow-2xl w-full max-w-[340px] h-28 flex items-center justify-between px-3 overflow-hidden transition-all duration-300">
                    
                    <!-- РЕЖИМ РОССИЯ (по умолчанию) -->
                    <div id="plate-ru-body" class="w-full flex items-center justify-between font-plate font-black text-black">
                        <div id="plate-ru-main" class="text-3xl tracking-tighter">A 000 AA</div>
                        <div class="h-full border-l-2 border-black pl-2 flex flex-col items-center justify-center">
                            <span id="plate-ru-reg" class="text-xl leading-none">777</span>
                            <div class="flex items-center gap-1 mt-1">
                                <span class="text-[9px] font-bold tracking-widest">RUS</span>
                                <span class="text-xs">🇷🇺</span>
                            </div>
                        </div>
                    </div>

                    <!-- РЕЖИМ УКРАИНА / БЕЛАРУСЬ (Скрыто по умолчанию) -->
                    <div id="plate-other-body" class="hidden w-full flex items-center justify-between font-plate font-black text-black">
                        <div id="plate-left-badge" class="bg-blue-700 text-white h-full -ml-3 px-2 flex flex-col items-center justify-center gap-1 border-r-2 border-black">
                            <span id="plate-flag" class="text-sm leading-none">🇺🇦</span>
                            <span id="plate-country-code" class="text-[10px] font-bold">UA</span>
                        </div>
                        <div id="plate-other-main" class="flex-1 text-center text-2xl tracking-widest px-1">AA 0000 AA</div>
                    </div>

                </div>
            </div>

            <!-- Результат прокрута -->
            <div id="info-box" class="text-center my-4 hidden bg-slate-900/60 border border-slate-800 p-3 rounded-xl w-full">
                <p id="res-title" class="text-xs font-bold text-indigo-400 uppercase tracking-wider"></p>
                <p class="text-xs text-slate-300 mt-1">Рыночная стоимость: <span id="res-val" class="text-emerald-400 font-bold">0</span> ₽</p>
            </div>

            <!-- Кнопки крутки -->
            <div class="w-full space-y-3 mt-auto pt-4">
                <button onclick="spin('normal')" class="w-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 font-bold py-4 rounded-xl shadow-lg shadow-indigo-950/50 transition flex items-center justify-between px-5 active:scale-[0.98]">
                    <span class="text-sm">🎰 Обычное вращение</span>
                    <span class="text-xs bg-black/30 border border-white/10 px-2.5 py-1 rounded-lg text-indigo-200">1 000 ₽</span>
                </button>
                <button onclick="spin('elite')" class="w-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 font-bold py-4 rounded-xl shadow-lg shadow-amber-950/50 transition flex items-center justify-between px-5 active:scale-[0.98]">
                    <span class="text-sm">🔥 Премиум (Шанс блатных)</span>
                    <span class="text-xs bg-black/30 border border-white/10 px-2.5 py-1 rounded-lg text-amber-100">5 000 ₽</span>
                </button>
            </div>
        </div>

        <!-- 🚗 ВКЛАДКА 2: ГАРАЖ -->
        <div id="tab-garage" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <h2 class="text-base font-bold mb-4 text-slate-200">Ваша коллекция номеров</h2>
            <div id="garage-list" class="space-y-3">
                <div class="text-center text-slate-500 py-12 text-sm">Гараж пуст. Выбейте свой первый номер!</div>
            </div>
        </div>

        <!-- 📈 ВКЛАДКА 3: БИРЖА / РЫНОК -->
        <div id="tab-market" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <h2 class="text-base font-bold mb-1 text-slate-200">Автомобильная Биржа</h2>
            <p class="text-xs text-slate-400 mb-4">Покупайте редкие номера у других игроков за рубли.</p>
            <div id="market-list" class="space-y-3"></div>
        </div>

        <!-- 👑 ВКЛАДКА 4: АДМИН-ПАНЕЛЬ (Доступна только для ADMIN_TG_ID) -->
        <div id="tab-admin" class="p-4 hidden flex-1 max-w-md mx-auto w-full">
            <div class="glass-panel p-5 rounded-2xl border border-rose-500/30">
                <div class="flex items-center gap-2 mb-4">
                    <span class="text-xl">👑</span>
                    <h2 class="text-lg font-extrabold text-rose-400">Панель Владельца</h2>
                </div>
                <p class="text-xs text-slate-400 mb-6">Доступ разрешен для Telegram ID: <code class="text-rose-300 font-bold">{ADMIN_TG_ID}</code></p>
                
                <div class="space-y-3">
                    <button onclick="adminAddMoney(100000)" class="w-full bg-emerald-600/30 border border-emerald-500/50 hover:bg-emerald-600/40 text-emerald-300 font-bold py-3 rounded-xl text-sm transition">
                        +100 000 ₽ на баланс
                    </button>
                    <button onclick="adminAddMoney(1000000)" class="w-full bg-amber-600/30 border border-amber-500/50 hover:bg-amber-600/40 text-amber-300 font-bold py-3 rounded-xl text-sm transition">
                        +1 000 000 ₽ на баланс
                    </button>
                    <button onclick="adminGiveCustomPlate()" class="w-full bg-indigo-600/30 border border-indigo-500/50 hover:bg-indigo-600/40 text-indigo-300 font-bold py-3 rounded-xl text-sm transition">
                        Выдать блатный номер "А777АА 77"
                    </button>
                </div>
            </div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            // Проверка Telegram ID на права Администратора
            const ADMIN_ID = {ADMIN_TG_ID};
            let currentUserTgId = tg.initDataUnsafe?.user?.id || 0;

            if (currentUserTgId === ADMIN_ID) {{
                document.getElementById('admin-tab-btn').classList.remove('hidden');
            }}

            let state = {{
                balance: 15000,
                level: 1,
                garage: [],
                market: [
                    {{ id: 1, number: "А777АА 77", title: "🇷🇺 Блатные семерки", price: 250000, seller: "Игрок #1" }},
                    {{ id: 2, number: "AA 0001 AA", title: "🇺🇦 Первый номер", price: 180000, seller: "Киевлянин" }},
                    {{ id: 3, number: "7777 OO-7", title: "🇧🇾 Минский элитный", price: 120000, seller: "Батька" }}
                ]
            }};

            function updateUI() {{
                document.getElementById('balance').innerText = state.balance.toLocaleString('ru-RU');
                document.getElementById('level').innerText = state.level;
                document.getElementById('garage-count').innerText = state.garage.length;
                renderGarage();
                renderMarket();
            }}

            function switchTab(tab) {{
                ['game', 'garage', 'market', 'admin'].forEach(t => {{
                    let el = document.getElementById(`tab-${{t}}`);
                    let btn = document.getElementById(`tab-${{t}}-btn`);
                    if (el) el.classList.add('hidden');
                    if (btn) btn.className = "flex-1 py-3 text-center text-slate-400 transition";
                }});
                
                document.getElementById(`tab-${{tab}}`).classList.remove('hidden');
                let activeBtn = document.getElementById(`tab-${{tab}}-btn`);
                if (activeBtn) activeBtn.className = "flex-1 py-3 text-center font-bold text-indigo-400 border-b-2 border-indigo-500 transition";
            }}

            // Динамический визуализатор автономера
            function updatePlateStyle(country, text = "А000АА 77") {{
                let ruBody = document.getElementById('plate-ru-body');
                let otherBody = document.getElementById('plate-other-body');
                
                if (country === 'ru') {{
                    ruBody.classList.remove('hidden');
                    otherBody.classList.add('hidden');
                    
                    let parts = text.split(" ");
                    document.getElementById('plate-ru-main').innerText = parts[0] || "А000АА";
                    document.getElementById('plate-ru-reg').innerText = parts[1] || "77";
                }} else {{
                    ruBody.classList.add('hidden');
                    otherBody.classList.remove('hidden');
                    
                    let flag = document.getElementById('plate-flag');
                    let code = document.getElementById('plate-country-code');
                    
                    if (country === 'ua') {{
                        flag.innerText = '🇺🇦';
                        code.innerText = 'UA';
                    }} else if (country === 'by') {{
                        flag.innerText = '🇧🇾';
                        code.innerText = 'BY';
                    }}
                    document.getElementById('plate-other-main').innerText = text;
                }}
            }}

            document.getElementById('country-select').addEventListener('change', (e) => {{
                let c = e.target.value;
                if (c === 'ru') updatePlateStyle('ru', 'А123АА 777');
                else if (c === 'ua') updatePlateStyle('ua', 'AA 7777 AA');
                else if (c === 'by') updatePlateStyle('by', '7777 AB-7');
            }});

            async function spin(tier) {{
                let cost = tier === 'normal' ? 1000 : 5000;
                if (state.balance < cost) {{
                    alert('Недостаточно рублей на балансе!');
                    return;
                }}
                state.balance -= cost;
                updateUI();

                let country = document.getElementById('country-select').value;
                let infoBox = document.getElementById('info-box');
                infoBox.classList.add('hidden');

                // Анимация вращения
                let counter = 0;
                let interval = setInterval(() => {{
                    let randStr = Math.random().toString(36).substring(2, 8).toUpperCase();
                    updatePlateStyle(country, randStr + " 77");
                    counter++;
                    if (counter > 12) clearInterval(interval);
                }}, 40);

                let response = await fetch(`/api/spin?country=${{country}}&tier=${{tier}}`);
                if (response.ok) {{
                    let data = await response.json();
                    setTimeout(() => {{
                        updatePlateStyle(country, data.number);
                        document.getElementById('res-title').innerText = data.title;
                        document.getElementById('res-val').innerText = data.value.toLocaleString('ru-RU');
                        infoBox.classList.remove('hidden');

                        state.garage.unshift(data);
                        updateUI();
                        tg.HapticFeedback?.notificationOccurred('success');
                    }}, 600);
                }}
            }}

            function renderGarage() {{
                let list = document.getElementById('garage-list');
                if (state.garage.length === 0) {{
                    list.innerHTML = '<div class="text-center text-slate-500 py-12 text-sm">Гараж пуст. Выбейте свой первый номер!</div>';
                    return;
                }}
                list.innerHTML = state.garage.map((item, index) => `
                    <div class="glass-panel p-4 rounded-xl flex justify-between items-center border border-slate-800">
                        <div>
                            <span class="text-[10px] font-bold text-indigo-400 uppercase tracking-wider">${{item.title}}</span>
                            <div class="text-lg font-plate font-black text-white mt-0.5">${{item.number}}</div>
                            <span class="text-xs text-emerald-400 font-semibold">Оценка: ${{item.value.toLocaleString('ru-RU')}} ₽</span>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="sellItem(${{index}})" class="bg-emerald-600/20 border border-emerald-500/40 hover:bg-emerald-600/30 text-emerald-300 px-3 py-2 rounded-lg text-xs font-bold transition">Продать</button>
                            <button onclick="listToMarket(${{index}})" class="bg-indigo-600/20 border border-indigo-500/40 hover:bg-indigo-600/30 text-indigo-300 px-3 py-2 rounded-lg text-xs font-bold transition">На биржу</button>
                        </div>
                    </div>
                `).join('');
            }}

            function sellItem(index) {{
                let item = state.garage[index];
                state.balance += item.value;
                state.garage.splice(index, 1);
                updateUI();
                tg.HapticFeedback?.impactOccurred('medium');
            }}

            function listToMarket(index) {{
                let item = state.garage[index];
                state.market.unshift({{
                    id: Date.now(),
                    number: item.number,
                    title: item.title,
                    price: Math.round(item.value * 1.25),
                    seller: "Вы"
                }});
                state.garage.splice(index, 1);
                updateUI();
                alert("Номер успешно выставлен на биржу!");
            }}

            function renderMarket() {{
                let list = document.getElementById('market-list');
                list.innerHTML = state.market.map((item, index) => `
                    <div class="glass-panel p-4 rounded-xl flex justify-between items-center border border-slate-800">
                        <div>
                            <span class="text-[10px] text-slate-400">Продавец: ${{item.seller}}</span>
                            <div class="text-lg font-plate font-black text-amber-400 mt-0.5">${{item.number}}</div>
                            <span class="text-xs text-slate-300">${{item.title}}</span>
                        </div>
                        <div class="text-right">
                            <div class="text-emerald-400 font-bold mb-1 text-sm">${{item.price.toLocaleString('ru-RU')}} ₽</div>
                            ${{item.seller !== "Вы" ? `<button onclick="buyMarketItem(${{index}})" class="bg-indigo-600 hover:bg-indigo-500 px-3 py-1.5 rounded-lg text-xs font-bold transition">Купить</button>` : `<span class="text-[10px] text-slate-500">Ваш лот</span>` }}
                        </div>
                    </div>
                `).join('');
            }}

            function buyMarketItem(index) {{
                let item = state.market[index];
                if (state.balance < item.price) {{
                    alert("Недостаточно рублей на балансе!");
                    return;
                }}
                state.balance -= item.price;
                state.garage.unshift({{ number: item.number, title: item.title, value: item.price }});
                state.market.splice(index, 1);
                updateUI();
                tg.HapticFeedback?.notificationOccurred('success');
            }}

            // АДМИН-ФУНКЦИИ
            function adminAddMoney(amount) {{
                state.balance += amount;
                updateUI();
                alert(`Успешно начислено +${{amount.toLocaleString('ru-RU')}} ₽!`);
            }}

            function adminGiveCustomPlate() {{
                state.garage.unshift({{
                    number: "А777АА 77",
                    title: "👑 ЭКСКЛЮЗИВ ВЛАДЕЛЬЦА",
                    value: 1000000
                }});
                updateUI();
                alert('Номер А777АА 77 успешно добавлен в ваш гараж!');
            }}

            updateUI();
            updatePlateStyle('ru', 'А777АА 777');
        </script>
    </body>
    </html>
    """