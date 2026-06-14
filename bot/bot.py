# python bot/bot.py

import random
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#CONFIGURATION
TOKEN = ""
API_URL = "https://kepler-project.onrender.com/planets"

#KEYBOARD LAYOUT
keyboard = [
    [KeyboardButton("📊 API Summary"), KeyboardButton("🟢 Habitable Zone")],
    [KeyboardButton("🎲 Random Planet"), KeyboardButton("📈 Database Stats")],
    [KeyboardButton("ℹ️ Project Info")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user and explains the features."""
    welcome_message = (
        "🚀 **Kepler Mission Control Online**\n\n"
        "Connection to FastAPI backend established. I can provide telemetry on Kepler Objects of Interest (KOI).\n\n"
        "👇 Use the menu buttons below, or **just type a planet's name** (e.g., K00752.01) to search the database directly!"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

#MESSAGE HANDLER
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # BUTTON 1: API Summary
    if text == "📊 API Summary":
        res = requests.get(API_URL, params={"limit": 5})
        if res.status_code == 200:
            data = res.json()
            msg = "📡 **Latest Mainframe Records:**\n\n"
            for p in data:
                msg += f"🪐 {p['kepoi_name']} | {p['koi_disposition']} | R: {p['koi_prad']} R⊕\n"
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ API Connection Error. Is FastAPI running?")

    # BUTTON 2: Habitable Zone
    elif text == "🟢 Habitable Zone":
        res = requests.get(API_URL, params={"status": "CONFIRMED", "limit": 200})
        if res.status_code == 200:
            data = res.json()
            habitable = [p for p in data if p.get('habitable_zone')]
            
            if habitable:
                msg = "🌍 **Top Habitable Zone Candidates (200K - 320K):**\n\n"
                for p in habitable[:5]: 
                    msg += f"✅ **{p['kepoi_name']}** (Temp: {p['koi_teq']}K, Radius: {p['koi_prad']} R⊕)\n"
                await update.message.reply_text(msg, parse_mode="Markdown")
            else:
                await update.message.reply_text("No habitable planets found in the current fetch limit.")
        else:
            await update.message.reply_text("❌ API Error.")

    # BUTTON 3: Random Planet
    elif text == "🎲 Random Planet":
        res = requests.get(API_URL, params={"limit": 500})
        if res.status_code == 200:
            data = res.json()
            if data:
                p = random.choice(data)
                hz_status = "Yes 🟢" if p.get('habitable_zone') else "No 🔴"
                msg = (
                    f"🎲 **Random Target Acquired!**\n\n"
                    f"**Name:** {p['kepoi_name']}\n"
                    f"**Status:** {p['koi_disposition']}\n"
                    f"**Orbital Period:** {p['koi_period']} days\n"
                    f"**Radius:** {p['koi_prad']} Earth radii\n"
                    f"**Temperature:** {p['koi_teq']} K\n"
                    f"**Potentially Habitable:** {hz_status}"
                )
                await update.message.reply_text(msg, parse_mode="Markdown")
            else:
                await update.message.reply_text("Database is currently empty.")
        else:
            await update.message.reply_text("❌ API Error.")

    # BUTTON 4: Database Stats
    elif text == "📈 Database Stats":
        res = requests.get(API_URL, params={"limit": 1000})
        if res.status_code == 200:
            data = res.json()
            confirmed = sum(1 for p in data if p['koi_disposition'] == 'CONFIRMED')
            candidates = sum(1 for p in data if p['koi_disposition'] == 'CANDIDATE')
            false_positives = sum(1 for p in data if p['koi_disposition'] == 'FALSE POSITIVE')
            
            msg = (
                f"📊 **Current Sample Statistics (Limit: 1000)**\n\n"
                f"✅ Confirmed Planets: **{confirmed}**\n"
                f"⚠️ Candidates: **{candidates}**\n"
                f"❌ False Positives: **{false_positives}**\n\n"
                f"*Data synced in real-time with FastAPI.*"
            )
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ API Error.")

    # BUTTON 5: Project Info
    elif text == "ℹ️ Project Info":
        msg = (
            "🚀 **Kepler Exoplanet Analytics (DSBA Project)**\n\n"
            "• **Backend:** FastAPI (Data processing & CRUD)\n"
            "• **Frontend:** Streamlit (Interactive Dashboards & 3D Radar)\n"
            "• **Bot:** python-telegram-bot (Mobile API Access)\n\n"
            "Designed to process NASA Kepler telemetric data."
        )
        await update.message.reply_text(msg, parse_mode="Markdown")

    # FREE TEXT: Smart Search
    else:
        # if the user typed something else, assume it's a planet name search
        res = requests.get(API_URL, params={"limit": 1000})
        if res.status_code == 200:
            data = res.json()
            # search case-insensitive
            found = next((p for p in data if text.lower() in p['kepoi_name'].lower()), None)
            
            if found:
                hz_status = "Yes 🟢" if found.get('habitable_zone') else "No 🔴"
                msg = (
                    f"🎯 **Search Result for '{text}':**\n\n"
                    f"**Name:** {found['kepoi_name']}\n"
                    f"**Status:** {found['koi_disposition']}\n"
                    f"**Radius:** {found['koi_prad']} Earth radii\n"
                    f"**Temperature:** {found['koi_teq']} K\n"
                    f"**Habitable:** {hz_status}"
                )
                await update.message.reply_text(msg, parse_mode="Markdown")
            else:
                await update.message.reply_text(f"🔍 Planet '{text}' not found in the current databank. Try another name (e.g., K00752.01).")
        else:
            await update.message.reply_text("❌ API Error during search.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Kepler Telegram Bot is running")
    app.run_polling()

if __name__ == "__main__":
    main()
