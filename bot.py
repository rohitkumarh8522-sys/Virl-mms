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

# Default Working QR Code Image
DEFAULT_QR = "https://via.placeholder.com/300?text=Scan+and+Pay"

# Dynamic Data Storage (In-Memory)
DATA = {
    "welcome_text": "👋 **हमारे Business Bot में आपका स्वागत है!**\n\n**यह कैसे काम करता है?**\n1. नीचे दिए गए किसी भी प्रोडक्ट/सर्विस बटन पर क्लिक करें।\n2. पेमेंट QR कोड स्कैन करें और पेमेंट पूरा करें।\n3. '✅ I have paid' पर क्लिक करके स्क्रीनशॉट अपलोड करें।\n4. एडमिन वेरिफिकेशन के बाद आपको आपका एक्सेस लिंक मिल जाएगा।\n\n👇 **अपनी पसंद की सर्विस चुनें:**",
    "qr_code": DEFAULT_QR,
    "items": [
        {
            "id": "item_1",
            "name": "1. Demo Product / VIP Membership", 
            "details": "📌 **Plan Details:**\n• Validity: 30 Days\n• Access: Full Access\n• Support: 24/7 Premium Support", 
            "link": "https://example.com/demo"
        }
    ]
}

# States for ConversationHandler
WAITING_BTN_NAME, WAITING_BTN_DETAILS, WAITING_BTN_LINK, WAITING_WELCOME_TEXT = range(4)

# ----------------- CUSTOMER FLOW -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = DATA.get("welcome_text", "👋 **हमारे Business Bot में आपका स्वागत है!**")
    
    keyboard = []
    # Buttons को 1, 2, 3 एक के नीचे एक (Single Column) लगाना
    for item in DATA["items"]:
        keyboard.append([InlineKeyboardButton(item["name"], callback_data=f"select_{item['id']}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=reply_markup)

# ----------------- ADMIN PANEL -----------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    admin_text = "⚙️ **Smart Admin Control Panel**\n\nयहाँ से आप पूरे बॉट को आसानी से कंट्रोल कर सकते हैं:"
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Welcome Text (How it works)", callback_data="admin_edit_welcome")],
        [InlineKeyboardButton("➕ Add New Button (Name, Details & Link)", callback_data="admin_add_btn")],
        [InlineKeyboardButton("🖼️ Change Payment QR Code", callback_data="admin_change_qr")],
        [InlineKeyboardButton("🗑️ Delete Button", callback_data="admin_del_btn")],
        [InlineKeyboardButton("📋 View All Buttons & Links", callback_data="admin_view_btns")]
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
        item_id = data.replace("select_", "")
        
        # ID के आधार पर आइटम खोजना
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        
        if not selected_item:
            await query.message.reply_text("❌ यह आइटम अब उपलब्ध नहीं है। कृपया नया बटन चुनें।")
            return

        context.user_data["selected_item_id"] = item_id
        
        item_name = selected_item.get("name", "Service")
        item_details = selected_item.get("details", "कोई विवरण उपलब्ध नहीं है।")

        caption = f"🛒 **{item_name}**\n\n📝 **विवरण / Details:**\n{item_details}\n\n━━━━━━━━━━━━━━━━━━━\n💳 **पेमेंट करने के लिए QR कोड स्कैन करें और फिर '✅ I have paid' बटन दबाएं।**"
        
        pay_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I have paid", callback_data="paid")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="customer_back")]
        ])
        
        try:
            await query.message.reply_photo(photo=DATA["qr_code"], caption=caption, parse_mode="Markdown", reply_markup=pay_buttons)
        except Exception:
            await query.message.reply_text(caption, parse_mode="Markdown", reply_markup=pay_buttons)

    elif data == "paid":
        context.user_data["waiting_for_proof"] = True
        await query.message.reply_text("📸 कृपया अपने पेमेंट का Screenshot यहाँ भेजें:")

    elif data == "customer_back":
        await start(update, context)

    elif data.startswith("approve_"):
        parts = data.split("_")
        user_id = int(parts[1])
        item_id = parts[2]
        
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        delivery_link = selected_item["link"] if selected_item else "Link Not Found"
        
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 **आपका पेमेंट Approve हो गया है!**\n\nआपका Access Link यह रहा:\n🔗 {delivery_link}",
            parse_mode="Markdown"
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **APPROVED BY ADMIN**")

    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ **आपका पेमेंट Reject कर दिया गया है।** कृपया सही स्क्रीनशॉट भेजें या सपोर्ट से संपर्क करें।"
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **REJECTED BY ADMIN**")

    elif data == "admin_view_btns":
        msg = "📋 **Current Active Buttons & Links:**\n\n"
        for idx, item in enumerate(DATA["items"], 1):
            msg += f"**{idx}. {item['name']}**\n📄 **Details:** {item['details']}\n🔗 **Link:** {item['link']}\n\n"
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif data == "admin_del_btn":
        keyboard = []
        for item in DATA["items"]:
            keyboard.append([InlineKeyboardButton(f"❌ Delete {item['name']}", callback_data=f"confirm_del_{item['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        await query.message.edit_text("किस Button को Delete करना चाहते हैं?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("confirm_del_"):
        item_id = data.replace("confirm_del_", "")
        DATA["items"] = [item for item in DATA["items"] if item["id"] != item_id]
        await query.message.reply_text("✅ Button सफलतापूर्वक डिलीट कर दिया गया!")
        await admin_panel(update, context)

    elif data == "admin_back":
        await admin_panel(update, context)

# ----------------- SCREENSHOT & QR HANDLER -----------------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Admin updating QR Code
    if context.user_data.get("waiting_for_qr") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr"] = False
        DATA["qr_code"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ **नया QR Code सेट हो गया है!**")
        await admin_panel(update, context)
        return

    # Customer uploading Screenshot
    if context.user_data.get("waiting_for_proof"):
        item_id = context.user_data.get("selected_item_id")
        user = update.effective_user
        photo_id = update.message.photo[-1].file_id

        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        item_name = selected_item["name"] if selected_item else "Unknown Item"

        context.user_data["waiting_for_proof"] = False
        await update.message.reply_text("⏳ आपका स्क्रीनशॉट एडमिन को भेज दिया गया है। वेरीफिकेशन के बाद आपको लिंक मिल जाएगा।")

        admin_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{item_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
            ]
        ])
        
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=f"📩 **नया Payment Screenshot आया है!**\n\n👤 **User:** @{user.username or 'No Username'} ({user.id})\n📦 **Selected Item:** {item_name}",
            reply_markup=admin_markup
        )

# ----------------- CONVERSATIONS -----------------
async def start_add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ **Step 1:** नये Button का **नाम** लिखकर भेजें (उदा: 1. VIP Course):")
    return WAITING_BTN_NAME

async def get_btn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_name"] = update.message.text
    await update.message.reply_text("📝 **Step 2:** इस प्रोडक्ट/सर्विस का **विवरण (Details)** लिखकर भेजें (उदा: कितने दिन चलेगा, क्या-क्या मिलेगा):")
    return WAITING_BTN_DETAILS

async def get_btn_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_details"] = update.message.text
    await update.message.reply_text("🔗 **Step 3:** पेमेंट अप्रूव होने के बाद ग्राहक को मिलने वाला **Link** भेजें:")
    return WAITING_BTN_LINK

async def get_btn_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btn_name = context.user_data.get("temp_btn_name")
    btn_details = context.user_data.get("temp_btn_details")
    btn_link = update.message.text
    
    new_item = {
        "id": f"item_{len(DATA['items']) + 1}_{os.urandom(2).hex()}",
        "name": btn_name, 
        "details": btn_details, 
        "link": btn_link
    }
    DATA["items"].append(new_item)
    
    await update.message.reply_text(f"✅ नया बटन **'{btn_name}'** सफलतापूर्वक जोड़ दिया गया है!")
    await admin_panel(update, context)
    return ConversationHandler.END

# Welcome Text Edit Handlers
async def start_edit_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📝 नया **Welcome Message / How it works Details** लिखकर भेजें:")
    return WAITING_WELCOME_TEXT

async def get_welcome_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DATA["welcome_text"] = update.message.text
    await update.message.reply_text("✅ **Welcome Message सफलतापूर्वक अपडेट कर दिया गया है!**")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_change_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_qr"] = True
    await query.message.reply_text("🖼️ नया **Payment QR Code की फोटो** यहाँ भेजें:")

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

    edit_welcome_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_edit_welcome, pattern="^admin_edit_welcome$")],
        states={
            WAITING_WELCOME_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_welcome_text)]
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(add_btn_conv)
    app.add_handler(edit_welcome_conv)
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
