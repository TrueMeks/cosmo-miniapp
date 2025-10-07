# Установка пакета: python -m pip install python-telegram-bot==20.6
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8431586699:AAF093GO1N8LU46V_pc1iJLIie1neYvlAWc"
ADMIN_CHAT_ID = 828210450  # временно None, узнаем ниже и подставим число

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    # При первом заходе бот пришлёт твой chat_id, скопируй его в ADMIN_CHAT_ID
    await update.message.reply_text(f"Привет! Твой chat_id: {cid}")
    print("Ваш ADMIN_CHAT_ID:", cid)

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Если пришли данные из мини-приложения
    if update.message and update.message.web_app_data:
        raw = update.message.web_app_data.data
        try:
            payload = json.loads(raw)  # ожидаем {"type":"booking","data":{...}}
            booking = payload.get("data", payload)
        except Exception:
            booking = {"raw": raw}

        text = (
            "🧾 <b>Новая запись</b>\n"
            f"👤 Имя: {booking.get('name','')}\n"
            f"📞 Телефон: {booking.get('phone','')}\n"
            f"💆 Услуга: {booking.get('service','')}\n"
            f"📅 Дата: {booking.get('date','')}  ⏰ {booking.get('time','')}\n"
            f"📝 Комментарий: {booking.get('note','')}"
        )

        # Отправляем админу (тебе)
        if ADMIN_CHAT_ID:
            try:
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode="HTML")
            except Exception as e:
                print("Ошибка при отправке админу:", e)

        # Ответ клиенту
        await update.message.reply_text("Спасибо! Заявка отправлена ✅")
    else:
        # Ответ на любые другие сообщения
        if update.message and update.message.text:
            await update.message.reply_text("Напиши /start или открой «Запись» в меню бота 🙂")

# Доп. команда для быстрой проверки доставки
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_CHAT_ID:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="Тестовое уведомление ✅")
    else:
        await update.message.reply_text("Сначала получи chat_id через /start и подставь в код.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("test", test))
app.add_handler(MessageHandler(filters.ALL, handle_all))
app.run_polling()
