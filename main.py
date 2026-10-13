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

logging.basicConfig(level=logging.INFO)
app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🎮 Играть в Авто-Рынок Номеров", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    await message.answer(
        "👋 Добро пожаловать в **Авто-Рынок Номеров**!\n\n"
        "Покупай слоты, выбивай блатные номера Украины, России и Беларуси, продавай их на аукционе и ставай олигархом!",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@app.on_event("startup")
async def on_startup():
    async def run_bot():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    asyncio.create_task(run_bot())

# Базы данных для генерации со структурой под анимацию
UA_SERIES = ['AA', 'KA', 'BC', 'HC', 'AE', 'BH', 'BI', 'AX', 'AP', 'CB', 'ІH']
RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
RU_REGIONS = ['77', '99', '199', '777', '78', '98', '161', '50']
BY_LETTERS = ['AB', 'BM', 'CT', 'MH', 'PB', 'OO']
BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7']

@app.get("/api/spin")
def spin_plates(country: str, tier: str = "normal"):
    # Расчет редкости и стоимости
    price = 100 if tier == "normal" else 500
    
    if country == "ua":
        is_elite = random.random() < (0.15 if tier == "elite" else 0.03)
        series = random.choice(UA_SERIES)
        if is_elite:
            dig = str(random.choice([1, 3, 7, 9])) * 4
            number_str = f"{series} {dig} {series}"
            value = random.randint(5000, 25000)
            title = "🇺🇦 УКРАИНА | ЭЛИТНЫЙ"
        else:
            dig = f"{random.randint(1, 9999):04d}"
            suf = random.choice(['AA', 'AB', 'BA', 'BX'])
            number_str = f"{series} {dig} {suf}"
            value = random.randint(120, 800)
            title = "🇺🇦 Украина | Стандарт"

    elif country == "ru":
        is_elite = random.random() < (0.15 if tier == "elite" else 0.03)
        l1 = random.choice(RU_LETTERS)
        l23 = "".join(random.choices(RU_LETTERS, k=2))
        reg = random.choice(RU_REGIONS)
        if is_elite:
            dig = random.choice(["111", "333", "555", "777", "001"])
            number_str = f"А{dig}АА {reg}"
            value = random.randint(6000, 30000)
            title = "🇷🇺 РОССИЯ | БЛАТНОЙ"
        else:
            dig = f"{random.randint(1, 999):03d}"
            number_str = f"{l1}{dig}{l23} {reg}"
            value = random.randint(150, 900)
            title = "🇷🇺 Россия | Стандарт"

    elif country == "by":
        is_elite = random.random() < (0.15 if tier == "elite" else 0.03)
        dig = f"{random.randint(1, 9999):04d}"
        let = random.choice(BY_LETTERS)
        reg = random.choice(BY_REGIONS)
        if is_elite:
            dig = str(random.choice([7, 5, 9])) * 4
            number_str = f"{dig} ОО-{reg}"
            value = random.randint(4500, 20000)
            title = "🇧🇾 БЕЛАРУСЬ | ЭЛИТНЫЙ"
        else:
            number_str = f"{dig} {let}-{reg}"
            value = random.randint(100, 700)
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
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Авто-Рынок Номеров</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-white min-h-screen flex flex-col select-none pb-20">
        
        <!-- Шапка: Баланс и уровень -->
        <header class="bg-slate-900 border-b border-slate-800 p-4 flex justify-between items-center sticky top-0 z-50">
            <div class="flex items-center gap-2">
                <span class="text-xl">💰</span>
                <span id="balance" class="font-mono font-bold text-lg text-emerald-400">1500</span>
            </div>
            <div class="text-xs bg-slate-800 px-3 py-1.5 rounded-full border border-slate-700 text-slate-300">
                ⭐ Уровень: <span id="level" class="font-bold text-white">1</span>
            </div>
        </header>

        <!-- Навигация по вкладкам -->
        <div class="flex border-b border-slate-800 bg-slate-900/50">
            <button onclick="switchTab('game')" id="tab-game-btn" class="flex-1 py-3 text-center font-bold text-indigo-400 border-b-2 border-indigo-500">🎰 Крутить</button>
            <button onclick="switchTab('garage')" id="tab-garage-btn" class="flex-1 py-3 text-center text-slate-400">🚗 Гараж (<span id="garage-count">0</span>)</button>
            <button onclick="switchTab('market')" id="tab-market-btn" class="flex-1 py-3 text-center text-slate-400">📈 Рынок</button>
        </div>

        <!-- ВКЛАДКА 1: ИГРА / КРУТКА -->
        <div id="tab-game" class="p-4 flex flex-col items-center flex-1">
            
            <div class="w-full max-w-md mb-4 flex gap-2">
                <select id="country-select" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white font-medium">
                    <option value="ua">🇺🇦 Украина</option>
                    <option value="ru">🇷🇺 Россия</option>
                    <option value="by">🇧🇾 Беларусь</option>
                </select>
            </div>

            <!-- ТЕХНИЧЕСКИЙ БЛОК: НОМЕР КАК НА МАШИНЕ -->
            <div class="w-full max-w-md my-6 flex justify-center">
                <div id="plate-container" class="relative bg-white text-slate-900 border-4 border-slate-800 rounded-xl p-3 shadow-2xl w-80 h-32 flex items-center justify-between transition transform duration-300">
                    
                    <!-- Левый флаг / код страны -->
                    <div id="plate-left-badge" class="flex flex-col items-center justify-center border-r-2 border-slate-300 pr-2">
                        <span id="plate-flag" class="text-xl">🇺🇦</span>
                        <span id="plate-country-code" class="text-xs font-bold font-mono tracking-widest text-blue-800">UA</span>
                    </div>

                    <!-- Основной текст номера -->
                    <div class="flex-1 text-center font-mono font-black text-3xl tracking-widest px-2 overflow-hidden">
                        <span id="plate-text">AA 0000 AA</span>
                    </div>
                </div>
            </div>

            <!-- Информация о результате -->
            <div id="info-box" class="text-center mb-6 hidden">
                <p id="res-title" class="text-sm font-bold text-indigo-400 uppercase tracking-wide"></p>
                <p class="text-xs text-slate-400 mt-1">Оценка: <span id="res-val" class="text-emerald-400 font-bold">0</span> монет</p>
            </div>

            <!-- Кнопки крутки -->
            <div class="w-full max-w-md space-y-3">
                <button onclick="spin('normal')" id="spin-btn" class="w-full bg-indigo-600 hover:bg-indigo-500 font-bold py-4 rounded-xl shadow-lg transition flex items-center justify-center gap-2">
                    <span>🎰 Стандартный крут</span>
                    <span class="text-xs bg-indigo-900 px-2 py-0.5 rounded text-indigo-200">100 🪙</span>
                </button>
                <button onclick="spin('elite')" class="w-full bg-amber-600 hover:bg-amber-500 font-bold py-4 rounded-xl shadow-lg transition flex items-center justify-center gap-2">
                    <span>🔥 Премиум крут (Шанс блатных)</span>
                    <span class="text-xs bg-amber-900 px-2 py-0.5 rounded text-amber-200">500 🪙</span>
                </button>
            </div>
        </div>

        <!-- ВКЛАДКА 2: ГАРАЖ -->
        <div id="tab-garage" class="p-4 hidden flex-1">
            <h2 class="text-lg font-bold mb-4">Ваша коллекция номеров</h2>
            <div id="garage-list" class="space-y-3">
                <!-- Сюда падают сохраненные номера -->
                <div class="text-center text-slate-500 py-10">Гараж пуст. Крутите номера!</div>
            </div>
        </div>

        <!-- ВКЛАДКА 3: РЫНОК / АУКЦИОН -->
        <div id="tab-market" class="p-4 hidden flex-1">
            <h2 class="text-lg font-bold mb-2">Биржа номеров</h2>
            <p class="text-xs text-slate-400 mb-4">Покупайте и продавайте редкие номера у других игроков.</p>
            <div id="market-list" class="space-y-3">
                <!-- Динамические лоты -->
            </div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            let state = {
                balance: 1500,
                level: 1,
                garage: [],
                market: [
                    { id: 1, number: "777 АА 77", title: "🇷🇺 Блатные три семерки", price: 12000, seller: "Игрок #481" },
                    { id: 2, number: "AA 0001 AA", title: "🇺🇦 Первый киевский", price: 25000, seller: "Магнат" },
                    { id: 3, number: "0002 OO-7", title: "🇧🇾 Элитный минский", price: 9500, seller: "Батька" }
                ]
            };

            function updateUI() {
                document.getElementById('balance').innerText = state.balance;
                document.getElementById('level').innerText = state.level;
                document.getElementById('garage-count').innerText = state.garage.length;
                renderGarage();
                renderMarket();
            }

            function switchTab(tab) {
                ['game', 'garage', 'market'].forEach(t => {
                    document.getElementById(`tab-${t}`).classList.add('hidden');
                    document.getElementById(`tab-${t}-btn`).className = "flex-1 py-3 text-center text-slate-400";
                });
                document.getElementById(`tab-${tab}`).classList.remove('hidden');
                document.getElementById(`tab-${tab}-btn`).className = "flex-1 py-3 text-center font-bold text-indigo-400 border-b-2 border-indigo-500";
            }

            // Оформление визуала плашки номера по странам
            function updatePlateStyle(country) {
                let flag = document.getElementById('plate-flag');
                let code = document.getElementById('plate-country-code');
                let container = document.getElementById('plate-container');

                if (country === 'ua') {
                    flag.innerText = '🇺🇦';
                    code.innerText = 'UA';
                    code.className = "text-xs font-bold font-mono tracking-widest text-blue-700";
                    container.className = "relative bg-white text-slate-900 border-4 border-slate-800 rounded-xl p-3 shadow-2xl w-80 h-32 flex items-center justify-between";
                } else if (country === 'ru') {
                    flag.innerText = '🇷🇺';
                    code.innerText = 'RUS';
                    code.className = "text-xs font-bold font-mono tracking-widest text-red-700";
                    container.className = "relative bg-white text-slate-900 border-4 border-slate-800 rounded-xl p-3 shadow-2xl w-80 h-32 flex items-center justify-between";
                } else if (country === 'by') {
                    flag.innerText = '🇧🇾';
                    code.innerText = 'BY';
                    code.className = "text-xs font-bold font-mono tracking-widest text-red-600";
                    container.className = "relative bg-white text-slate-900 border-4 border-slate-800 rounded-xl p-3 shadow-2xl w-80 h-32 flex items-center justify-between";
                }
            }

            document.getElementById('country-select').addEventListener('change', (e) => {
                updatePlateStyle(e.target.value);
            });

            async function spin(tier) {
                let cost = tier === 'normal' ? 100 : 500;
                if (state.balance < cost) {
                    alert('Недостаточно монет!');
                    return;
                }
                state.balance -= cost;
                updateUI();

                let country = document.getElementById('country-select').value;
                updatePlateStyle(country);

                // Эффект крутки (анимация рандома)
                let plateText = document.getElementById('plate-text');
                let infoBox = document.getElementById('info-box');
                infoBox.classList.add('hidden');

                let counter = 0;
                let interval = setInterval(() => {
                    plateText.innerText = Math.random().toString(36).substring(2, 9).toUpperCase();
                    counter++;
                    if(counter > 10) clearInterval(interval);
                }, 50);

                let response = await fetch(`/api/spin?country=${country}&tier=${tier}`);
                if(response.ok) {
                    let data = await response.json();
                    setTimeout(() => {
                        plateText.innerText = data.number;
                        document.getElementById('res-title').innerText = data.title;
                        document.getElementById('res-val').innerText = data.value;
                        infoBox.classList.remove('hidden');

                        // Добавляем в гараж
                        state.garage.unshift(data);
                        updateUI();
                        tg.HapticFeedback.notificationOccurred('success');
                    }, 600);
                }
            }

            function renderGarage() {
                let list = document.getElementById('garage-list');
                if (state.garage.length === 0) {
                    list.innerHTML = '<div class="text-center text-slate-500 py-10">Гараж пуст. Крутите номера!</div>';
                    return;
                }
                list.innerHTML = state.garage.map((item, index) => `
                    <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl flex justify-between items-center">
                        <div>
                            <span class="text-xs text-indigo-400 font-bold">${item.title}</span>
                            <div class="text-xl font-mono font-black tracking-widest text-white mt-1">${item.number}</div>
                            <span class="text-xs text-emerald-400">Стоимость: ${item.value} 🪙</span>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="sellItem(${index})" class="bg-emerald-600 hover:bg-emerald-500 px-3 py-2 rounded-lg text-xs font-bold transition">Продать</button>
                            <button onclick="listToMarket(${index})" class="bg-indigo-600 hover:bg-indigo-500 px-3 py-2 rounded-lg text-xs font-bold transition">На рынок</button>
                        </div>
                    </div>
                `).join('');
            }

            function sellItem(index) {
                let item = state.garage[index];
                state.balance += item.value;
                state.garage.splice(index, 1);
                updateUI();
                tg.HapticFeedback.impactOccurred('medium');
            }

            function listToMarket(index) {
                let item = state.garage[index];
                state.market.unshift({
                    id: Date.now(),
                    number: item.number,
                    title: item.title,
                    price: Math.round(item.value * 1.3),
                    seller: "Вы"
                });
                state.garage.splice(index, 1);
                updateUI();
                alert("Номер успешно выставлен на биржу!");
            }

            function renderMarket() {
                let list = document.getElementById('market-list');
                list.innerHTML = state.market.map((item, index) => `
                    <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl flex justify-between items-center">
                        <div>
                            <span class="text-xs text-slate-400">Продавец: ${item.seller}</span>
                            <div class="text-xl font-mono font-black tracking-widest text-amber-400 mt-1">${item.number}</div>
                            <span class="text-xs text-slate-300">${item.title}</span>
                        </div>
                        <div class="text-right">
                            <div class="text-emerald-400 font-bold mb-2">${item.price} 🪙</div>
                            ${item.seller !== "Вы" ? `<button onclick="buyMarketItem(${index})" class="bg-indigo-600 hover:bg-indigo-500 px-3 py-1.5 rounded-lg text-xs font-bold transition">Купить</button>` : `<span class="text-xs text-slate-500">Ваш лот</span>`}
                        </div>
                    </div>
                `).join('');
            }

            function buyMarketItem(index) {
                let item = state.market[index];
                if (state.balance < item.price) {
                    alert("Недостаточно монет для покупки!");
                    return;
                }
                state.balance -= item.price;
                state.garage.unshift({ number: item.number, title: item.title, value: item.price });
                state.market.splice(index, 1);
                updateUI();
                tg.HapticFeedback.notificationOccurred('success');
            }

            updateUI();
        </script>
    </body>
    </html>
    """