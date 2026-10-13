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

# Default QR Code URL (Aapka uploaded QR)
DEFAULT_QR = "https://raw.githubusercontent.com/telegram-bot-sdk/telegram-bot-sdk/main/tests/fixtures/image.jpg"

# Analytics / Stats Storage
STATS = {
    "pending": 0,
    "approved": 0,
    "rejected": 0
}

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
            "name": "1. All Category Combo (₹198)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹198\n♾ Lifetime Access | 🎬 50+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+ehTHId3ryhY3YmJl"
        },
        {
            "id": "btn_2",
            "name": "2. Pack 2 (₹98)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹98\n♾ Lifetime Access | 🎬 01+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+bPhyrYiSBQozNDBl"
        },
        {
            "id": "btn_3",
            "name": "3. Pack 3 (₹98)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹98\n♾ Lifetime Access | 🎬 01+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+b4HvE2hp_Cs2ZDBl"
        },
        {
            "id": "btn_4",
            "name": "4. Pack 4 (₹98)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹98\n♾ Lifetime Access | 🎬 01+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+b4HvE2hp_Cs2ZDBl"
        },
        {
            "id": "btn_5",
            "name": "5. Pack 5 (₹98)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹98\n♾ Lifetime Access | 🎬 01+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+b4HvE2hp_Cs2ZDBl"
        },
        {
            "id": "btn_6",
            "name": "6. Pack 6 (₹98)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹98\n♾ Lifetime Access | 🎬 01+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+b4HvE2hp_Cs2ZDBl"
        },
        {
            "id": "btn_7",
            "name": "7. Pack 7 (₹98)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹98\n♾ Lifetime Access | 🎬 01+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+b4HvE2hp_Cs2ZDBl"
        },
        {
            "id": "btn_8",
            "name": "8. Pack 8 (₹98)",
            "details": "💳 UPI ID: roxxxx@axl\n📲 Please scan the QR and pay, then click 'I have paid' ✅\n💰 Amount: ₹98\n♾ Lifetime Access | 🎬 01+ Group Full Video\n⚡ Instant Delivery After Payment\n🚫 No Extra Charges\n💯 No Fake / Dead Links",
            "link": "https://t.me/+b4HvE2hp_Cs2ZDBl"
        }
    ]
}

# States
WAITING_BTN_NAME, WAITING_BTN_DETAILS, WAITING_BTN_LINK, WAITING_WELCOME_TEXT, WAITING_EDIT_NAME = range(5)

# ----------------- CUSTOMER FLOW -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = DATA.get("welcome_text")
    
    keyboard = []
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

    admin_text = (
        f"⚙️ **TANWEER STORE - Admin Control Panel**\n\n"
        f"📊 **Payment Analytics:**\n"
        f"⏳ Pending Requests: `{STATS['pending']}`\n"
        f"✅ Approved Payments: `{STATS['approved']}`\n"
        f"❌ Rejected Payments: `{STATS['rejected']}`\n\n"
        f"Neeche diye gaye buttons se bot ko manage karein:"
    )
    
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Welcome Text", callback_data="admin_edit_welcome")],
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

    elif data.startswith("approve_"):
        parts = data.split("_")
        user_id = int(parts[1])
        item_id = "_".join(parts[2:])
        
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        delivery_link = selected_item["link"] if selected_item else "Link Not Found"
        
        if STATS["pending"] > 0:
            STATS["pending"] -= 1
        STATS["approved"] += 1
        
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 **Aapka payment Approve ho gaya hai!**\n\nAapka Access Link ye raha:\n🔗 {delivery_link}",
            parse_mode="Markdown"
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **APPROVED BY ADMIN**")

    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        
        if STATS["pending"] > 0:
            STATS["pending"] -= 1
        STATS["rejected"] += 1
        
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ **Aapka payment Reject kar diya gaya hai.** Kripya sahi screenshot bhejein."
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **REJECTED BY ADMIN**")

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

    if context.user_data.get("waiting_for_qr") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr"] = False
        DATA["qr_code"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ **Naya Payment QR Code set ho gaya!**")
        await admin_panel(update, context)
        return

    if context.user_data.get("waiting_for_proof"):
        item_id = context.user_data.get("selected_item_id")
        user = update.effective_user
        photo_id = update.message.photo[-1].file_id

        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        item_name = selected_item["name"] if selected_item else "Unknown Item"

        context.user_data["waiting_for_proof"] = False
        STATS["pending"] += 1
        
        await update.message.reply_text("⏳ Aapka screenshot admin ko bhej diya gaya hai. Verification ke baad link mil jayega.")

        admin_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}_{item_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
            ]
        ])
        
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=f"📩 **Naya Payment Screenshot aaya hai!**\n\n👤 **User:** @{user.username or 'No Username'} ({user.id})\n📦 **Selected Item:** {item_name}",
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
