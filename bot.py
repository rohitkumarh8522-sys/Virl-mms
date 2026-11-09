import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ConversationHandler, filters, ContextTypes
)

# =====================================================================
# ✏️ EASY EDIT SECTION: 12 Buttons & Links
# =====================================================================

WELCOME_MESSAGE = """▪️𝐂𝐄𝐑𝐓𝐈𝐅𝐈𝐄𝐃 𝐒𝐇𝐎𝐏▪️

!!𝐍𝐄𝐖 𝐂𝐎𝐋𝐄𝐂𝐓𝐈𝐎𝐍!!

 ▪️𝐄𝐕𝐄𝐑𝐘 𝐂𝐀𝐓𝐄𝐆𝐎𝐑𝐘  𝐈𝐍𝐂𝐋𝐔𝐃𝐄𝐒 8 𝐆𝐑𝐎𝐔𝐏𝐒!!!

💥𝐁𝐔𝐘 𝐅𝐔𝐋𝐋 𝐏𝐀𝐂𝐊𝐀𝐆𝐄 𝐀𝐓 𝟏𝟗𝟗 𝐀𝐍𝐃 𝐆𝐄𝐓 𝟐𝟎𝟎+𝐃𝐀𝐈𝐋𝐘 𝐍𝐄𝐖 𝐔𝐏𝐋𝐎𝐀𝐃𝐄𝐃 𝐆𝐑𝐎𝐔𝐏𝐒

*𝐎𝐍𝐄 𝐓𝐈𝐌𝐄 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐏𝐄𝐑𝐌𝐄𝐍𝐄𝐍𝐓 𝐀𝐂𝐂𝐄𝐒𝐒*

𝐍𝐎 𝐄𝐗𝐓𝐑𝐀 𝐂𝐇𝐀𝐑𝐆𝐄
𝐍𝐎 𝐄𝐗𝐏𝐈𝐑𝐄𝐃 𝐋𝐈𝐍𝐊𝐒

*𝐃𝐀𝐈𝐋𝐘 𝐍𝐄𝐖 𝐕𝐈𝐃𝐄𝐎𝐒 𝐔𝐏𝐋𝐎𝐀𝐃𝐄𝐃✅

𝐒𝐔𝐏𝐎𝐑𝐓 : @BOTSUPPORTHELL

𝐃𝐄𝐌𝐎 𝐏𝐈𝐂𝐒: https://t.me/+8NSAu6AwbuQ1ZTk1
𝐏𝐀𝐘𝐌𝙴𝙽𝚃 𝐏𝐑𝐎𝐎𝐅𝐒: https://t.me/+AnxkmFajMo01ZDVl
𝐃𝐄𝐌𝐎 𝐕𝐈𝐃𝐄𝐎𝐒 : https://t.me/+qIaukTR44z1hYTk9"""

DEFAULT_SUPPORT_USERNAME = "BOTSUPPORTHELL"

# ---------------- 12 BUTTONS CONFIGURATION ----------------
BTN_1_NAME  = "1. All Category Combo (₹199)"
BTN_1_LINK  = "https://t.me/+ehTHId3ryhY3YmJl"

BTN_2_NAME  = "2. Pack 2 (₹98)"
BTN_2_LINK  = "https://t.me/+bPhyrYiSBQozNDBl"

BTN_3_NAME  = "3. Pack 3 (₹98)"
BTN_3_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_4_NAME  = "4. Pack 4 (₹98)"
BTN_4_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_5_NAME  = "5. Pack 5 (₹98)"
BTN_5_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_6_NAME  = "6. Pack 6 (₹98)"
BTN_6_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_7_NAME  = "7. Pack 7 (₹98)"
BTN_7_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_8_NAME  = "8. Pack 8 (₹98)"
BTN_8_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_9_NAME  = "9. Pack 9 (₹98)"
BTN_9_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_10_NAME = "10. Pack 10 (₹98)"
BTN_10_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_11_NAME = "11. Pack 11 (₹98)"
BTN_11_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_12_NAME = "12. Pack 12 (₹98)"
BTN_12_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

# =====================================================================
# ⚙️ SYSTEM CONFIGURATIONS
# =====================================================================

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))
PORT = int(os.environ.get("PORT", 10000))

RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"https://{RENDER_HOST}" if RENDER_HOST else None)

DEFAULT_QR = "https://raw.githubusercontent.com/telegram-bot-sdk/telegram-bot-sdk/main/tests/fixtures/image.jpg"

STATS = {"pending": 0, "approved": 0, "rejected": 0}
USER_MAP = {}
CONFIG = {"support_username": DEFAULT_SUPPORT_USERNAME}

# Separate QR storage for 199 and 98 packs
QR_CONFIG = {
    "qr_199": DEFAULT_QR,
    "qr_98": DEFAULT_QR
}

DETAILS_199 = (
    "!!𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝙳𝙴𝚃𝙰𝙸𝙻𝚂!!\n\n"
    "💰𝙿𝚁𝙸𝙲𝙴: ₹199\n\n"
    "📌 𝙰𝙵𝚃𝙴𝚁 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 → 𝚃𝙰𝙿 “𝙸 𝙷𝙰𝚅𝙴 𝙿𝙰𝙸𝙳” → 𝚂𝙴𝙽𝙳 𝚈𝙾𝚄𝚁 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝚂𝙲𝚁𝙴𝙴𝙽𝚂𝙷𝙾𝚃 ✅\n\n"
    "🔐 𝙾𝙽𝙲𝙴 𝚈𝙾𝚄𝚁 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝙸𝚂 𝚅𝙴𝚁𝙸𝙵𝙸𝙴𝙳, 𝚈𝙾𝚄𝚁 𝙾𝚁𝙳𝙴𝚁 𝚆𝙸𝙻𝙻 𝙱𝙴 𝙳𝙴𝙻𝙸𝚅𝙴𝚁𝙴𝙳 𝙸𝙽𝚂𝚃𝙰𝙽𝚃𝙻𝚈\n\n"
    "🎁 𝙻𝙸𝙵𝙴𝚃𝙸𝙼𝙴 𝙰𝙲𝙲𝙴𝚂𝚂\n"
    "🚫 𝙽𝙾 𝙴𝚇𝚃𝚁𝙰 𝙲𝙷𝙰𝚁𝙶𝙴𝚂"
)

DETAILS_98 = (
    "!!𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝙳𝙴𝚃𝙰𝙸𝙻𝚂!!\n\n"
    "💰𝙿𝚁𝙸𝙲𝙴: ₹98\n\n"
    "📌 𝙰𝙵𝚃𝙴𝚁 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 → 𝚃𝙰𝙿 “𝙸 𝙷𝙰𝚅𝙴 𝙿𝙰𝙸𝙳” → 𝚂𝙴𝙽𝙳 𝚈𝙾𝚄𝚁 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝚂𝙲𝚁𝙴𝙴𝙽𝚂𝙷𝙾𝚃 ✅\n\n"
    "🔐 𝙾𝙽𝙲𝙴 𝚈𝙾𝚄𝚁 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝙸𝚂 𝚅𝙴𝚁𝙸𝙵𝙸𝙴𝙳, 𝚈𝙾𝚄𝚁 𝙾𝚁𝙳𝙴𝚁 𝚆𝙸𝙻𝙻 𝙱𝙴 𝙳𝙴𝙻𝙸𝚅𝙴𝚁𝙴𝙳 𝙸𝙽𝚂𝚃𝙰𝙽𝚃𝙻𝚈\n\n"
    "🎁 𝙻𝙸𝙵𝙴𝚃𝙸𝙼𝙴 𝙰𝙲𝙲𝙴𝚂𝚂\n"
    "🚫 𝙽𝙾 𝙴𝚇𝚃𝚁𝙰 𝙲𝙷𝙰𝚁𝙶𝙴𝚂"
)

DATA = {
    "welcome_text": WELCOME_MESSAGE,
    "items": [
        {"id": "btn_1",  "name": BTN_1_NAME,  "details": DETAILS_199, "link": BTN_1_LINK, "price_type": "199"},
        {"id": "btn_2",  "name": BTN_2_NAME,  "details": DETAILS_98,  "link": BTN_2_LINK, "price_type": "98"},
        {"id": "btn_3",  "name": BTN_3_NAME,  "details": DETAILS_98,  "link": BTN_3_LINK, "price_type": "98"},
        {"id": "btn_4",  "name": BTN_4_NAME,  "details": DETAILS_98,  "link": BTN_4_LINK, "price_type": "98"},
        {"id": "btn_5",  "name": BTN_5_NAME,  "details": DETAILS_98,  "link": BTN_5_LINK, "price_type": "98"},
        {"id": "btn_6",  "name": BTN_6_NAME,  "details": DETAILS_98,  "link": BTN_6_LINK, "price_type": "98"},
        {"id": "btn_7",  "name": BTN_7_NAME,  "details": DETAILS_98,  "link": BTN_7_LINK, "price_type": "98"},
        {"id": "btn_8",  "name": BTN_8_NAME,  "details": DETAILS_98,  "link": BTN_8_LINK, "price_type": "98"},
        {"id": "btn_9",  "name": BTN_9_NAME,  "details": DETAILS_98,  "link": BTN_9_LINK, "price_type": "98"},
        {"id": "btn_10", "name": BTN_10_NAME, "details": DETAILS_98, "link": BTN_10_LINK, "price_type": "98"},
        {"id": "btn_11", "name": BTN_11_NAME, "details": DETAILS_98, "link": BTN_11_LINK, "price_type": "98"},
        {"id": "btn_12", "name": BTN_12_NAME, "details": DETAILS_98, "link": BTN_12_LINK, "price_type": "98"},
    ]
}

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
        
    support_user = CONFIG.get("support_username", DEFAULT_SUPPORT_USERNAME)
    keyboard.append([InlineKeyboardButton("💬 Support / Contact Admin", url=f"https://t.me/{support_user}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_msg, reply_markup=reply_markup)

# ----------------- ADMIN DIRECT MSG TO USER -----------------
async def send_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ Command Use Format:\n"
            "/send <User_ID ya @username> <Message>\n\n"
            "Example:\n"
            "/send 123456789 Aapka payment mil gaya hai!\n"
            "/send @john_doe Aapka access active hai."
        )
        return

    target = context.args[0].strip()
    msg_text = " ".join(context.args[1:])

    target_id = None
    if target.startswith("@"):
        uname = target.replace("@", "").lower()
        target_id = USER_MAP.get(uname)
        if not target_id:
            await update.message.reply_text(f"❌ Username @{uname} ki ID nahi mili. User ko pehle /start dabana hoga.")
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
            text=f"📩 Admin Message:\n\n{msg_text}"
        )
        await update.message.reply_text(f"✅ Message user {target_id} ko safaltapoorvak bhej diya gaya hai!")
    except Exception as e:
        await update.message.reply_text(f"❌ Message nahi bhej paaye: {str(e)}")

# ----------------- ADMIN PANEL -----------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    admin_text = (
        "⚙️ TANWEER STORE - Admin Control Panel\n\n"
        f"📊 Payment Analytics:\n"
        f"⏳ Pending Requests: {STATS['pending']}\n"
        f"✅ Approved Payments: {STATS['approved']}\n"
        f"❌ Rejected Payments: {STATS['rejected']}\n\n"
        f"👤 Current Support Username: @{CONFIG['support_username']}\n\n"
        "💬 Direct Msg Command:\n"
        "/send <ID or @username> <Message>\n\n"
        "Neeche diye gaye options se bot ko manage karein:"
    )
    
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Welcome Text", callback_data="admin_edit_welcome")],
        [InlineKeyboardButton("✏️ Edit Support Username", callback_data="admin_edit_support")],
        [InlineKeyboardButton("🖼️ Change ₹199 QR Code", callback_data="admin_qr_199")],
        [InlineKeyboardButton("🖼️ Change ₹98 QR Code", callback_data="admin_qr_98")],
        [InlineKeyboardButton("➕ Add New Button", callback_data="admin_add_btn")],
        [InlineKeyboardButton("🗑️ Delete Button", callback_data="admin_del_btn")],
        [InlineKeyboardButton("📋 View All Buttons & Links", callback_data="admin_view_btns")]
    ])
    
    if update.message:
        await update.message.reply_text(admin_text, reply_markup=admin_buttons)
    elif update.callback_query:
        await update.callback_query.message.edit_text(admin_text, reply_markup=admin_buttons)

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
        
        caption = f"🛒 {selected_item['name']}\n\n{selected_item['details']}\n\n-----------------------------------\n💳 Pay karke '✅ I have paid' button dabayein."
        
        pay_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I have paid", callback_data="paid")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="customer_back")]
        ])
        
        # Select appropriate QR code based on price type
        qr_to_send = QR_CONFIG["qr_199"] if selected_item.get("price_type") == "199" else QR_CONFIG["qr_98"]
        
        try:
            await query.message.reply_photo(photo=qr_to_send, caption=caption, reply_markup=pay_buttons)
        except Exception:
            await query.message.reply_text(caption, reply_markup=pay_buttons)

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
                text=f"🎉 Aapka payment Approve ho gaya hai!\n\nAapka Access Link ye raha:\n🔗 {delivery_link}"
            )
            await query.edit_message_caption(caption=query.message.caption + "\n\n✅ APPROVED BY ADMIN")
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
                text="❌ Aapka payment Reject kar diya gaya hai. Kripya sahi screenshot bhejein ya Support se contact karein."
            )
            await query.edit_message_caption(caption=query.message.caption + "\n\n❌ REJECTED BY ADMIN")
        except Exception as e:
            await query.message.reply_text(f"⚠️ Rejected! Par user ko message nahi bhej paaye: {str(e)}")

    elif data == "admin_view_btns":
        msg = "📋 Current Active Buttons & Links:\n\n"
        for idx, item in enumerate(DATA["items"], 1):
            msg += f"{idx}. {item['name']}\n📄 Details:\n{item['details']}\n🔗 Link: {item['link']}\n\n"
        await query.message.reply_text(msg)

    elif data == "admin_del_btn":
        keyboard = []
        for item in DATA["items"]:
            keyboard.append([InlineKeyboardButton(f"❌ Delete {item['name']}", callback_data=f"confirm_del_{item['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        await query.message.edit_text("Kis Button को Delete karna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("confirm_del_"):
        item_id = data.replace("confirm_del_", "")
        DATA["items"] = [item for item in DATA["items"] if item["id"] != item_id]
        await query.message.reply_text("✅ Button delete ho gaya!")
        await admin_panel(update, context)

    elif data == "admin_back":
        await admin_panel(update, context)

# ----------------- PHOTO HANDLER -----------------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = update.effective_user
    if user.username:
        USER_MAP[user.username.lower()] = user.id

    if context.user_data.get("waiting_for_qr_199") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr_199"] = False
        QR_CONFIG["qr_199"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ ₹199 wale pack ka naya QR Code set ho gaya!")
        await admin_panel(update, context)
        return

    if context.user_data.get("waiting_for_qr_98") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr_98"] = False
        QR_CONFIG["qr_98"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ ₹98 wale packs ka naya QR Code set ho gaya!")
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
            caption=f"📩 Naya Payment Screenshot aaya hai!\n\n👤 User: @{user.username or 'No Username'}\n🆔 User ID: {user.id}\n📦 Selected Item: {item_name}",
            reply_markup=admin_markup
        )

# ----------------- CONVERSATIONS -----------------
async def start_add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ Step 1: Naye Button ka Naam likhkar bhejein (jaise: 13. Pack 13 (₹98)):")
    return WAITING_BTN_NAME

async def get_btn_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["temp_btn_name"] = update.message.text
    await update.message.reply_text("🔗 Step 2: Access Link bhejein:")
    return WAITING_BTN_LINK

async def get_btn_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btn_name = context.user_data.get("temp_btn_name")
    btn_link = update.message.text
    
    new_item = {
        "id": f"btn_{len(DATA['items']) + 1}",
        "name": btn_name, 
        "details": DETAILS_98,  # New buttons will use ₹98 details by default
        "link": btn_link,
        "price_type": "98"
    }
    DATA["items"].append(new_item)
    
    await update.message.reply_text(f"✅ Naya button '{btn_name}' jod diya gaya!")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_edit_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📝 Naya Welcome Message likhkar bhejein:")
    return WAITING_WELCOME_TEXT

async def get_welcome_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DATA["welcome_text"] = update.message.text
    await update.message.reply_text("✅ Welcome Message update ho gaya!")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_edit_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ Naya Support Telegram Username lekhar bhejein (bina @ ke, jaise: BOTSUPPORTHELL):")
    return WAITING_SUPPORT_USER

async def get_support_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.replace("@", "").strip()
    CONFIG["support_username"] = username
    await update.message.reply_text(f"✅ Support Username change ho gaya: @{username}")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_change_qr_199(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_qr_199"] = True
    await query.message.reply_text("🖼️ ₹199 wale pack ke liye naya QR Code photo me bhejein:")

async def start_change_qr_98(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_qr_98"] = True
    await query.message.reply_text("🖼️ ₹98 wale packs ke liye naya QR Code photo me bhejein:")

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
    app.add_handler(CallbackQueryHandler(start_change_qr_199, pattern="^admin_qr_199$"))
    app.add_handler(CallbackQueryHandler(start_change_qr_98, pattern="^admin_qr_98$"))
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
