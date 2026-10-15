import os
import random
import asyncio
import logging
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN", "8609625925:AAF72Vk5wI1oJJ5_QlztYq6CZqGiZBN3F6w")

# 🔑 НАСТРОЙКИ SUPABASE (Укажите ваши реальные данные или переменные окружения)
SUPABASE_URL = "https://gdxoodthdiccoaqfrttg.supabase.co"
SUPABASE_KEY = "sb_publishable_5MR8eewv0D5h_OnLSfQBSg_Z1If4Xt1"

# 👑 ТВОЙ TELEGRAM ID АДМИНА
ADMIN_TG_ID = 7271568260

logging.basicConfig(level=logging.INFO)
app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ------------------------------------------------------------------
# КЛИЕНТ БАЗЫ ДАННЫХ SUPABASE (REST API)
# ------------------------------------------------------------------
class SupabaseDB:
    @staticmethod
    def _headers():
        return {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    @classmethod
    def get_or_create_profile(cls, user_id: int, username: str = "Коллекционер"):
        url = f"{SUPABASE_URL}/rest/v1/profiles?user_id=eq.{user_id}"
        res = requests.get(url, headers=cls._headers()).json()
        if not res:
            new_user = {"user_id": user_id, "username": username, "balance": 1250000, "level": 1, "exp": 0}
            res = requests.post(f"{SUPABASE_URL}/rest/v1/profiles", headers=cls._headers(), json=new_user).json()
            return new_user
        return res[0]

    @classmethod
    def update_profile(cls, user_id: int, data: dict):
        url = f"{SUPABASE_URL}/rest/v1/profiles?user_id=eq.{user_id}"
        requests.patch(url, headers=cls._headers(), json=data)

    @classmethod
    def is_plate_taken(cls, full_code: str) -> bool:
        """Проверяет, владеет ли кто-то уже таким уникальным номером в мире игры"""
        url = f"{SUPABASE_URL}/rest/v1/active_plates?full_code=eq.{full_code}"
        res = requests.get(url, headers=cls._headers()).json()
        return len(res) > 0

    @classmethod
    def register_new_plate(cls, user_id: int, item: dict):
        full_code = f"{item['number']}_{item['region']}"
        data = {
            "owner_id": user_id,
            "number_str": item["number"],
            "region_str": item["region"],
            "full_code": full_code,
            "title": item["title"],
            "value_amount": item["value"],
            "color": item["color"],
            "country": item["country"],
            "is_on_market": False,
            "market_price": 0
        }
        res = requests.post(f"{SUPABASE_URL}/rest/v1/active_plates", headers=cls._headers(), json=data).json()
        return res[0] if isinstance(res, list) and len(res) > 0 else res

    @classmethod
    def get_user_garage(cls, user_id: int):
        url = f"{SUPABASE_URL}/rest/v1/active_plates?owner_id=eq.{user_id}&is_on_market=eq.false&order=id.desc"
        return requests.get(url, headers=cls._headers()).json()

    @classmethod
    def delete_plate(cls, plate_id: int):
        """Быстрая продажа системе -> номер удаляется из базы и снова становится доступен для выбивания"""
        url = f"{SUPABASE_URL}/rest/v1/active_plates?id=eq.{plate_id}"
        requests.delete(url, headers=cls._headers())

    @classmethod
    def list_plate_on_market(cls, plate_id: int, price: int):
        """Выставить номер на биржу за свою цену"""
        url = f"{SUPABASE_URL}/rest/v1/active_plates?id=eq.{plate_id}"
        requests.patch(url, headers=cls._headers(), json={"is_on_market": True, "market_price": price})

    @classmethod
    def get_market_items(cls):
        """Получить все лоты живой P2P биржи"""
        url = f"{SUPABASE_URL}/rest/v1/active_plates?is_on_market=eq.true&order=id.desc"
        return requests.get(url, headers=cls._headers()).json()

    @classmethod
    def buy_plate_from_market(cls, buyer_id: int, plate_id: int):
        """Покупка номера у другого игрока"""
        url = f"{SUPABASE_URL}/rest/v1/active_plates?id=eq.{plate_id}&is_on_market=eq.true"
        items = requests.get(url, headers=cls._headers()).json()
        if not items:
            return {"success": False, "message": "Этот лот уже куплен или снят с продажи!"}
        
        plate = items[0]
        seller_id = plate["owner_id"]
        price = plate["market_price"]

        if buyer_id == seller_id:
            return {"success": False, "message": "Нельзя покупать собственный номер!"}

        buyer_profile = cls.get_or_create_profile(buyer_id)
        if buyer_profile["balance"] < price:
            return {"success": False, "message": "Недостаточно средств на балансе!"}

        seller_profile = cls.get_or_create_profile(seller_id)

        # Транзакция: перевод средств и передача прав на номер
        cls.update_profile(buyer_id, {"balance": buyer_profile["balance"] - price})
        cls.update_profile(seller_id, {"balance": seller_profile["balance"] + price})
        
        requests.patch(f"{SUPABASE_URL}/rest/v1/active_plates?id=eq.{plate_id}", headers=cls._headers(), json={
            "owner_id": buyer_id,
            "is_on_market": False,
            "market_price": 0
        })

        return {"success": True, "message": f"Успешная покупка за {price:,} ₽!"}

# ------------------------------------------------------------------
# БАЗЫ РЕГИОНОВ И КОДОВ (РОССИЯ, УКРАИНА, БЕЛАРУСЬ)[cite: 2]
# ------------------------------------------------------------------
RU_LETTERS = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
RU_ALL_REGIONS = [
    '01', '02', '102', '702', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '113', '14', '15', '16', '116', '716',
    '17', '18', '19', '21', '121', '22', '122', '23', '93', '123', '193', '24', '84', '88', '124', '25', '125', '26', '126', '27',
    '28', '29', '30', '31', '32', '33', '34', '134', '35', '36', '136', '37', '38', '85', '138', '39', '91', '40', '41', '82', '42', '142',
    '43', '44', '45', '46', '47', '147', '48', '49', '50', '90', '150', '190', '750', '790', '51', '52', '152', '252', '53', '54', '154',
    '55', '155', '56', '156', '57', '58', '59', '159', '60', '61', '161', '761', '62', '63', '163', '763', '64', '164', '65', '66', '96', '196',
    '67', '68', '69', '169', '70', '71', '72', '172', '73', '173', '74', '174', '774', '75', '80', '76', '77', '97', '99', '177', '197', '199', '777', '797', '799', '977',
    '78', '98', '178', '198', '79', '83', '86', '186', '87', '89', '92', '94', '95'
]

UA_OBLASTS = [
    'AA', 'KA', 'TT', 'TA', 'AM', 'KM', 'AO', 'KO', 'AP', 'KP', 'AT', 'KT', 'AI', 'KI', 
    'BA', 'HA', 'BB', 'HB', 'BC', 'HC', 'BE', 'HE', 'BH', 'HH', 'BI', 'HI', 'BK', 'HK', 
    'BM', 'HM', 'BO', 'HO', 'AX', 'KX', 'BT', 'HT', 'BX', 'HX', 'CA', 'IA', 'CB', 'IB', 
    'CE', 'IE', 'AE', 'KE', 'AH', 'KH', 'AB', 'KB', 'AC', 'KC', 'CH', 'IH'
]
UA_SUFFIXES = ['AA', 'AB', 'AC', 'AE', 'AH', 'AK', 'AM', 'AO', 'AP', 'AT', 'AX', 'BA', 'BB', 'BC', 'BE', 'BH', 'BI', 'BK', 'BM', 'BO', 'BP', 'BT', 'BX', 'CB', 'CE']

BY_LETTERS = ['AB', 'BM', 'CT', 'MH', 'PB', 'OO', 'AK', 'BI', 'CK', 'EK', 'IB', 'OI']
BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7']

# ------------------------------------------------------------------
# TELEGRAM BOT HANDLERS
# ------------------------------------------------------------------
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.button(
        text="🚗 Играть в нАмерок", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    reply_markup = reply_builder.as_markup(resize_keyboard=True)

    await message.answer(
        "🔥 **нАмерок 2100 // Full Cloud Engine** 🔥\n\n"
        "Загружены все регионы РФ, Украины и Беларуси! Уникальная мировая база номеров и живая биржа активны. Нажмите кнопку ниже!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

@app.on_event("startup")
async def on_startup():
    async def run_bot():
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    asyncio.create_task(run_bot())

# ------------------------------------------------------------------
# API СЛОТЫ И ГЕНЕРАЦИЯ С УНИКАЛЬНОСТЬЮ
# ------------------------------------------------------------------
@app.get("/api/spin")
def spin_plates(user_id: int, country: str, region: str = "auto", tier: str = "normal"):
    profile = SupabaseDB.get_or_create_profile(user_id)
    
    # Генерация с проверкой глобальной уникальности в Supabase
    max_attempts = 25
    for _ in range(max_attempts):
        roll = random.random()
        if tier == "legendary":
            if roll < 0.0033: rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 2500000
            elif roll < 0.06: rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 900000
            elif roll < 0.22: rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 350000
            elif roll < 0.55: rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 120000
            else: rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 50000
        else:
            if roll < 0.0005: rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1000000
            elif roll < 0.01: rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 400000
            elif roll < 0.06: rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 150000
            elif roll < 0.25: rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 55000
            elif roll < 0.55: rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 18000
            else: rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 5000

        if country == "ru":
            l1 = random.choice(RU_LETTERS)
            digits = f"{random.randint(1, 999):03d}" if rarity in ["обычный", "редкий"] else random.choice(["777", "001", "999", "333", "555"])
            l23 = "".join(random.choices(RU_LETTERS, k=2))
            reg = region if region != "auto" else random.choice(RU_ALL_REGIONS)
            number_str, region_str = f"{l1} {digits} {l23}", reg
        elif country == "ua":
            oblast = region if region != "auto" else random.choice(UA_OBLASTS)
            digits = f"{random.randint(1, 9999):04d}" if rarity in ["обычный", "редкий"] else str(random.choice([1, 7, 9, 0])) * 4
            if len(digits) < 4: digits = digits.zfill(4)
            suf = random.choice(UA_SUFFIXES)
            number_str, region_str = f"{oblast} {digits} {suf}", "UA"
        else:
            digits = f"{random.randint(1, 9999):04d}" if rarity in ["обычный", "редкий"] else str(random.choice([7, 5, 9, 1])) * 4
            if len(digits) < 4: digits = digits.zfill(4)
            let = random.choice(BY_LETTERS)
            reg = region if region != "auto" else random.choice(BY_REGIONS)
            number_str, region_str = f"{digits} {let}-{reg}", reg

        full_code = f"{number_str}_{region_str}"
        if not SupabaseDB.is_plate_taken(full_code):
            break

    return {
        "number": number_str,
        "region": region_str,
        "title": title,
        "value": val_mult,
        "country": country,
        "rarity": rarity,
        "color": color
    }

@app.get("/api/user/data")
def get_user_data(user_id: int):
    profile = SupabaseDB.get_or_create_profile(user_id)
    garage = SupabaseDB.get_user_garage(user_id)
    market = SupabaseDB.get_market_items()
    return {"profile": profile, "garage": garage, "market": market}

@app.post("/api/user/save_plate")
def save_plate_to_garage(user_id: int, item: dict):
    return SupabaseDB.register_new_plate(user_id, item)

@app.post("/api/user/quick_sell")
def quick_sell_plate(user_id: int, plate_id: int, price: int):
    profile = SupabaseDB.get_or_create_profile(user_id)
    SupabaseDB.update_profile(user_id, {"balance": profile["balance"] + price})
    SupabaseDB.delete_plate(plate_id)
    return {"success": True}

@app.post("/api/market/list")
def list_on_market(plate_id: int, custom_price: int):
    SupabaseDB.list_plate_on_market(plate_id, custom_price)
    return {"success": True}

@app.post("/api/market/buy")
def buy_from_market(buyer_id: int, plate_id: int):
    return SupabaseDB.buy_plate_from_market(buyer_id, plate_id)

# ------------------------------------------------------------------
# FRONTEND INTERFACE (GLASSMORPHISM 2.0 + NEON & FULL REGIONS)
# ------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def get_webapp():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>нАмерок 2100 // Enterprise Glass & Neon</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=PT+Sans+Caption:wght@700&display=swap');
            
            :root {
                --ds-bg-primary: #020617;
                --ds-surface-glass: rgba(15, 23, 42, 0.82);
                --ds-border-glass: rgba(255, 255, 255, 0.08);
            }

            * {
                box-sizing: border-box;
                -webkit-tap-highlight-color: transparent;
            }

            body {
                font-family: 'Plus Jakarta Sans', sans-serif;
                background-color: var(--ds-bg-primary);
                background-image: 
                    radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.1) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 40%);
                color: #f8fafc;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                overflow-x: hidden;
            }

            .font-plate { font-family: 'PT Sans Caption', sans-serif; }

            .glass-panel {
                background: var(--ds-surface-glass);
                backdrop-filter: blur(24px);
                -webkit-backdrop-filter: blur(24px);
                border: 1px solid var(--ds-border-glass);
                box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
            }

            .cyber-btn {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                box-shadow: 0 4px 20px rgba(79, 70, 229, 0.45);
                transition: all 0.2s ease;
            }
            .cyber-btn:active { transform: scale(0.96); }

            .gold-btn {
                background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
                box-shadow: 0 4px 25px rgba(245, 158, 11, 0.5);
                transition: all 0.2s ease;
            }
            .gold-btn:active { transform: scale(0.96); }

            @keyframes grayGlow { 0%, 100% { border-color: #475569; box-shadow: 0 0 10px rgba(71,85,105,0.3); } 50% { border-color: #94a3b8; box-shadow: 0 0 25px rgba(148,163,184,0.5); } }
            @keyframes greenGlow { 0%, 100% { border-color: #059669; box-shadow: 0 0 15px rgba(5,150,105,0.4); } 50% { border-color: #34d399; box-shadow: 0 0 35px rgba(52,211,153,0.8); } }
            @keyframes blueGlow { 0%, 100% { border-color: #2563eb; box-shadow: 0 0 20px rgba(37,99,235,0.5); } 50% { border-color: #60a5fa; box-shadow: 0 0 40px rgba(96,165,250,0.9); } }
            @keyframes yellowGlow { 0%, 100% { border-color: #d97706; box-shadow: 0 0 25px rgba(217,119,6,0.6); } 50% { border-color: #facc15; box-shadow: 0 0 50px rgba(250,204,21,1); } }
            @keyframes redGlow { 0%, 100% { border-color: #dc2626; box-shadow: 0 0 30px rgba(220,38,38,0.7); } 50% { border-color: #f87171; box-shadow: 0 0 60px rgba(248,113,113,1); } }
            @keyframes purpleGlow { 0%, 100% { border-color: #9333ea; box-shadow: 0 0 35px rgba(147,51,234,0.8); } 50% { border-color: #ec4899; box-shadow: 0 0 70px rgba(236,72,153,1); } }

            .glow-gray { animation: grayGlow 3s infinite; }
            .glow-green { animation: greenGlow 2s infinite; }
            .glow-blue { animation: blueGlow 2s infinite; }
            .glow-yellow { animation: yellowGlow 1.5s infinite; }
            .glow-red { animation: redGlow 1s infinite; }
            .glow-purple { animation: purpleGlow 0.8s infinite; }

            #toast {
                transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                transform: translateY(-140%);
                opacity: 0;
            }
            #toast.show {
                transform: translateY(0);
                opacity: 1;
            }

            select, input {
                background: rgba(15, 23, 42, 0.9) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                color: #ffffff !important;
            }
        </style>
    </head>
    <body class="min-h-screen flex flex-col select-none pb-10">
        
        <!-- TOAST -->
        <div id="toast" class="fixed top-4 left-1/2 -translate-x-1/2 z-50 pointer-events-none w-11/12 max-w-md">
            <div id="toast-body" class="glass-panel p-4 rounded-2xl flex items-center gap-3.5 border border-indigo-500/40 shadow-2xl">
                <span id="toast-icon" class="text-2xl">⚡</span>
                <span id="toast-msg" class="text-xs font-bold text-slate-100 flex-1">Уведомление</span>
            </div>
        </div>

        <!-- ШАПКА -->
        <header class="glass-panel border-b border-slate-800/80 p-3.5 flex justify-between items-center sticky top-0 z-40">
            <div class="flex flex-col">
                <span class="text-[9px] text-slate-400 font-bold uppercase tracking-wider">Облачный баланс</span>
                <span id="balance" class="font-mono font-black text-lg text-emerald-400 tracking-tight">1 250 000 ₽</span>
            </div>
            
            <div class="flex items-center gap-2">
                <div class="text-xs glass-panel px-3 py-1.5 rounded-xl text-slate-300 font-bold flex items-center gap-1.5">
                    <span>Ур. <span id="level" class="text-indigo-400">1</span></span>
                </div>
                <button onclick="showView('garage')" class="cyber-btn p-2.5 px-3.5 rounded-xl text-white font-bold text-xs">🚗 Гараж</button>
                <button onclick="showView('market')" class="gold-btn text-slate-950 p-2.5 px-3.5 rounded-xl font-bold text-xs">📈 Биржа</button>
            </div>
        </header>

        <!-- ЭКРАН СЛОТОВ -->
        <div id="view-slots" class="p-4 flex flex-col flex-1 max-w-md mx-auto w-full space-y-4">
            
            <div class="glass-panel rounded-2xl p-3 text-center flex justify-between items-center px-4 border border-indigo-500/20">
                <span class="text-xs text-amber-400 font-bold">🔥 Все регионы и областя активны</span>
                <span class="text-[9px] bg-amber-500/20 text-amber-300 border border-amber-500/40 px-2.5 py-1 rounded-lg font-black">CLOUD</span>
            </div>

            <!-- АНИМИРОВАННЫЙ НОМЕРНОЙ ЗНАК -->
            <div class="w-full flex justify-center my-3">
                <div id="plate-box" class="relative bg-white text-black border-4 rounded-2xl shadow-2xl w-full max-w-[340px] h-32 flex items-center justify-between px-3.5 overflow-hidden transition-all duration-300 glow-gray">
                    
                    <div id="ua-badge" class="hidden absolute left-0 top-0 bottom-0 bg-[#0057b7] text-white w-7 flex flex-col items-center justify-center border-r border-slate-300">
                        <div class="w-4 h-3 bg-[#ffd700] rounded-sm mb-1 shadow-sm"></div>
                        <span class="text-[9px] font-black tracking-widest text-white">UA</span>
                    </div>

                    <div id="plate-content-box" class="flex-1 flex items-center justify-center font-plate font-black text-2xl tracking-widest overflow-hidden">
                        <span id="plate-text">А 777 АА</span>
                    </div>

                    <div id="region-block" class="border-l-2 border-slate-300 pl-3 flex flex-col items-center justify-center min-w-[70px]">
                        <span id="plate-region" class="text-2xl font-plate font-black leading-none text-slate-900">777</span>
                        <div class="flex items-center gap-1 mt-1.5">
                            <span id="plate-code-text" class="text-[9px] font-black tracking-widest text-slate-800">RUS</span>
                            <div id="svg-flag-box" class="w-5 h-3.5 rounded-sm overflow-hidden border border-slate-400 shadow-sm flex items-center justify-center"></div>
                        </div>
                    </div>

                </div>
            </div>

            <div id="info-box" class="text-center my-1 hidden glass-panel p-3.5 rounded-2xl w-full border border-indigo-500/30">
                <p id="res-title" class="text-xs font-extrabold text-indigo-400 uppercase tracking-widest"></p>
                <p class="text-xs text-slate-300 mt-1">ЦЕННОСТЬ: <span id="res-val" class="text-emerald-400 font-black text-sm">0</span> ₽</p>
            </div>

            <!-- УПРАВЛЕНИЕ -->
            <div class="w-full space-y-3.5 mt-auto pt-2">
                <div>
                    <label class="block text-[10px] text-slate-400 mb-1 font-bold">ТИП КОНТЕЙНЕРА:</label>
                    <select id="spin-tier-select" class="w-full rounded-2xl p-3.5 text-xs font-bold text-amber-400 focus:outline-none">
                        <option value="normal">📦 Обычный слот — 1 000 ₽</option>
                        <option value="legendary">⚡ Легендарный слот — 15 000 ₽</option>
                    </select>
                </div>

                <div class="flex gap-2">
                    <select id="country-select" onchange="onCountryChange()" class="rounded-2xl p-3.5 text-xs font-bold text-white focus:outline-none flex-1">
                        <option value="ru">🇷🇺 Россия</option>
                        <option value="ua">🇺🇦 Украина</option>
                        <option value="by">🇧🇾 Беларусь</option>
                    </select>

                    <select id="region-select" class="rounded-2xl p-3.5 text-xs font-bold text-white focus:outline-none flex-1">
                    </select>
                </div>

                <button onclick="spin()" class="w-full gold-btn text-slate-950 font-black py-4 rounded-2xl transition flex items-center justify-center gap-2">
                    <span>🚀 КРУТИТЬ СЛОТ (1 000 ₽)</span>
                </button>
            </div>
        </div>

        <!-- ГАРАЖ -->
        <div id="view-garage" class="p-4 hidden flex-col max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('slots')" class="text-xs text-indigo-400 font-bold mb-2">← Назад к слотам</button>
            <h2 class="text-sm font-extrabold text-white">Ваш личный гараж (Облако)</h2>
            <div id="garage-list" class="space-y-3"></div>
        </div>

        <!-- БИРЖА ИГРОКОВ -->
        <div id="view-market" class="p-4 hidden flex-col max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('slots')" class="text-xs text-indigo-400 font-bold mb-2">← Назад к слотам</button>
            <h2 class="text-sm font-extrabold text-white">📈 Живая биржа игроков</h2>
            <div id="market-list" class="space-y-3"></div>
        </div>

        <!-- МОДАЛКА ВЫСТАВЛЕНИЯ НА БИРЖУ С КАСТОМНОЙ ЦЕНОЙ -->
        <div id="sell-modal" class="hidden fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center p-4">
            <div class="glass-panel p-6 rounded-3xl max-w-sm w-full space-y-4 text-center border border-amber-500/50">
                <h3 class="text-base font-black text-amber-400">ПРОДАЖА НА БИРЖЕ</h3>
                <p class="text-xs text-slate-300">Укажите вашу личную цену в рублях для продажи этого номера:</p>
                <div id="modal-sell-plate-name" class="font-plate text-lg font-black text-white"></div>
                
                <input id="custom-price-input" type="number" placeholder="Цена в ₽" class="w-full rounded-2xl p-3.5 text-center text-emerald-400 font-extrabold text-sm focus:outline-none">
                
                <div class="flex gap-3 pt-2">
                    <button onclick="confirmMarketSell()" class="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold py-3.5 rounded-2xl text-xs">Выставить</button>
                    <button onclick="closeSellModal()" class="flex-1 bg-slate-800 hover:bg-slate-700 text-white font-extrabold py-3.5 rounded-2xl text-xs">Отмена</button>
                </div>
            </div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            let userId = tg.initDataUnsafe?.user?.id || 7271568260;
            let currentData = { profile: {}, garage: [], market: [] };
            let selectedPlateForMarket = null;

            const RU_REGIONS = ['77', '99', '177', '199', '777', '799', '78', '98', '178', '198', '50', '90', '150', '161', '125', '23', '93', '123', '16', '116', '716', '02', '102', '25', '63', '66', '36', '52', '61', '34', '54'];
            const UA_OBLASTS = ['AA', 'KA', 'AM', 'AO', 'AP', 'AT', 'AI', 'BA', 'BB', 'BC', 'HC', 'BE', 'BH', 'BI', 'BK', 'BM', 'BO', 'AX', 'KX', 'BT', 'BX', 'CA', 'CB', 'CE', 'AE', 'KE', 'AH', 'KH', 'AB', 'AC'];
            const BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7'];

            function showToast(msg, icon = "⚡") {
                let toast = document.getElementById('toast');
                document.getElementById('toast-msg').innerText = msg;
                document.getElementById('toast-icon').innerText = icon;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 3200);
            }

            async function loadUserData() {
                let res = await fetch(`/api/user/data?user_id=${userId}`);
                if (res.ok) {
                    currentData = await res.json();
                    document.getElementById('balance').innerText = currentData.profile.balance.toLocaleString('ru-RU') + ' ₽';
                    document.getElementById('level').innerText = currentData.profile.level;
                    renderGarage();
                    renderMarket();
                }
            }

            function showView(viewName) {
                ['slots', 'garage', 'market'].forEach(v => {
                    let el = document.getElementById(`view-${v}`);
                    if (el) el.classList.add('hidden');
                });
                document.getElementById(`view-${viewName}`).classList.remove('hidden');
                loadUserData();
            }

            function updatePlateVisual(country, numberText, regionText, colorClass) {
                let plateBox = document.getElementById('plate-box');
                let codeText = document.getElementById('plate-code-text');
                let svgBox = document.getElementById('svg-flag-box');
                let regionBlock = document.getElementById('region-block');
                let uaBadge = document.getElementById('ua-badge');

                plateBox.className = `relative bg-white text-black border-4 rounded-2xl shadow-2xl w-full max-w-[340px] h-32 flex items-center justify-between px-3.5 overflow-hidden transition-all duration-300 glow-${colorClass}`;
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
                let country = document.getElementById('country-select').value;
                let region = document.getElementById('region-select').value;
                let tier = document.getElementById('spin-tier-select').value;

                let res = await fetch(`/api/spin?user_id=${userId}&country=${country}&region=${region}&tier=${tier}`);
                if (res.ok) {
                    let item = await res.json();
                    updatePlateVisual(country, item.number, item.region, item.color);

                    document.getElementById('res-title').innerText = item.title;
                    document.getElementById('res-val').innerText = item.value.toLocaleString('ru-RU');
                    document.getElementById('info-box').classList.remove('hidden');

                    await fetch(`/api/user/save_plate?user_id=${userId}`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(item)
                    });

                    showToast(`Выбили уникальный номер: ${item.number}! Сохранено в гараж.`, "🎉");
                    loadUserData();
                    tg.HapticFeedback?.notificationOccurred('success');
                }
            }

            function renderGarage() {
                let list = document.getElementById('garage-list');
                if (!currentData.garage || currentData.garage.length === 0) {
                    list.innerHTML = '<div class="text-center text-slate-500 py-8 text-xs">Гараж пуст. Начните крутить слоты!</div>';
                    return;
                }
                list.innerHTML = currentData.garage.map((item) => `
                    <div class="glass-panel p-4 rounded-2xl flex justify-between items-center border glow-${item.color}">
                        <div>
                            <span class="text-[10px] font-black uppercase text-indigo-400">${item.title}</span>
                            <div class="font-plate font-black text-white text-base mt-0.5">${item.number_str} ${item.region_str !== "UA" ? "| " + item.region_str : ""}</div>
                            <div class="text-xs text-emerald-400 font-bold">Оценка: ${item.value_amount.toLocaleString('ru-RU')} ₽</div>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="quickSell(${item.id}, ${item.value_amount})" class="bg-emerald-600/20 text-emerald-300 border border-emerald-500/40 px-3 py-1.5 rounded-xl text-xs font-bold">Продать системе</button>
                            <button onclick="openSellModal(${item.id}, '${item.number_str}', '${item.region_str}', ${item.value_amount})" class="cyber-btn text-white px-3 py-1.5 rounded-xl text-xs font-bold">На биржу</button>
                        </div>
                    </div>
                `).join('');
            }

            async function quickSell(plateId, value) {
                let res = await fetch(`/api/user/quick_sell?user_id=${userId}&plate_id=${plateId}&price=${value}`, {method: 'POST'});
                if (res.ok) {
                    showToast(`Продано! Номер снова доступен в мире игры. +${value.toLocaleString('ru-RU')} ₽`, "💰");
                    loadUserData();
                }
            }

            function openSellModal(id, num, reg, val) {
                selectedPlateForMarket = id;
                document.getElementById('modal-sell-plate-name').innerText = `${num} | ${reg}`;
                document.getElementById('custom-price-input').value = Math.round(val * 1.3);
                document.getElementById('sell-modal').classList.remove('hidden');
            }

            function closeSellModal() {
                document.getElementById('sell-modal').classList.add('hidden');
            }

            async function confirmMarketSell() {
                let price = parseInt(document.getElementById('custom-price-input').value) || 1000;
                let res = await fetch(`/api/market/list?plate_id=${selectedPlateForMarket}&custom_price=${price}`, {method: 'POST'});
                if (res.ok) {
                    closeSellModal();
                    showToast(`Лот выставлен на биржу за ${price.toLocaleString('ru-RU')} ₽!`, "📈");
                    loadUserData();
                }
            }

            function renderMarket() {
                let list = document.getElementById('market-list');
                if (!currentData.market || currentData.market.length === 0) {
                    list.innerHTML = '<div class="text-center text-slate-500 py-8 text-xs">На бирже пока нет лотов от игроков.</div>';
                    return;
                }
                list.innerHTML = currentData.market.map((item) => `
                    <div class="glass-panel p-4 rounded-2xl flex justify-between items-center border border-slate-800">
                        <div>
                            <span class="text-[10px] text-slate-400 font-bold">${item.title}</span>
                            <div class="font-plate font-black text-amber-400 text-base mt-0.5">${item.number_str} ${item.region_str !== "UA" ? "| " + item.region_str : ""}</div>
                            <div class="text-emerald-400 font-black text-xs mt-1">${item.market_price.toLocaleString('ru-RU')} ₽</div>
                        </div>
                        <div>
                            ${item.owner_id !== userId 
                                ? `<button onclick="buyMarketItem(${item.id})" class="cyber-btn text-white px-3.5 py-2 rounded-xl text-xs font-bold">Купить</button>`
                                : `<span class="text-[10px] text-slate-500 font-bold">Ваш лот</span>`
                            }
                        </div>
                    </div>
                `).join('');
            }

            async function buyMarketItem(plateId) {
                let res = await fetch(`/api/market/buy?buyer_id=${userId}&plate_id=${plateId}`, {method: 'POST'});
                if (res.ok) {
                    let result = await res.json();
                    showToast(result.message, result.success ? "🎉" : "❌");
                    loadUserData();
                }
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
                updatePlateVisual(country, country === 'ua' ? 'AA 7777 AB' : 'А 777 АА', list[0], 'yellow');
            }

            onCountryChange();
            loadUserData();
        </script>
    </body>
    </html>
    """
    return html_content.replace("__ADMIN_ID__", str(ADMIN_TG_ID))