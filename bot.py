import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ConversationHandler, filters, ContextTypes
)

# ----------------- CONFIGURATIONS -----------------
TOKEN = os.getenv("BOT_TOKEN")  # Render Env Variable
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))  # Aapki Telegram ID
PORT = int(os.environ.get("PORT", 10000))  # Render ka automatic port

# Render External Hostname
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"https://{RENDER_HOST}" if RENDER_HOST else None)

# Dynamic Data Storage
DATA = {
    "qr_code": "https://via.placeholder.com/300?text=Scan+and+Pay", # Default QR
    "items": {
        "btn_1": {"name": "Product 1", "link": "https://example.com/p1"},
        "btn_2": {"name": "Product 2", "link": "https://example.com/p2"},
    }
}

WAITING_BTN_NAME, WAITING_BTN_LINK = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "👋 **Hamare Business Bot me aapka swagat hai!**\n\nNeeche diye gaye option me se apni pasand ki service chunein:"
    
    keyboard = []
    items = list(DATA["items"].items())
    
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i][1]["name"], callback_data=f"select_{items[i][0]}")]
        if i + 1 < len(items):
            row.append(InlineKeyboardButton(items[i+1][1]["name"], callback_data=f"select_{items[i+1][0]}"))
        keyboard.append(row)
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    admin_text = "⚙️ **Admin Control Panel**\n\nYahan se aap bot ko control kar sakte hain:"
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add New Button & Link", callback_data="admin_add_btn")],
        [InlineKeyboardButton("🖼️ Change QR Code", callback_data="admin_change_qr")],
        [InlineKeyboardButton("🗑️ Delete Button", callback_data="admin_del_btn")],
        [InlineKeyboardButton("📋 View All Buttons", callback_data="admin_view_btns")]
    ])
    
    if update.message:
        await update.message.reply_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)
    elif update.callback_query:
        await update.callback_query.message.edit_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("select_"):
        item_key = data.split("_")[1]
        context.user_data["selected_item"] = item_key
        
        caption = f"📌 Aapne **{DATA['items'][item_key]['name']}** chuna hai.\n\nNeeche QR code scan karke payment karein aur **'I have paid'** button par click karein."
        pay_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I have paid", callback_data="paid")],
            [InlineKeyboardButton("🔙 Back", callback_data="customer_back")]
        ])
        
        await query.message.reply_photo(photo=DATA["qr_code"], caption=caption, parse_mode="Markdown", reply_markup=pay_buttons)

    elif data == "paid":
        context.user_data["waiting_for_proof"] = True
        await query.message.reply_text("📸 Kripya apne payment ka Screenshot yahan bhejein:")

    elif data == "customer_back":
        await start(update, context)

    elif data.startswith("approve_"):
        parts = data.split("_")
        user_id = int(parts[1])
        item_key = parts[2]
        
        delivery_link = DATA["items"][item_key]["link"]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 **Aapka payment Approve ho gaya hai!**\n\nAapka Access Link: {delivery_link}",
            parse_mode="Markdown"
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **APPROVED**")

    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ **Aapka payment Reject kar diya gaya hai.** Kripya sahi screenshot bhejein."
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **REJECTED**")

    elif data == "admin_view_btns":
        msg = "📋 **Current Buttons & Links:**\n\n"
        for k, v in DATA["items"].items():
            msg += f"• **{v['name']}**: {v['link']}\n"
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif data == "admin_del_btn":
        keyboard = []
        for k, v in DATA["items"].items():
            keyboard.append([InlineKeyboardButton(f"❌ Delete {v['name']}", callback_data=f"confirm_del_{k}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        await query.message.edit_text("Kis Button ko Delete karna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("confirm_del_"):
        item_key = data.replace("confirm_del_", "")
        if item_key in DATA["items"]:
            del DATA["items"][item_key]
            await query.message.reply_text("✅ Button safaltapoorvak delete kar diya gaya!")
        await admin_panel(update, context)

    elif data == "admin_back":
        await admin_panel(update, context)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if context.user_data.get("waiting_for_qr") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr"] = False
        DATA["qr_code"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ **Naya QR Code set ho gaya hai!**")
        await admin_panel(update, context)
        return

    if context.user_data.get("waiting_for_proof"):
        item_key = context.user_data.get("selected_item")
        user = update.effective_user
        photo_id = update.message.photo[-1].file_id

        context.user_data["waiting_for_proof"] = False
        await update.message.reply_text("⏳ Aapka screenshot admin ko bhej diya gaya hai.")

        admin_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{item_key}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
            ]
        ])
        
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=f"📩 **Naya Payment Screenshot aaya hai!**\n\n👤 **User:** @{user.username or 'No Username'} ({user.id})\n📦 **Selected Item:** {DATA['items'][item_key]['name']}",
            reply_markup=admin_markup
        )

async def start_add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ Naye Button ka **naam** likh kar bhejein:")
    return WAITING_BTN_NAME

async def get_btn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_name"] = update.message.text
    await update.message.reply_text("🔗 Ab is Button ke liye **Link** bhejein:")
    return WAITING_BTN_LINK

async def get_btn_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btn_name = context.user_data.get("temp_btn_name")
    btn_link = update.message.text
    
    new_id = f"btn_{len(DATA['items']) + 1}"
    DATA["items"][new_id] = {"name": btn_name, "link": btn_link}
    
    await update.message.reply_text(f"✅ Naya button **'{btn_name}'** jod diya gaya hai!")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_change_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_qr"] = True
    await query.message.reply_text("🖼️ Naya **QR Code ki photo** yahan bhejein:")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    add_btn_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_add_button, pattern="^admin_add_btn$")],
        states={
            WAITING_BTN_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_btn_name)],
            WAITING_BTN_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_btn_link)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(add_btn_conv)
    app.add_handler(CallbackQueryHandler(start_change_qr, pattern="^admin_change_qr$"))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print(f"Starting webhook on port {PORT} with URL {WEBHOOK_URL}...")
    
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
        bootstrap_retries=3
    )

if __name__ == "__main__":
    main()