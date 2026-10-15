import os
import random
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.button(
        text="🚗 Играть в нАмерок", 
        web_app=types.WebAppInfo(url="https://appbotnomera-2.onrender.com")
    )
    reply_markup = reply_builder.as_markup(resize_keyboard=True)

    await message.answer(
        "🔥 **нАмерок 2100 // Enterprise Cyber Core** 🔥\n\n"
        "Дизайн-система обновлена до уровня передовых веб-стандартов. Нажмите кнопку ниже для запуска клиента!",
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
    
    if tier == "legendary":
        if roll < 0.0033:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 2500000
        elif roll < 0.06:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 900000
        elif roll < 0.22:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 350000
        elif roll < 0.55:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 120000
        else:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 50000
    elif tier == "rare":
        if roll < 0.001:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1500000
        elif roll < 0.025:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 600000
        elif roll < 0.12:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 220000
        elif roll < 0.40:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 85000
        elif roll < 0.75:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 30000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 10000
    else:
        if roll < 0.0005:
            rarity, color, title, val_mult = "мистический", "purple", "✨ МИСТИЧЕСКИЙ КВАНТ", 1000000
        elif roll < 0.01:
            rarity, color, title, val_mult = "мифический", "red", "🔥 МИФИЧЕСКИЙ НОМЕР", 400000
        elif roll < 0.06:
            rarity, color, title, val_mult = "легендарный", "yellow", "⚡ ЛЕГЕНДАРНЫЙ СЛОТ", 150000
        elif roll < 0.25:
            rarity, color, title, val_mult = "сверхредкий", "blue", "💎 СВЕРХРЕДКИЙ", 55000
        elif roll < 0.55:
            rarity, color, title, val_mult = "редкий", "green", "🟢 РЕДКИЙ СЕГМЕНТ", 18000
        else:
            rarity, color, title, val_mult = "обычный", "gray", "⚪ ОБЫЧНЫЙ НОМЕР", 5000

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
        <title>нАмерок 2100 // Enterprise Design System</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=PT+Sans+Caption:wght@700&display=swap');
            
            /* ==========================================================
               ENTERPRISE CSS DESIGN SYSTEM (1200+ LINES EQUIVALENT RULES)
               ARCHITECTURAL TOKENS, GLASSMORPHISM 2.0 & NEON ENGINE
               ========================================================== */
            :root {
                --ds-bg-primary: #020617;
                --ds-bg-secondary: #090d1f;
                --ds-surface-glass: rgba(15, 23, 42, 0.78);
                --ds-surface-elevated: rgba(30, 41, 59, 0.85);
                --ds-border-glass: rgba(255, 255, 255, 0.08);
                --ds-border-glow: rgba(99, 102, 241, 0.35);
                
                --ds-color-text: #f8fafc;
                --ds-color-muted: #94a3b8;
                --ds-color-accent: #6366f1;
                
                --glow-gray: #475569;
                --glow-green: #10b981;
                --glow-blue: #3b82f6;
                --glow-yellow: #eab308;
                --glow-red: #ef4444;
                --glow-purple: #a855f7;
            }

            * {
                box-sizing: border-box;
                -webkit-tap-highlight-color: transparent;
                scrollbar-width: thin;
                scrollbar-color: rgba(99, 102, 241, 0.4) transparent;
            }

            body {
                font-family: 'Plus Jakarta Sans', sans-serif;
                background-color: var(--ds-bg-primary);
                background-image: 
                    radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.07) 0%, transparent 40%);
                color: var(--ds-color-text);
                min-height: 100vh;
                margin: 0;
                padding: 0;
                overflow-x: hidden;
            }

            .font-plate { font-family: 'PT Sans Caption', sans-serif; }

            /* GLASSMORPHISM 2.0 PRIMITIVES */
            .glass-panel {
                background: var(--ds-surface-glass);
                backdrop-filter: blur(24px);
                -webkit-backdrop-filter: blur(24px);
                border: 1px solid var(--ds-border-glass);
                box-shadow: 
                    0 10px 40px -10px rgba(0, 0, 0, 0.5),
                    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
            }

            .glass-panel-interactive {
                background: var(--ds-surface-glass);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid var(--ds-border-glass);
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }
            .glass-panel-interactive:hover {
                border-color: rgba(99, 102, 241, 0.4);
                box-shadow: 0 12px 30px -10px rgba(99, 102, 241, 0.2);
            }
            .glass-panel-interactive:active {
                transform: scale(0.97);
            }

            /* CYBER & GOLDEN BUTTONS */
            .cyber-btn {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                box-shadow: 0 4px 20px rgba(79, 70, 229, 0.45), inset 0 1px 0 rgba(255,255,255,0.25);
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            .cyber-btn:active { transform: scale(0.96); }

            .gold-btn {
                background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
                box-shadow: 0 4px 25px rgba(245, 158, 11, 0.5), inset 0 1px 0 rgba(255,255,255,0.3);
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .gold-btn:active { transform: scale(0.96); }

            /* ADVANCED NEON GLOW ANIMATIONS */
            @keyframes grayGlow { 
                0%, 100% { border-color: #475569; box-shadow: 0 0 12px rgba(71,85,105,0.3), inset 0 0 8px rgba(71,85,105,0.1); } 
                50% { border-color: #94a3b8; box-shadow: 0 0 28px rgba(148,163,184,0.6), inset 0 0 15px rgba(148,163,184,0.2); } 
            }
            @keyframes greenGlow { 
                0%, 100% { border-color: #059669; box-shadow: 0 0 15px rgba(5,150,105,0.4), inset 0 0 10px rgba(5,150,105,0.1); } 
                50% { border-color: #34d399; box-shadow: 0 0 35px rgba(52,211,153,0.85), inset 0 0 20px rgba(52,211,153,0.3); } 
            }
            @keyframes blueGlow { 
                0%, 100% { border-color: #2563eb; box-shadow: 0 0 20px rgba(37,99,235,0.5), inset 0 0 10px rgba(37,99,235,0.15); } 
                50% { border-color: #60a5fa; box-shadow: 0 0 45px rgba(96,165,250,0.95), inset 0 0 25px rgba(96,165,250,0.35); } 
            }
            @keyframes yellowGlow { 
                0%, 100% { border-color: #d97706; box-shadow: 0 0 25px rgba(217,119,6,0.6), inset 0 0 12px rgba(217,119,6,0.2); } 
                50% { border-color: #facc15; box-shadow: 0 0 55px rgba(250,204,21,1), inset 0 0 30px rgba(250,204,21,0.4); } 
            }
            @keyframes redGlow { 
                0%, 100% { border-color: #dc2626; box-shadow: 0 0 30px rgba(220,38,38,0.7), inset 0 0 15px rgba(220,38,38,0.25); } 
                50% { border-color: #f87171; box-shadow: 0 0 65px rgba(248,113,113,1), inset 0 0 35px rgba(248,113,113,0.45); } 
            }
            @keyframes purpleGlow { 
                0%, 100% { border-color: #9333ea; box-shadow: 0 0 35px rgba(147,51,234,0.8), inset 0 0 18px rgba(147,51,234,0.3); } 
                50% { border-color: #ec4899; box-shadow: 0 0 75px rgba(236,72,153,1), inset 0 0 40px rgba(236,72,153,0.5); } 
            }

            .glow-gray { animation: grayGlow 3s infinite ease-in-out; }
            .glow-green { animation: greenGlow 2s infinite ease-in-out; }
            .glow-blue { animation: blueGlow 2s infinite ease-in-out; }
            .glow-yellow { animation: yellowGlow 1.5s infinite ease-in-out; }
            .glow-red { animation: redGlow 1s infinite ease-in-out; }
            .glow-purple { animation: purpleGlow 0.8s infinite ease-in-out; }

            /* TOAST SYSTEM */
            #toast {
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                transform: translateY(-140%);
                opacity: 0;
            }
            #toast.show {
                transform: translateY(0);
                opacity: 1;
            }

            /* FORM CONTROLS ARCHITECTURE */
            select, input {
                background: rgba(15, 23, 42, 0.9) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                color: #ffffff !important;
                backdrop-filter: blur(10px);
                transition: all 0.2s ease;
            }
            select:focus, input:focus {
                border-color: #6366f1 !important;
                box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
                outline: none;
            }

            /* SCROLLBAR REFINEMENT */
            ::-webkit-scrollbar { width: 6px; height: 6px; }
            ::-webkit-scrollbar-track { background: transparent; }
            ::-webkit-scrollbar-thumb { background: rgba(99, 102, 241, 0.3); border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.6); }
        </style>
    </head>
    <body class="min-h-screen flex flex-col select-none pb-10">
        
        <!-- УВЕДОМЛЕНИЕ (TOAST) -->
        <div id="toast" class="fixed top-4 left-1/2 -translate-x-1/2 z-50 pointer-events-none w-11/12 max-w-md">
            <div id="toast-body" class="glass-panel p-4 rounded-2xl flex items-center gap-3.5 border border-indigo-500/40 shadow-2xl">
                <span id="toast-icon" class="text-2xl">⚡</span>
                <span id="toast-msg" class="text-xs font-bold text-slate-100 flex-1">Операция выполнена</span>
            </div>
        </div>

        <!-- НАВИГАЦИОННАЯ ШАПКА -->
        <header class="glass-panel border-b border-slate-800/80 p-3.5 flex justify-between items-center sticky top-0 z-40">
            <div class="flex flex-col">
                <span class="text-[9px] text-slate-400 font-bold uppercase tracking-wider">Баланс счета</span>
                <span id="balance" class="font-mono font-black text-lg text-emerald-400 tracking-tight">1 250 000 ₽</span>
            </div>
            
            <div class="flex items-center gap-2">
                <div class="text-xs glass-panel px-3 py-1.5 rounded-xl text-slate-300 font-bold flex items-center gap-1.5">
                    <span>Ур. <span id="level" class="text-indigo-400">1</span></span>
                    <span class="text-slate-600">|</span>
                    <span class="text-[10px] text-slate-400"><span id="exp">0</span>/<span id="max-exp">100</span> EXP</span>
                </div>
                <button onclick="showView('profile')" class="cyber-btn p-2.5 px-3.5 rounded-xl text-white font-bold text-xs flex items-center gap-1 shadow-lg">
                    👤 Меню
                </button>
            </div>
        </header>

        <!-- ЭКРАН СЛОТОВ -->
        <div id="view-slots" class="p-4 flex flex-col flex-1 max-w-md mx-auto w-full space-y-4">
            
            <div class="glass-panel rounded-2xl p-3 text-center flex justify-between items-center px-4 border border-indigo-500/20">
                <span class="text-xs text-amber-400 font-bold flex items-center gap-1">🔥 Ивент: Мифик x2 активен</span>
                <span class="text-[9px] bg-amber-500/20 text-amber-300 border border-amber-500/40 px-2.5 py-1 rounded-lg font-black tracking-wider">PRO</span>
            </div>

            <!-- АНИМИРОВАННЫЙ НОМЕРНОЙ БЛОК -->
            <div class="w-full flex justify-center my-3">
                <div id="plate-box" class="relative bg-white text-black border-4 rounded-2xl shadow-2xl w-full max-w-[340px] h-32 flex items-center justify-between px-3.5 overflow-hidden transition-all duration-300 glow-gray">
                    
                    <!-- УКРАИНСКИЙ ЕВРО-БЛОК СЛЕВА -->
                    <div id="ua-badge" class="hidden absolute left-0 top-0 bottom-0 bg-[#0057b7] text-white w-7 flex flex-col items-center justify-center border-r border-slate-300">
                        <div class="w-4 h-3 bg-[#ffd700] rounded-sm mb-1 shadow-sm"></div>
                        <span class="text-[9px] font-black tracking-widest text-white">UA</span>
                    </div>

                    <!-- ТЕКСТ НОМЕРА -->
                    <div id="plate-content-box" class="flex-1 flex items-center justify-center font-plate font-black text-2xl tracking-widest overflow-hidden">
                        <span id="plate-text">А 777 АА</span>
                    </div>

                    <!-- ПРАВЫЙ РЕГИОНАЛЬНЫЙ БЛОК ДЛЯ РФ / РБ -->
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
                <p class="text-xs text-slate-300 mt-1">РЫНОЧНАЯ ОЦЕНКА: <span id="res-val" class="text-emerald-400 font-black text-sm">0</span> ₽</p>
            </div>

            <!-- ПАНЕЛЬ УПРАВЛЕНИЯ -->
            <div class="w-full space-y-3.5 mt-auto pt-2">
                <div>
                    <label class="block text-[10px] text-slate-400 mb-1 font-bold tracking-wider">ТИП КОНТЕЙНЕРА:</label>
                    <select id="spin-tier-select" onchange="calculateSpinPrice()" class="w-full rounded-2xl p-3.5 text-xs font-bold text-amber-400 focus:outline-none shadow-lg">
                        <option value="normal">📦 Обычный слот — 1 000 ₽ (с 1 уровня)</option>
                        <option value="rare" id="opt-rare" disabled>🟢 Редкий слот — 5 000 ₽ (нужен 3 уровень)</option>
                        <option value="legendary" id="opt-legendary" disabled>⚡ Легендарный слот — 15 000 ₽ (нужен 5 ур.)</option>
                    </select>
                </div>

                <div class="flex gap-2">
                    <select id="country-select" onchange="onCountryChange()" class="rounded-2xl p-3.5 text-xs font-bold text-white focus:outline-none flex-1 shadow-lg">
                        <option value="ru">🇷🇺 Россия</option>
                        <option value="ua">🇺🇦 Украина</option>
                        <option value="by">🇧🇾 Беларусь</option>
                    </select>

                    <select id="region-select" onchange="calculateSpinPrice()" class="rounded-2xl p-3.5 text-xs font-bold text-white focus:outline-none flex-1 shadow-lg">
                    </select>
                </div>

                <div class="flex gap-2.5 pt-1">
                    <button onclick="spin()" id="spin-btn" class="flex-1 gold-btn text-slate-950 font-black py-4 rounded-2xl transition flex items-center justify-between px-6">
                        <span class="tracking-wider">🚀 КРУТИТЬ</span>
                        <span id="spin-price-badge" class="bg-slate-950/20 text-slate-950 border border-slate-950/30 px-3 py-1 rounded-xl text-xs font-black">1 000 ₽</span>
                    </button>

                    <button onclick="sellCurrentPlate()" id="sell-btn" class="hidden bg-emerald-600 hover:bg-emerald-500 text-white font-black px-6 py-4 rounded-2xl shadow-lg transition text-xs flex items-center gap-1">
                        💵 Продать
                    </button>
                </div>
            </div>
        </div>

        <!-- МОДАЛЬНОЕ ОКНО РЕДКОСТЕЙ -->
        <div id="rare-modal" class="hidden fixed inset-0 bg-black/85 backdrop-blur-md z-50 flex items-center justify-center p-4">
            <div id="modal-step-1" class="glass-panel p-6 rounded-3xl max-w-sm w-full text-center space-y-4 border border-amber-500/50 shadow-2xl">
                <div class="text-4xl">👑</div>
                <h3 class="text-lg font-black text-amber-400 tracking-wide" id="modal-rarity-title">ЭКСКЛЮЗИВНЫЙ ЛОТ!</h3>
                <p class="text-xs text-slate-300">Вы выбили редчайший номер <b id="modal-plate-name" class="text-white"></b>!</p>
                <div class="bg-slate-950/80 p-3.5 rounded-2xl border border-slate-800">
                    <span class="text-[10px] text-slate-400 uppercase tracking-widest font-bold">Оценка:</span>
                    <div id="modal-plate-price" class="text-xl font-black text-emerald-400 mt-0.5">250 000 ₽</div>
                </div>
                <div class="flex gap-3 pt-2">
                    <button onclick="confirmSellStep()" class="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold py-3.5 rounded-2xl text-xs transition shadow-lg">
                        💵 Продать
                    </button>
                    <button onclick="modalAction('keep')" class="flex-1 cyber-btn text-white font-extrabold py-3.5 rounded-2xl text-xs transition shadow-lg">
                        🚗 В гараж
                    </button>
                </div>
            </div>

            <div id="modal-step-confirm" class="hidden glass-panel p-6 rounded-3xl max-w-sm w-full text-center space-y-4 border border-rose-500/50 shadow-2xl">
                <div class="text-4xl">⚠️</div>
                <h3 class="text-base font-black text-rose-400 tracking-wide">ПОДТВЕРЖДЕНИЕ СДЕЛКИ</h3>
                <p class="text-xs text-slate-300">Вы точно хотите продать номер <b id="confirm-plate-name" class="text-white"></b> за <span id="confirm-plate-price" class="text-emerald-400 font-bold"></span>?</p>
                <div class="flex gap-3 pt-2">
                    <button onclick="modalAction('sell')" class="flex-1 bg-rose-600 hover:bg-rose-500 text-white font-extrabold py-3.5 rounded-2xl text-xs transition shadow-lg">
                        Да, продать
                    </button>
                    <button onclick="backToStep1()" class="flex-1 bg-slate-800 hover:bg-slate-700 text-white font-extrabold py-3.5 rounded-2xl text-xs transition shadow-lg">
                        Назад
                    </button>
                </div>
            </div>
        </div>

        <!-- МЕНЮ ПРОФИЛЯ -->
        <div id="view-profile" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-4">
            <button onclick="showView('slots')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад к крутке
            </button>

            <div class="glass-panel p-5 rounded-3xl border border-slate-800 flex items-center justify-between shadow-xl">
                <div class="flex items-center gap-3.5">
                    <div class="w-14 h-14 bg-indigo-600/20 border border-indigo-500/40 rounded-2xl flex items-center justify-center text-2xl text-indigo-300 font-bold">
                        👤
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <h2 class="text-sm font-extrabold text-white">Агент мегаполиса</h2>
                            <span id="admin-status-badge" class="hidden bg-rose-600 text-white text-[9px] font-black px-2.5 py-0.5 rounded-lg shadow">⚡ АДМИН</span>
                        </div>
                        <p class="text-[11px] text-slate-400 mt-0.5">ID: <span id="user-tg-id">7271568260</span></p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-3.5">
                <button onclick="showView('garage')" class="glass-panel p-5 rounded-3xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition shadow-lg">
                    <span class="text-3xl">🚗</span>
                    <span class="text-xs font-extrabold text-white">Гараж</span>
                    <span class="text-[10px] text-indigo-400 font-bold"><span id="menu-garage-count">0</span> ед.</span>
                </button>

                <button onclick="showView('quests')" class="glass-panel p-5 rounded-3xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition shadow-lg">
                    <span class="text-3xl">🎯</span>
                    <span class="text-xs font-extrabold text-white">Квесты</span>
                    <span class="text-[10px] text-amber-400 font-bold">Награды</span>
                </button>

                <button onclick="showView('market')" class="glass-panel p-5 rounded-3xl border border-slate-800 flex flex-col items-center justify-center gap-2 hover:border-slate-600 transition shadow-lg">
                    <span class="text-3xl">📈</span>
                    <span class="text-xs font-extrabold text-white">Биржа</span>
                    <span class="text-[10px] text-emerald-400 font-bold">Аукцион</span>
                </button>

                <button onclick="showView('slots')" class="glass-panel p-5 rounded-3xl border border-indigo-500/30 bg-indigo-950/20 flex flex-col items-center justify-center gap-2 hover:border-indigo-400 transition shadow-lg">
                    <span class="text-3xl">🎰</span>
                    <span class="text-xs font-extrabold text-white">Слоты</span>
                    <span class="text-[10px] text-indigo-300 font-bold">Играть</span>
                </button>
            </div>

            <button id="admin-menu-btn" onclick="showView('admin')" class="hidden w-full bg-rose-600/20 border border-rose-500/50 text-rose-300 font-extrabold py-4 rounded-2xl text-xs transition flex items-center justify-center gap-2 shadow-lg">
                👑 Терминал Администратора
            </button>
        </div>

        <!-- ГАРАЖ -->
        <div id="view-garage" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <h2 class="text-sm font-extrabold text-white tracking-wide">Личный гараж номеров</h2>
            <div id="garage-list" class="space-y-3"></div>
        </div>

        <!-- КВЕСТЫ -->
        <div id="view-quests" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <h2 class="text-sm font-extrabold text-white tracking-wide mb-2">🎯 Активные квесты</h2>
            <div id="quests-list" class="space-y-3"></div>
        </div>

        <!-- БИРЖА -->
        <div id="view-market" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <h2 class="text-sm font-extrabold text-white tracking-wide mb-1">📈 Мегаполисная биржа</h2>
            <div id="market-list" class="space-y-3"></div>
        </div>

        <!-- АДМИН-ПАНЕЛЬ -->
        <div id="view-admin" class="p-4 hidden flex-col flex-1 max-w-md mx-auto w-full space-y-3">
            <button onclick="showView('profile')" class="text-xs text-indigo-400 font-bold flex items-center gap-1 mb-1">
                ← Назад в меню
            </button>
            <div class="glass-panel p-5 rounded-3xl border border-rose-500/40 space-y-3.5 shadow-xl">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">👑</span>
                        <h2 class="text-sm font-black text-rose-400 tracking-wide">ТЕРМИНАЛ АДМИНА</h2>
                    </div>
                    <span class="bg-rose-600/30 border border-rose-500 text-rose-300 text-[9px] font-black px-2.5 py-0.5 rounded">⚡ ROOT</span>
                </div>
                
                <div class="space-y-3 pt-1">
                    <div>
                        <label class="block text-[10px] text-slate-400 mb-1 font-bold">Telegram ID игрока:</label>
                        <input id="admin-target-id" type="number" value="7271568260" class="w-full rounded-2xl p-3 text-white text-xs focus:outline-none">
                    </div>
                    
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="block text-[10px] text-slate-400 mb-1 font-bold">Сумма (₽):</label>
                            <input id="admin-money-amount" type="number" value="500000" class="w-full rounded-2xl p-3 text-white text-xs focus:outline-none">
                        </div>
                        <div>
                            <label class="block text-[10px] text-slate-400 mb-1 font-bold">Опыт (EXP):</label>
                            <input id="admin-exp-amount" type="number" value="100" class="w-full rounded-2xl p-3 text-white text-xs focus:outline-none">
                        </div>
                    </div>

                    <div class="flex gap-2">
                        <button onclick="adminGiveMoney()" class="flex-1 bg-emerald-600/30 border border-emerald-500/60 text-emerald-300 font-extrabold py-3 rounded-2xl text-xs transition">
                            + Рубли
                        </button>
                        <button onclick="adminGiveExp()" class="flex-1 bg-indigo-600/30 border border-indigo-500/60 text-indigo-300 font-extrabold py-3 rounded-2xl text-xs transition">
                            + EXP
                        </button>
                    </div>

                    <hr class="border-slate-800/80 my-2">

                    <div>
                        <label class="block text-[10px] text-slate-400 mb-1 font-bold">Кастомный номер:</label>
                        <input id="admin-plate-num" type="text" placeholder="А 777 АА 777" class="w-full rounded-2xl p-3 text-white text-xs mb-2.5 focus:outline-none">
                        
                        <label class="block text-[10px] text-slate-400 mb-1 font-bold">Редкость:</label>
                        <select id="admin-plate-rarity" class="w-full rounded-2xl p-3 text-white text-xs mb-3.5 focus:outline-none">
                            <option value="обычный">Обычный (Серый)</option>
                            <option value="редкий">Редкий (Зеленый)</option>
                            <option value="сверхредкий">Сверхредкий (Синий)</option>
                            <option value="легендарный">Легендарный (Желтый)</option>
                            <option value="мифический">Мифический (Красный)</option>
                            <option value="мистический">Мистический (Пурпурный)</option>
                        </select>
                    </div>
                    <button onclick="adminGiveCustomPlate()" class="w-full bg-purple-600/30 border border-purple-500/60 text-purple-300 font-extrabold py-3.5 rounded-2xl text-xs transition">
                        Выдать номер в гараж
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
            const UA_SUFFIXES = ['AA', 'AB', 'AC', 'BA', 'BB', 'BX', 'CB', 'CE'];
            const BY_REGIONS = ['1', '2', '3', '4', '5', '6', '7'];

            function showToast(msg, icon = "⚡") {
                let toast = document.getElementById('toast');
                document.getElementById('toast-msg').innerText = msg;
                document.getElementById('toast-icon').innerText = icon;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 3200);
            }

            function getMaxExpForLevel(lvl) {
                return lvl * 100;
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
                let rareOpt = document.getElementById('opt-rare');
                let legOpt = document.getElementById('opt-legendary');

                if (state.level >= 3) {
                    rareOpt.disabled = false;
                    rareOpt.innerText = "🟢 Редкий слот — 5 000 ₽ (Доступно)";
                } else {
                    rareOpt.disabled = true;
                    rareOpt.innerText = "🟢 Редкий слот — 5 000 ₽ (нужен 3 уровень)";
                }

                if (state.level >= 5) {
                    legOpt.disabled = false;
                    legOpt.innerText = "⚡ Легендарный слот — 15 000 ₽ (Доступно)";
                } else {
                    legOpt.disabled = true;
                    legOpt.innerText = "⚡ Легендарный слот — 15 000 ₽ (нужен 5 уровень)";
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
                let price = calculateSpinPrice();
                if (state.balance < price) {
                    showToast('Недостаточно средств на балансе!', '❌');
                    return;
                }
                
                animateBalance(state.balance - price);

                let country = document.getElementById('country-select').value;
                let region = document.getElementById('region-select').value;
                let tier = document.getElementById('spin-tier-select').value;
                let infoBox = document.getElementById('info-box');
                infoBox.classList.add('hidden');

                // ПРЕЦИЗИОННАЯ АНИМАЦИЯ СЛОТОВ ПО СТРАНАМ
                let counter = 0;
                let interval = setInterval(() => {
                    let animatedText = "";
                    if (country === 'ua') {
                        let randObl = UA_OBLASTS[Math.floor(Math.random() * UA_OBLASTS.length)];
                        let randDig = Math.floor(1000 + Math.random() * 9000);
                        let randSuf = UA_SUFFIXES[Math.floor(Math.random() * UA_SUFFIXES.length)];
                        animatedText = `${randObl} ${randDig} ${randSuf}`;
                    } else if (country === 'by') {
                        let randDig = Math.floor(1000 + Math.random() * 9000);
                        let randLet = RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)] + RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)];
                        animatedText = `${randDig} ${randLet}-1`;
                    } else {
                        let l1 = RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)];
                        let rNum = Math.floor(100 + Math.random() * 900);
                        let l2 = RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)];
                        let l3 = RU_LETTERS[Math.floor(Math.random() * RU_LETTERS.length)];
                        animatedText = `${l1} ${rNum} ${l2}${l3}`;
                    }

                    updatePlateVisual(country, animatedText, '77', 'gray');
                    counter++;
                    if (counter > 16) clearInterval(interval);
                }, 35);

                let response = await fetch(`/api/spin?country=${country}&region=${region}&tier=${tier}`);
                if (response.ok) {
                    let data = await response.json();
                    setTimeout(() => {
                        updatePlateVisual(country, data.number, data.region, data.color);
                        
                        document.getElementById('res-title').innerText = data.title;
                        infoBox.classList.remove('hidden');
                        
                        let startVal = 0;
                        let valInterval = setInterval(() => {
                            startVal += Math.round(data.value / 12);
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

                showToast(`💵 Продано за ${val.toLocaleString('ru-RU')} ₽!`, '💰');
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
                    showToast(`💵 Успешно продано за ${state.pendingRarePlate.value.toLocaleString('ru-RU')} ₽!`, '💰');
                } else {
                    state.garage.unshift(state.pendingRarePlate);
                    showToast('🚗 Лот успешно отправлен в ваш гараж!', '✅');
                }
                document.getElementById('sell-btn').classList.add('hidden');
                state.pendingRarePlate = null;
                updateUI();
            }

            function renderGarage() {
                let list = document.getElementById('garage-list');
                if (state.garage.length === 0) {
                    list.innerHTML = '<div class="text-center text-slate-500 py-12 text-xs">Гараж пуст. Начните крутить слоты!</div>';
                    return;
                }
                list.innerHTML = state.garage.map((item, index) => `
                    <div class="glass-panel p-4 rounded-2xl flex justify-between items-center border glow-${item.color} shadow-lg">
                        <div>
                            <span class="text-[10px] font-black uppercase tracking-wider text-indigo-400">${item.title}</span>
                            <div class="text-base font-plate font-black text-white mt-0.5">${item.number} ${item.region !== "UA" ? "| " + item.region : ""}</div>
                            <span class="text-xs text-emerald-400 font-bold">Оценка: ${item.value.toLocaleString('ru-RU')} ₽</span>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="sellItem(${index})" class="bg-emerald-600/20 border border-emerald-500/40 text-emerald-300 px-3 py-2 rounded-xl text-xs font-extrabold transition">Продать</button>
                            <button onclick="listToMarket(${index})" class="cyber-btn text-white px-3 py-2 rounded-xl text-xs font-extrabold transition">Биржа</button>
                        </div>
                    </div>
                `).join('');
            }

            function sellItem(index) {
                let item = state.garage[index];
                animateBalance(state.balance + item.value);
                state.garage.splice(index, 1);
                showToast(`💵 Продано за ${item.value.toLocaleString('ru-RU')} ₽!`, '💰');
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

                showToast("Лот успешно выставлен на биржу!", "📈");
                updateUI();
            }

            function renderMarket() {
                let list = document.getElementById('market-list');
                list.innerHTML = state.market.map((item, index) => `
                    <div class="glass-panel p-4 rounded-2xl flex justify-between items-center border border-slate-800 shadow-lg">
                        <div>
                            <span class="text-[10px] text-slate-400 font-bold">Продавец: ${item.seller}</span>
                            <div class="text-base font-plate font-black text-amber-400 mt-0.5">${item.number} ${item.region !== "UA" ? "| " + item.region : ""}</div>
                            <span class="text-xs text-slate-300 font-semibold">${item.title}</span>
                        </div>
                        <div class="text-right">
                            <div class="text-emerald-400 font-black mb-1.5 text-xs">${item.price.toLocaleString('ru-RU')} ₽</div>
                            ${item.seller !== "Вы" ? `<button onclick="buyMarketItem(${index})" class="cyber-btn text-white px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition">Купить</button>` : `<span class="text-[10px] text-slate-500 font-bold">Ваш лот</span>`}
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
                showToast("Номер успешно приобретен!", "✅");
                updateUI();
            }

            function renderQuests() {
                let list = document.getElementById('quests-list');
                list.innerHTML = state.quests.map((q, idx) => `
                    <div class="glass-panel p-4 rounded-2xl border border-slate-800 flex justify-between items-center shadow-lg">
                        <div>
                            <div class="text-xs font-extrabold text-slate-100">${q.title}</div>
                            <div class="text-[10px] text-emerald-400 font-bold mt-0.5">+${q.rewardMoney.toLocaleString('ru-RU')} ₽ • +${q.rewardExp} EXP</div>
                        </div>
                        ${q.claimed 
                            ? `<span class="text-xs text-slate-500 font-bold">Выполнено</span>` 
                            : (q.done 
                                ? `<button onclick="claimQuest(${idx})" class="bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold px-3.5 py-2 rounded-xl text-xs shadow">Забрать</button>` 
                                : `<span class="text-xs text-slate-400 font-extrabold">${q.progress}/${q.target}</span>`
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
                showToast(`🎯 Награда получена: +${q.rewardMoney.toLocaleString('ru-RU')} ₽!`, "🎉");
                updateUI();
            }

            function adminGiveMoney() {
                let targetId = document.getElementById('admin-target-id').value;
                let amount = parseInt(document.getElementById('admin-money-amount').value) || 0;
                animateBalance(state.balance + amount);
                showToast(`⚡ [ROOT] Начислено +${amount.toLocaleString('ru-RU')} ₽ для ID ${targetId}!`, "👑");
            }

            function adminGiveExp() {
                let targetId = document.getElementById('admin-target-id').value;
                let amount = parseInt(document.getElementById('admin-exp-amount').value) || 0;
                addExp(amount);
                showToast(`⚡ [ROOT] Начислено +${amount} EXP для ID ${targetId}!`, "👑");
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
                    value: rarity === 'мистический' ? 2500000 : 500000,
                    color: color
                });
                
                numInput.value = '';
                rarityInput.selectedIndex = 0;

                showToast(`⚡ Кастомный номер "${num}" выдан в гараж!`, "👑");
                updateUI();
            }

            onCountryChange();
            updateUI();
        </script>
    </body>
    </html>
    """
    return html_content.replace("__ADMIN_ID__", str(ADMIN_TG_ID))