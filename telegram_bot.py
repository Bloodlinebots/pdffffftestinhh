import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
import io
from fpdf import FPDF

# Enable logging
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Add this in Heroku config vars

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me some images and I'll convert them into a single PDF!")

image_store = {}

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    photo_file = await update.message.photo[-1].get_file()
    image_bytes = await photo_file.download_as_bytearray()
    
    if user_id not in image_store:
        image_store[user_id] = []

    image_store[user_id].append(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
    await update.message.reply_text("✅ Image received. Send more or type /convert to get your PDF.")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    images = image_store.get(user_id)

    if not images:
        await update.message.reply_text("⚠️ No images found. Send at least one image.")
        return

    pdf = FPDF(unit="pt", format="A4")
    for img in images:
        width, height = img.size
        a4_width, a4_height = 595, 842
        ratio = min(a4_width / width, a4_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size)

        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        pdf.add_page()
        pdf.image(img_bytes, x=(a4_width - new_size[0]) // 2, y=30, w=new_size[0], h=new_size[1])

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    await update.message.reply_document(document=pdf_output, filename="converted.pdf")
    image_store[user_id] = []  # clear user data

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    image_store[user_id] = []
    await update.message.reply_text("🗑️ All stored images cleared.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
