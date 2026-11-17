import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, ConversationHandler, filters, ContextTypes
)

# =====================================================================
# ✏️ EASY EDIT SECTION: 7 Buttons, Links & Settings
# =====================================================================

WELCOME_MESSAGE = """▪️𝐂𝐄𝐑𝐓𝐈𝐅𝐈𝐄𝐃 𝐒𝐇𝐎𝐏▪️

!!𝐍𝐄𝐖 𝐂𝐎𝐋𝐄𝐂𝐓𝐈𝐎𝐍!!

 ▪️𝐄𝐕𝐄𝐑𝐘 𝐂𝐀𝐓𝐄𝐆𝐎𝐑𝐘  𝐈𝐍𝐂𝐋𝐔𝐃𝐄𝐒 8 𝐆𝐑𝐎𝐔𝐏𝐒!!!

💥𝐁𝐔𝐘 𝐅𝐔𝐋𝐋 𝐏𝐀𝐂𝐊𝐀𝐆𝐄 𝐀𝐓 𝟏𝟗𝟗 𝐀𝐍𝐃 𝐆𝐄𝐓 𝟐𝟎𝟎+𝐃𝐀𝐈𝐋𝐘 𝐍𝐄𝐖 𝐔𝐏𝐋𝐎𝐀𝐃𝐄𝐃 𝐆𝐑𝐎𝐔𝐏𝐒

*𝐎𝐍𝐄 𝐓𝐈𝐌𝐄 𝙿𝙰𝚈𝙼𝙴𝙽𝚃 𝙿𝙴𝚁𝙼𝙴𝙽𝙴𝙽𝚃 𝙰𝙲𝙲𝙴𝚂𝚂*

𝐍𝐎 𝙴𝚇𝚃𝚁𝙰 𝙲𝙷𝙰𝚁𝙶𝙴
𝐍𝙾 𝙴𝚇𝙿𝙸𝚁𝙴𝙳 𝐋𝙸𝙽𝐊𝚂

*𝐃𝐀𝐈𝐋𝐘 𝐍𝐄𝐖 𝐕𝙸𝙳𝙴𝙾𝚂 𝐔𝙿𝙻𝙾𝙰𝐃𝙴𝙳✅

𝐃𝐄𝐌𝙾 𝐕𝙸𝙳𝙴𝙾𝚂 : https://t.me/+qIaukTR44z1hYTk9"""

DEFAULT_SUPPORT_USERNAME = "BOTSUPPORTHELL"
REPORT_USERNAME = "BOTSUPPORTHELL"
HOW_TO_USE_TEXT = "📌 **How to Use / Guide:**\n\n1. Select your preferred pack from the menu.\n2. Scan the QR code and complete the payment.\n3. Tap 'I have paid' and upload your payment screenshot.\n4. Admin will verify and send your access link instantly!"

# 7 Buttons Configuration (1 Combo ₹199 and 6 Packs ₹98)
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
CONFIG = {
    "support_username": DEFAULT_SUPPORT_USERNAME,
    "report_username": REPORT_USERNAME,
    "how_to_use": HOW_TO_USE_TEXT
}

MEDIA_CONFIG = {
    "welcome_videos": [] # List to store file_ids of welcome videos
}

QR_IMAGE = DEFAULT_QR

DETAILS_199 = (
    "━━━━━━━━━━━━━━━━━━━\n"
    "💎 **PAYMENT INVOICE - ₹199**\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "💰 **Price:** ₹199\n"
    "📌 **Step 1:** Scan QR and pay exact amount.\n"
    "📌 **Step 2:** Tap **“I HAVE PAID”** below.\n"
    "📌 **Step 3:** Send your payment screenshot.\n\n"
    "🔐 *Instant delivery after manual verification.*\n"
    "🎁 *Lifetime Access | No Extra Charges*"
)

DETAILS_98 = (
    "━━━━━━━━━━━━━━━━━━━\n"
    "💎 **PAYMENT INVOICE - ₹98**\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "💰 **Price:** ₹98\n"
    "📌 **Step 1:** Scan QR and pay exact amount.\n"
    "📌 **Step 2:** Tap **“I HAVE PAID”** below.\n"
    "📌 **Step 3:** Send your payment screenshot.\n\n"
    "🔐 *Instant delivery after manual verification.*\n"
    "🎁 *Lifetime Access | No Extra Charges*"
)

DATA = {
    "welcome_text": WELCOME_MESSAGE,
    "items": [
        {"id": "btn_1", "name": BTN_1_NAME, "details": DETAILS_199, "link": BTN_1_LINK, "price_type": "199"},
        {"id": "btn_2", "name": BTN_2_NAME, "details": DETAILS_98,  "link": BTN_2_LINK, "price_type": "98"},
        {"id": "btn_3", "name": BTN_3_NAME, "details": DETAILS_98,  "link": BTN_3_LINK, "price_type": "98"},
        {"id": "btn_4", "name": BTN_4_NAME, "details": DETAILS_98,  "link": BTN_4_LINK, "price_type": "98"},
        {"id": "btn_5", "name": BTN_5_NAME, "details": DETAILS_98,  "link": BTN_5_LINK, "price_type": "98"},
        {"id": "btn_6", "name": BTN_6_NAME, "details": DETAILS_98,  "link": BTN_6_LINK, "price_type": "98"},
        {"id": "btn_7", "name": BTN_7_NAME, "details": DETAILS_98,  "link": BTN_7_LINK, "price_type": "98"},
    ]
}

WAITING_WELCOME_TEXT, WAITING_SUPPORT_USER, WAITING_REPORT_USER, WAITING_HOW_TO = range(4)

def get_main_menu_markup():
    keyboard = []
    for item in DATA["items"]:
        keyboard.append([InlineKeyboardButton(item["name"], callback_data=f"select_{item['id']}")])
    
    # Extra 2 buttons: How to Use & Report Issue
    keyboard.append([
        InlineKeyboardButton("📌 How to Use", callback_data="how_to_use"),
        InlineKeyboardButton("🚨 Report Issue", callback_data="report_issue")
    ])
    
    support_user = CONFIG.get("support_username", DEFAULT_SUPPORT_USERNAME)
    keyboard.append([InlineKeyboardButton("💬 Support / Contact Admin", url=f"https://t.me/{support_user}")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        USER_MAP[user.username.lower()] = user.id

    chat_id = update.effective_chat.id
    
    # 1. Send welcome videos first if available
    for video_id in MEDIA_CONFIG["welcome_videos"]:
        try:
            await context.bot.send_video(chat_id=chat_id, video=video_id)
        except Exception:
            pass

    welcome_msg = DATA.get("welcome_text")
    reply_markup = get_main_menu_markup()
    
    if update.message:
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup)
    elif update.callback_query:
        try:
            if update.callback_query.message.photo:
                await update.callback_query.message.delete()
                await update.callback_query.message.reply_text(welcome_msg, reply_markup=reply_markup)
            else:
                await update.callback_query.message.edit_text(welcome_msg, reply_markup=reply_markup)
        except Exception:
            await update.callback_query.message.reply_text(welcome_msg, reply_markup=reply_markup)

async def send_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text("⚠️ Format: `/send <User_ID ya @username> <Message>`")
        return

    target = context.args[0].strip()
    msg_text = " ".join(context.args[1:])

    target_id = None
    if target.startswith("@"):
        uname = target.replace("@", "").lower()
        target_id = USER_MAP.get(uname)
    else:
        try:
            target_id = int(target)
        except ValueError:
            pass

    if target_id:
        try:
            await context.bot.send_message(chat_id=target_id, text=f"📩 Admin Message:\n\n{msg_text}")
            await update.message.reply_text("✅ Message bhej diya gaya!")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("❌ User nahi mila.")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    admin_text = (
        "⚙️ **TANWEER STORE - Admin Control Panel**\n\n"
        f"📊 **Analytics:**\n"
        f"⏳ Pending: {STATS['pending']} | ✅ Approved: {STATS['approved']} | ❌ Rejected: {STATS['rejected']}\n\n"
        f"👤 Support: @{CONFIG['support_username']} | 🚨 Report: @{CONFIG['report_username']}\n"
        f"🎬 Welcome Videos Uploaded: {len(MEDIA_CONFIG['welcome_videos'])}\n\n"
        "💬 Direct Msg: `/send <ID> <Message>`"
    )
    
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Welcome Text", callback_data="admin_edit_welcome")],
        [InlineKeyboardButton("🎬 Add Welcome Video", callback_data="admin_add_video")],
        [InlineKeyboardButton("🗑️ Clear All Welcome Videos", callback_data="admin_clear_videos")],
        [InlineKeyboardButton("🖼️ Change Payment QR Code", callback_data="admin_change_qr")],
        [InlineKeyboardButton("📌 Edit How to Use Text", callback_data="admin_edit_how_to")],
        [InlineKeyboardButton("✏️ Edit Support & Report User", callback_data="admin_edit_users")],
        [InlineKeyboardButton("🗑️ Delete Button", callback_data="admin_del_btn")]
    ])
    
    if update.message:
        await update.message.reply_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)
    elif update.callback_query:
        try:
            if update.callback_query.message.photo:
                await update.callback_query.message.delete()
                await update.callback_query.message.reply_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)
            else:
                await update.callback_query.message.edit_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)
        except Exception:
            await update.callback_query.message.reply_text(admin_text, parse_mode="Markdown", reply_markup=admin_buttons)

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
        
        text = f"🛒 *{selected_item['name']}*\n\nSelect your preferred payment method below:"
        
        method_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇮🇳 UPI Payment", callback_data=f"pay_upi_{item_id}")],
            [InlineKeyboardButton("💎 Crypto Payment", callback_data=f"pay_crypto_{item_id}")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="customer_back")]
        ])
        
        try:
            if query.message.photo:
                await query.message.delete()
                await query.message.reply_text(text, parse_mode="Markdown", reply_markup=method_keyboard)
            else:
                await query.message.edit_text(text, parse_mode="Markdown", reply_markup=method_keyboard)
        except Exception:
            await query.message.reply_text(text, parse_mode="Markdown", reply_markup=method_keyboard)

    elif data.startswith("pay_upi_"):
        item_id = data.replace("pay_upi_", "")
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        
        if not selected_item:
            return

        context.user_data["selected_item_id"] = item_id
        caption = f"🛒 *{selected_item['name']}*\n\n{selected_item['details']}"
        
        pay_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I Have Paid", callback_data="paid")],
            [InlineKeyboardButton("🔙 Back", callback_data=f"select_{item_id}")]
        ])
        
        try:
            await query.message.delete()
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=QR_IMAGE,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=pay_buttons
            )
        except Exception:
            await query.message.reply_text(caption, parse_mode="Markdown", reply_markup=pay_buttons)

    elif data.startswith("pay_crypto_"):
        item_id = data.replace("pay_crypto_", "")
        text = "💎 Crypto payment filhal available nahi hai. Kripya 🇮🇳 UPI Payment ka upyog karein."
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=f"select_{item_id}")]])
        try:
            await query.message.edit_text(text, reply_markup=back_kb)
        except Exception:
            await query.message.reply_text(text, reply_markup=back_kb)

    elif data == "how_to_use":
        text = CONFIG.get("how_to_use", HOW_TO_USE_TEXT)
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="customer_back")]])
        try:
            if query.message.photo:
                await query.message.delete()
                await query.message.reply_text(text, parse_mode="Markdown", reply_markup=back_kb)
            else:
                await query.message.edit_text(text, parse_mode="Markdown", reply_markup=back_kb)
        except Exception:
            await query.message.reply_text(text, parse_mode="Markdown", reply_markup=back_kb)

    elif data == "report_issue":
        rep_user = CONFIG.get("report_username", REPORT_USERNAME)
        text = f"🚨 **Report an Issue**\n\nAgar aapko koi samasya aa rahi hai ya payment verification mein deri ho rahi hai, toh turant hamare support se contact karein:\n\n👉 @{rep_user}"
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="customer_back")]])
        try:
            if query.message.photo:
                await query.message.delete()
                await query.message.reply_text(text, parse_mode="Markdown", reply_markup=back_kb)
            else:
                await query.message.edit_text(text, parse_mode="Markdown", reply_markup=back_kb)
        except Exception:
            await query.message.reply_text(text, parse_mode="Markdown", reply_markup=back_kb)

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
            await query.edit_message_caption(caption=query.message.caption + "\n\n━━━━━━━━━━━━━━━━━━━\n✅ **STATUS: APPROVED BY ADMIN**\n━━━━━━━━━━━━━━━━━━━")
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
            await query.edit_message_caption(caption=query.message.caption + "\n\n━━━━━━━━━━━━━━━━━━━\n❌ **STATUS: REJECTED BY ADMIN**\n━━━━━━━━━━━━━━━━━━━")
        except Exception as e:
            await query.message.reply_text(f"⚠️ Rejected! Par user ko message nahi bhej paaye: {str(e)}")

    elif data == "admin_clear_videos":
        MEDIA_CONFIG["welcome_videos"] = []
        await query.message.reply_text("✅ Sabhi welcome videos hata diye gaye hain!")
        await admin_panel(update, context)

    elif data == "admin_del_btn":
        keyboard = []
        for item in DATA["items"]:
            keyboard.append([InlineKeyboardButton(f"❌ Delete {item['name']}", callback_data=f"confirm_del_{item['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        try:
            await query.message.edit_text("Kis Button ko Delete karna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            await query.message.reply_text("Kis Button ko Delete karna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("confirm_del_"):
        item_id = data.replace("confirm_del_", "")
        DATA["items"] = [item for item in DATA["items"] if item["id"] != item_id]
        await query.message.reply_text("✅ Button delete ho gaya!")
        await admin_panel(update, context)

    elif data == "admin_back":
        await admin_panel(update, context)

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = update.effective_user
    if user.username:
        USER_MAP[user.username.lower()] = user.id

    # Admin uploading welcome video
    if context.user_data.get("waiting_for_welcome_video") and user_id == ADMIN_ID:
        if update.message.video:
            file_id = update.message.video.file_id
            MEDIA_CONFIG["welcome_videos"].append(file_id)
            await update.message.reply_text(f"✅ Video add ho gaya! Total welcome videos: {len(MEDIA_CONFIG['welcome_videos'])}\n\nAur video bhejna ho toh bhejein, ya /admin dabayein.")
        else:
            await update.message.reply_text("⚠️ Kripya valid video file hi bhejein.")
        return

    # Admin changing QR code
    if context.user_data.get("waiting_for_qr") and user_id == ADMIN_ID:
        context.user_data["waiting_for_qr"] = False
        global QR_IMAGE
        QR_IMAGE = update.message.photo[-1].file_id
        await update.message.reply_text("✅ Naya Payment QR Code successfully set ho gaya!")
        await admin_panel(update, context)
        return

    # User sending payment proof screenshot
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
        
        # Stylish formatted proof card for admin
        proof_caption = (
            "📥 **NEW PAYMENT PROOF RECEIVED**\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Customer:** @{user.username or 'No Username'}\n"
            f"🆔 **User ID:** `{user.id}`\n"
            f"📦 **Selected Pack:** {item_name}\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "👇 *Review payment screenshot below and take action:*"
        )
        
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=proof_caption,
            parse_mode="Markdown",
            reply_markup=admin_markup
        )

async def start_edit_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📝 Naya Welcome Message text likhkar bhejein:")
    return WAITING_WELCOME_TEXT

async def get_welcome_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DATA["welcome_text"] = update.message.text
    await update.message.reply_text("✅ Welcome Message update ho gaya!")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_add_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_welcome_video"] = True
    await query.message.reply_text("🎬 Welcome ke liye video bhejein (Aap ek-ek karke kai video bhej sakte hain):")

async def start_change_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_qr"] = True
    await query.message.reply_text("🖼️ Naya Payment QR Code photo format me bhejein:")

async def start_edit_how_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📌 Naya 'How to Use' text likhkar bhejein:")
    return WAITING_HOW_TO

async def get_how_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CONFIG["how_to_use"] = update.message.text
    await update.message.reply_text("✅ 'How to Use' text update ho gaya!")
    await admin_panel(update, context)
    return ConversationHandler.END

async def start_edit_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ Naya Report Issue Username bhejein (bina @ ke, jaise: BOTSUPPORTHELL):")
    return WAITING_REPORT_USER

async def get_report_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uname = update.message.text.replace("@", "").strip()
    CONFIG["report_username"] = uname
    CONFIG["support_username"] = uname
    await update.message.reply_text(f"✅ Support aur Report username update ho gaya: @{uname}")
    await admin_panel(update, context)
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    edit_welcome_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_edit_welcome, pattern="^admin_edit_welcome$")],
        states={
            WAITING_WELCOME_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_welcome_text)]
        },
        fallbacks=[]
    )

    edit_how_to_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_edit_how_to, pattern="^admin_edit_how_to$")],
        states={
            WAITING_HOW_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_how_to_text)]
        },
        fallbacks=[]
    )

    edit_users_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_edit_users, pattern="^admin_edit_users$")],
        states={
            WAITING_REPORT_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_report_user)]
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("send", send_user_message))
    
    app.add_handler(edit_welcome_conv)
    app.add_handler(edit_how_to_conv)
    app.add_handler(edit_users_conv)
    
    app.add_handler(CallbackQueryHandler(start_add_video, pattern="^admin_add_video$"))
    app.add_handler(CallbackQueryHandler(start_change_qr, pattern="^admin_change_qr$"))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))

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
