import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render se secure token lega

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    search_url = f"https://vegamovies.quest/?s={query.replace(' ', '+')}"
    headers = { "User-Agent": "Mozilla/5.0" }

    try:
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        first = soup.select_one("h2.title a")

        if not first:
            await update.message.reply_text("❌ Koi result nahi mila.")
            return

        title = first.text.strip()
        post_link = first['href']

        post_res = requests.get(post_link, headers=headers)
        post_soup = BeautifulSoup(post_res.text, "html.parser")
        dl = post_soup.select_one("a[href*='.mkv'], a[href*='.mp4'], a[href*='drive.google.com']")

        if dl:
            final_link = dl['href']
            reply = f"🎬 {title}\n⬇️ [Download Now]({final_link})"
            await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=False)
        else:
            await update.message.reply_text("😢 Link nahi mila.")
    except Exception as e:
        await update.message.reply_text("⚠️ Error: " + str(e))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
