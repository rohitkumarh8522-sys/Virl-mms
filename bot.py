import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ConversationHandler, filters, ContextTypes
)

# ----------------- CONFIGURATIONS -----------------
TOKEN = os.getenv("BOT_TOKEN")  # Render Env Variable
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))  # Aapki Telegram ID
PORT = int(os.environ.get("PORT", 10000))

RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"https://{RENDER_HOST}" if RENDER_HOST else None)

# Default Working QR Code
DEFAULT_QR = "https://raw.githubusercontent.com/telegram-bot-sdk/telegram-bot-sdk/main/tests/fixtures/image.jpg"

# Analytics / Stats Storage
STATS = {
    "pending": 0,
    "approved": 0,
    "rejected": 0
}

# User Mapping Database (In-Memory)
USER_MAP = {}  # username -> user_id

# Dynamic Configuration
CONFIG = {
    "support_username": "tanweer_store_support"  # Without @ symbol
}

# Common Details Template for Pack 2 to 15 (₹98)
DETAILS_98 = (
    "💳 UPI ID: roxxxx@axl\n"
    "📲 Please scan the QR and pay, then click 'I have paid' ✅\n"
    "💰 Amount: ₹98\n"
    "♾ Lifetime Access | 🎬 01+ Group Full Video\n"
    "⚡ Instant Delivery After Payment\n"
    "🚫 No Extra Charges\n"
    "💯 No Fake / Dead Links"
)

# Default Link Template
DEFAULT_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

# ----------------- HARDCODED DEFAULT DATA -----------------
DATA = {
    "welcome_text": """🕊️𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗧𝗔𝗡𝗪𝗘𝗘𝗥 𝗦𝗧𝗢𝗥𝗘🕊️

⚡𝗡𝗘𝗪 𝗖𝗢𝗟𝗟𝗘𝗖𝗧𝗜𝗢𝗡 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘⚡

𝗘𝗔𝗖𝗛 𝗖𝗔𝗧𝗘𝗚𝗢𝗥𝗬 𝗖𝗢𝗡𝗧𝗔𝗜𝗡𝗦 4 𝗚𝗥𝗢𝗨𝗣𝗦 (𝟭𝟮𝟬𝟬-𝟭𝟴𝟬𝟬 𝗩𝗜𝗗𝗘𝗢𝗦 𝗣𝗘𝗥 𝗚𝗥𝗢𝗨𝗣)

🕊️𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗣𝗥𝗢𝗢𝗙𝗦👉https://t.me/+hbere12UWTMzYTI1

💥𝗗𝗘𝗠𝗢 𝗩𝗜𝗗𝗘𝗢𝗦👉https://t.me/+2jSY317AQww2ZjM9""",
    
    "qr_code": DEFAULT_QR,
    
    "items": [
        {
            "id": "btn_1",
            "name": "1. All Category Combo (₹199)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹199\n♾ Lifetime Access | 🎬 50+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+ehTHId3ryhY3YmJl"
        },
        {
            "id": "btn_2",
            "name": "2. Pack 2 (₹98)",
            "details": DETAILS_98,
            "link": "https://t.me/+bPhyrYiSBQozNDBl"
        },
        {"id": "btn_3", "name": "3. Pack 3 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_4", "name": "4. Pack 4 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_5", "name": "5. Pack 5 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_6", "name": "6. Pack 6 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_7", "name": "7. Pack 7 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_8", "name": "8. Pack 8 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_9", "name": "9. Pack 9 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_10", "name": "10. Pack 10 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_11", "name": "11. Pack 11 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_12", "name": "12. Pack 12 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_13", "name": "13. Pack 13 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_14", "name": "14. Pack 14 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK},
        {"id": "btn_15", "name": "15. Pack 15 (₹98)", "details": DETAILS_98, "link": DEFAULT_LINK}
    ]
}

# States for ConversationHandler
WAITING_BTN_NAME, WAITING_BTN_DETAILS, WAITING_BTN_LINK, WAITING_WELCOME_TEXT, WAITING_SUPPORT_USER = range(5)

# ----------------- CUSTOMER FLOW -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        USER_MAP[user.username.lower()] = user.id

    welcome_msg = DATA.get("welcome_text")
    
    keyboard = []
    for item in DATA["items"]:
        keyboard.append([InlineKeyboardButton(item["name"], callback_data=f"select_{item['id']}")])
        
    support_user = CONFIG.get("support_username", "admin")
    keyboard.append([InlineKeyboardButton("💬 Support / Contact Admin", url=f"https://t.me/{support_user}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=reply_markup)

# ----------------- ADMIN DIRECT MESSAGE TO USER -----------------
async def send_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ **Sahi tarika:**\n"
            "`/send <User_ID ya @username> <Aapka Message>`\n\n"
            "**Example:**\n"
            "`/send 123456789 Aapka payment mil gaya hai!`\n"
            "`/send @john_doe Aapka access active hai.`",
            parse_mode="Markdown"
        )
        return

    target = context.args[0].strip()
    msg_text = " ".join(context.args[1:])

    target_id = None
    if target.startswith("@"):
        uname = target.replace("@", "").lower()
        target_id = USER_MAP.get(uname)
        if not target_id:
            await update.message.reply_text(f"❌ Username `@{uname}` ki ID nahi mili. User ko pehle `/start` dabana hoga.")
            return
    else:
        try:
            target_id = int(target)
        except ValueError:
            await update.message.reply_text("❌ Kripya sahi User ID ya @username dalein.")
            return

    try:
        await context.bot.send_message(
            chat_id=target_id,
            text=f"📩 **Admin Message:**\n\n{msg_text}",
            parse_mode="Markdown"
        )
        await update.message.reply_text(f"✅ Message user `{target_id}` ko safaltapoorvak bhej diya gaya hai!")
    except Exception as e:
        await update.message.reply_text(f"❌ Message nahi bhej paaye: {str(e)}")

# ----------------- ADMIN PANEL -----------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    admin_text = (
        f"⚙️ **TANWEER STORE - Admin Control Panel**\n\n"
        f"📊 **Payment Analytics:**\n"
        f"⏳ Pending Requests: `{STATS['pending']}`\n"
        f"✅ Approved Payments: `{STATS['approved']}`\n"
        f"❌ Rejected Payments: `{STATS['rejected']}`\n\n"
        f"👤 Current Support Username: `@{CONFIG['support_username']}`\n\n"
        f"💬 **Direct Customer Msg Command:**\n"
        f"`/send <ID or @username> <Message>`\n\n"
        f"Neeche diye gaye options se bot ko manage karein:"
    )
    
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Welcome Text", callback_data="admin_edit_welcome")],
        [InlineKeyboardButton("✏️ Edit Support Username", callback_data="admin_edit_support")],
        [InlineKeyboardButton("✏️ Edit Button Name/Details", callback_data="admin_edit_btn_menu")],
        [InlineKeyboardButton("➕ Add New Button", callback_data="admin_add_btn")],
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
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        
        if not selected_item:
            await query.message.reply_text("❌ Ye option abhi uplabdha nahi hai.")
            return

        context.user_data["selected_item_id"] = item_id
        
        caption = f"🛒 **{selected_item['name']}**\n\n📝 **Details:**\n{selected_item['details']}\n\n━━━━━━━━━━━━━━━━━━━\n💳 **Pay karke '✅ I have paid' button dabayein.**"
        
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
        await query.message.reply_text("📸 Kripya apne payment ka Screenshot yahan bhejein:")

    elif data == "customer_back":
        await start(update, context)

    elif data.startswith("approve:"):
        payload = data.replace("approve:", "")
        parts = payload.split(":")
        user_id = int(parts[0])
        item_id = parts[1]
        
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        delivery_link = selected_item["link"] if selected_item else "Link Not Found"
        
        if STATS["pending"] > 0:
            STATS["pending"] -= 1
        STATS["approved"] += 1
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"🎉 **Aapka payment Approve ho gaya hai!**\n\nAapka Access Link ye raha:\n🔗 {delivery_link}",
                parse_mode="Markdown"
            )
            await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **APPROVED BY ADMIN**")
        except Exception as e:
            await query.message.reply_text(f"⚠️ Approved! Par user ko message nahi bhej paaye: {str(e)}")

    elif data.startswith("reject:"):
        payload = data.replace("reject:", "")
        user_id = int(payload)
        
        if STATS["pending"] > 0:
            STATS["pending"] -= 1
        STATS["rejected"] += 1
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ **Aapka payment Reject kar diya gaya hai.** Kripya sahi screenshot bhejein ya Support se contact karein."
            )
            await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **REJECTED BY ADMIN**")
        except Exception as e:
            await query.message.reply_text(f"⚠️ Rejected! Par user ko message nahi bhej paaye: {str(e)}")

    elif data == "admin_view_btns":
        msg = "📋 **Current Active Buttons & Links:**\n\n"
        for idx, item in enumerate(DATA["items"], 1):
            msg += f"**{idx}. {item['name']}**\n📄 **Details:**\n{item['details']}\n🔗 **Link:** {item['link']}\n\n"
        await query.message.reply_text(msg, parse_mode="Markdown")

    elif data == "admin_del_btn":
        keyboard = []
        for item in DATA["items"]:
            keyboard.append([InlineKeyboardButton(f"❌ Delete {item['name']}", callback_data=f"confirm_del_{item['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        await query.message.edit_text("Kis Button ko Delete karna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("confirm_del_"):
        item_id = data.replace("confirm_del_", "")
        DATA["items"] = [item for item in DATA["items"] if item["id"] != item_id]
        await query.message.reply_text("✅ Button delete ho gaya!")
        await admin_panel(update, context)

    elif data == "admin_back":
        await admin_panel(update, context)

    elif data == "admin_edit_btn_menu":
        keyboard = []
        for item in DATA["items"]:
            keyboard.append([InlineKeyboardButton(f"✏️ Edit {item['name']}", callback_data=f"start_edit_{item['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        await query.message.edit_text("Kis button ka Naam/Details badalna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))

# ----------------- SCREENSHOT & QR HANDLER -----------------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = update.effective_user
    if user.username:
        USER_MAP[user.username.lower()] = user.id

    if context.user_data.get("waiting_for_qr") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr"] = False
        DATA["qr_code"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ **Naya Payment QR Code set ho gaya!**")
        await admin_panel(update, context)
        return

    if context.user_data.get("waiting_for_proof"):
        item_id = context.user_data.get("selected_item_id")
        photo_id = update.message.photo[-1].file_id

        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        item_name = selected_item["name"] if selected_item else "Unknown Item"

        context.user_data["waiting_for_proof"] = False
        STATS["pending"] += 1
        
        await update.message.reply_text("⏳ Aapka screenshot admin ko bhej diya gaya hai. Verification ke baad link mil jayega.")

        admin_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user.id}:{item_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{user.id}")
            ]
        ])
        
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=f"📩 **Naya Payment Screenshot aaya hai!**\n\n👤 **User:** @{user.username or 'No Username'}\n🆔 **User ID:** `{user.id}`\n📦 **Selected Item:** {item_name}",
            reply_markup=admin_markup
        )

# ----------------- CONVERSATIONS -----------------
async def start_add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ **Step 1:** Naye Button ka **Naam** likhkar bhejein:")
    return WAITING_BTN_NAME

async def get_btn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_name"] = update.message.text
    await update.message.reply_text("📝 **Step 2:** Service ki **Details** likhkar bhejein:")
    return WAITING_BTN_DETAILS

async def get_btn_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_details"] = update.message.text
    await update.message.reply_text("🔗 **Step 3:** Access **Link** bhejein:")
    return WAITING_BTN_LINK

async def get_btn_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btn_name = context.user_data.get("temp_btn_name")
    btn_details = context.user_data.get("temp_btn_details")
    btn_link = update.message.text
    
    new_item = {
        "id": f"btn_{len(DATA['items']) + 1}",
        "name": btn_name, 
        "details": btn_details, 
        "link": btn_link
    }
    DATA["items"].append(new_item)
    
    await update.message.reply_text(f"✅ Naya button **'{btn_name}'** jod diya gaya!")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_edit_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📝 Naya **Welcome Message** likhkar bhejein:")
    return WAITING_WELCOME_TEXT

async def get_welcome_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DATA["welcome_text"] = update.message.text
    await update.message.reply_text("✅ **Welcome Message update ho gaya!**")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_edit_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ Naya **Support Telegram Username** lekhar bhejein (bina @ ke, jaise: `tanweer_store_support`):")
    return WAITING_SUPPORT_USER

async def get_support_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.replace("@", "").strip()
    CONFIG["support_username"] = username
    await update.message.reply_text(f"✅ **Support Username change ho gaya: @{username}**")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_change_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_qr"] = True
    await query.message.reply_text("🖼️ Naya **Payment QR Code** photo me bhejein:")

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

    edit_support_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_edit_support, pattern="^admin_edit_support$")],
        states={
            WAITING_SUPPORT_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_support_username)]
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("send", send_user_message))
    app.add_handler(add_btn_conv)
    app.add_handler(edit_welcome_conv)
    app.add_handler(edit_support_conv)
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
