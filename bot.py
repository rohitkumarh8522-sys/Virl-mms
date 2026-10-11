import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ConversationHandler, filters, ContextTypes
)

# ----------------- CONFIGURATIONS -----------------
TOKEN = os.getenv("BOT_TOKEN")  # Render Env Variable
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))  # आपकी Telegram ID
PORT = int(os.environ.get("PORT", 10000))  # Render का पोर्ट

RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"https://{RENDER_HOST}" if RENDER_HOST else None)

# Default Working QR Code Image URL
DEFAULT_QR = "https://raw.githubusercontent.com/telegram-bot-sdk/telegram-bot-sdk/main/tests/fixtures/image.jpg"

# Dynamic Data Storage
DATA = {
    "qr_code": DEFAULT_QR,
    "items": {
        "btn_1": {
            "name": "Demo Plan 1", 
            "details": "📌 **Plan Details:**\n• Validation: 30 Days\n• Full Access\n• 24/7 Support", 
            "link": "https://example.com/p1"
        }
    }
}

# States for ConversationHandler
WAITING_BTN_NAME, WAITING_BTN_DETAILS, WAITING_BTN_LINK = range(3)

# ----------------- CUSTOMER FLOW -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "👋 **हमारे Business Bot में आपका स्वागत है!**\n\nनीचे दिए गए ऑप्शन में से अपनी पसंद की सर्विस चुनें:"
    
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

# ----------------- ADMIN PANEL -----------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    admin_text = "⚙️ **Admin Control Panel**\n\nयहाँ से आप Bot को कंट्रोल कर सकते हैं:"
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add New Button (Name, Details & Link)", callback_data="admin_add_btn")],
        [InlineKeyboardButton("🖼️ Change QR Code", callback_data="admin_change_qr")],
        [InlineKeyboardButton("🗑️ Delete Button", callback_data="admin_del_btn")],
        [InlineKeyboardButton("📋 View All Buttons", callback_data="admin_view_btns")]
    ])
    
    if update.message:
        await update.message.reply_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)
    elif update.callback_query:
        await update.callback_query.message.edit_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)

# ----------------- CALLBACK HANDLER -----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("select_"):
        item_key = data.split("_")[1]
        context.user_data["selected_item"] = item_key
        
        item_data = DATA['items'].get(item_key)
        if not item_data:
            await query.message.reply_text("❌ यह आइटम अब उपलब्ध नहीं है।")
            return

        item_name = item_data.get("name", "Service")
        item_details = item_data.get("details", "कोई विवरण उपलब्ध नहीं है।")

        caption = f"🛒 **{item_name}**\n\n📝 **विवरण / Details:**\n{item_details}\n\n━━━━━━━━━━━━━━━━━━━\n💳 **पेमेंट करने के लिए ऊपर दिए QR कोड को स्कैन करें और फिर '✅ I have paid' बटन दबाएं।**"
        
        pay_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I have paid", callback_data="paid")],
            [InlineKeyboardButton("🔙 Back", callback_data="customer_back")]
        ])
        
        try:
            await query.message.reply_photo(photo=DATA["qr_code"], caption=caption, parse_mode="Markdown", reply_markup=pay_buttons)
        except Exception as e:
            # अगर QR फ़ोटो लोड नहीं होती है तो केवल टेक्स्ट मैसेज भेज दिया जाएगा
            await query.message.reply_text(caption, parse_mode="Markdown", reply_markup=pay_buttons)

    elif data == "paid":
        context.user_data["waiting_for_proof"] = True
        await query.message.reply_text("📸 कृपया अपने पेमेंट का Screenshot यहाँ भेजें:")

    elif data == "customer_back":
        await start(update, context)

    elif data.startswith("approve_"):
        parts = data.split("_")
        user_id = int(parts[1])
        item_key = parts[2]
        
        delivery_link = DATA["items"][item_key]["link"]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 **आपका पेमेंट Approve हो गया है!**\n\nआपका Access Link यह रहा: {delivery_link}",
            parse_mode="Markdown"
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **APPROVED BY ADMIN**")

    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ **आपका पेमेंट Reject कर दिया गया है।** कृपया सही स्क्रीनशॉट भेजें।"
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **REJECTED BY ADMIN**")

    elif data == "admin_view_btns":
        msg = "📋 **Current Buttons, Details & Links:**\n\n"
        for k, v in DATA["items"].items():
            msg += f"• **{v['name']}**\n  📄 Details: {v.get('details', 'N/A')}\n  🔗 Link: {v['link']}\n\n"
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif data == "admin_del_btn":
        keyboard = []
        for k, v in DATA["items"].items():
            keyboard.append([InlineKeyboardButton(f"❌ Delete {v['name']}", callback_data=f"confirm_del_{k}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        await query.message.edit_text("किस Button को Delete करना चाहते हैं?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("confirm_del_"):
        item_key = data.replace("confirm_del_", "")
        if item_key in DATA["items"]:
            del DATA["items"][item_key]
            await query.message.reply_text("✅ Button सफलतापूर्वक डिलीट कर दिया गया!")
        await admin_panel(update, context)

    elif data == "admin_back":
        await admin_panel(update, context)

# ----------------- SCREENSHOT & QR HANDLER -----------------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # 1. Admin Changing QR Code
    if context.user_data.get("waiting_for_qr") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr"] = False
        DATA["qr_code"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ **नया QR Code सेट हो गया है!** अब ग्राहक जब भी बटन पर क्लिक करेंगे, यही QR दिखेगा।")
        await admin_panel(update, context)
        return

    # 2. Customer Sending Payment Screenshot
    if context.user_data.get("waiting_for_proof"):
        item_key = context.user_data.get("selected_item")
        user = update.effective_user
        photo_id = update.message.photo[-1].file_id

        context.user_data["waiting_for_proof"] = False
        await update.message.reply_text("⏳ आपका स्क्रीनशॉट एडमिन को भेज दिया गया है। वेरिफिकेशन के बाद आपको लिंक मिल जाएगा।")

        admin_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{item_key}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
            ]
        ])
        
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=f"📩 **नया Payment Screenshot आया है!**\n\n👤 **User:** @{user.username or 'No Username'} ({user.id})\n📦 **Selected Item:** {DATA['items'][item_key]['name']}",
            reply_markup=admin_markup
        )

# ----------------- CONVERSATION FOR ADDING BUTTONS -----------------
async def start_add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ **Step 1:** नये Button का **नाम (Name)** लिखकर भेजें:")
    return WAITING_BTN_NAME

async def get_btn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_name"] = update.message.text
    await update.message.reply_text("📝 **Step 2:** इस प्रोडक्ट/सर्विस का **विवरण (Details)** लिखकर भेजें (उदा: कितने दिन चलेगा, क्या-क्या मिलेगा):")
    return WAITING_BTN_DETAILS

async def get_btn_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_details"] = update.message.text
    await update.message.reply_text("🔗 **Step 3:** पेमेंट के बाद ग्राहक को मिलने वाला **Link** भेजें:")
    return WAITING_BTN_LINK

async def get_btn_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btn_name = context.user_data.get("temp_btn_name")
    btn_details = context.user_data.get("temp_btn_details")
    btn_link = update.message.text
    
    new_id = f"btn_{len(DATA['items']) + 1}"
    DATA["items"][new_id] = {
        "name": btn_name, 
        "details": btn_details, 
        "link": btn_link
    }
    
    await update.message.reply_text(f"✅ नया बटन **'{btn_name}'** सफलतापूर्वक जोड़ दिया गया है!")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_change_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_qr"] = True
    await query.message.reply_text("🖼️ नया **QR Code की फोटो** यहाँ भेजें:")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    add_btn_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_add_button, pattern="^admin_add_btn$")],
        states={
            WAITING_BTN_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_btn_name)],
            WAITING_BTN_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_btn_details)],
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
