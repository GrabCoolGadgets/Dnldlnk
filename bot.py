import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    search_url = f"https://apk4free.net/?s={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        first_result = soup.select_one("h2.post-title a")

        if not first_result:
            await update.message.reply_text("❌ Koi APK result nahi mila.")
            return

        app_title = first_result.text.strip()
        app_page = first_result['href']

        # Get download link
        app_page_res = requests.get(app_page, headers=headers, timeout=10)
        app_soup = BeautifulSoup(app_page_res.text, "html.parser")
        download_btn = app_soup.select_one("a[href*='apkadmin.com'], a[href*='mediafire.com'], a[href*='dropbox.com']")

        if download_btn:
            download_link = download_btn['href']
            reply = f"📱 {app_title}\n⬇️ [Download Link]({download_link})"
            await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            await update.message.reply_text(f"📱 {app_title}\n🔗 {app_page}\n(Link page par hi milega)")
    except Exception as e:
        await update.message.reply_text("⚠️ Error: " + str(e))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
