from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import pandas as pd
import os

# Загружаем Excel
df = pd.read_excel('products.xlsx')

# Получаем уникальные категории
categories = df['Категория'].unique()

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Купить", callback_data='buy')],
        [InlineKeyboardButton("Оставить отзыв", callback_data='review')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать в наш магазин! Что вы хотите сделать?", reply_markup=reply_markup)

# Обработка нажатий
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy':
        keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat_{cat}")] for cat in categories]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите категорию:", reply_markup=reply_markup)
    
    elif query.data.startswith('cat_'):
        category = query.data.split('_', 1)[1]
        products = df[df['Категория'] == category]
        for _, row in products.iterrows():
            text = f"{row['Название']}\nЦена: {row['Цена']} руб."
            photo_path = os.path.join('photos', row['Фото'])  # Путь к фото
            if os.path.exists(photo_path):
                with open(photo_path, 'rb') as photo:
                    await query.message.reply_photo(photo=photo, caption=text)
            else:
                await query.message.reply_text(text)

    elif query.data == 'review':
        await query.edit_message_text("Вы можете оставить отзыв, написав нам сюда.")

# Главная функция
def main():
    TOKEN = "7713900787:AAHuEPpjV4Kgk5hPEA_dMTdQFOo9Z2yL7CM"  # <-- замените на ваш токен
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
    
if name == '__main__':
    main()
