import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)

# =====================================================================
# ✏️ EASY EDIT SECTION: 12 Buttons, Links & UPI Settings
# =====================================================================

WELCOME_MESSAGE = """🕊️WELCOME TO TANWEER STORE🕊️

⚡NEW COLLECTION AVAILABLE⚡

EACH CATEGORY CONTAINS 4 GROUPS (1200-1800 VIDEOS PER GROUP)

🕊️PAYMENT PROOFS 👉 https://t.me/+hbere12UWTMzYTI1

💥DEMO VIDEOS 👉 https://t.me/+2jSY317AQww2ZjM9"""

DEFAULT_SUPPORT_USERNAME = "G_KlNG"

# Apni UPI ID yahan dalein
YOUR_UPI_ID = "roxxxx@axl"

# ---------------- 12 BUTTONS CONFIGURATION ----------------
BTN_1_NAME  = "1. All Category Combo (₹199)"
BTN_1_LINK  = "https://t.me/+ehTHId3ryhY3YmJl"
BTN_1_AMT   = 199

BTN_2_NAME  = "2. Pack 2 (₹98)"
BTN_2_LINK  = "https://t.me/+bPhyrYiSBQozNDBl"
BTN_2_AMT   = 98

BTN_3_NAME  = "3. Pack 3 (₹98)"
BTN_3_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_3_AMT   = 98

BTN_4_NAME  = "4. Pack 4 (₹98)"
BTN_4_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_4_AMT   = 98

BTN_5_NAME  = "5. Pack 5 (₹98)"
BTN_5_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_5_AMT   = 98

BTN_6_NAME  = "6. Pack 6 (₹98)"
BTN_6_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_6_AMT   = 98

BTN_7_NAME  = "7. Pack 7 (₹98)"
BTN_7_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_7_AMT   = 98

BTN_8_NAME  = "8. Pack 8 (₹98)"
BTN_8_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_8_AMT   = 98

BTN_9_NAME  = "9. Pack 9 (₹98)"
BTN_9_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_9_AMT   = 98

BTN_10_NAME = "10. Pack 10 (₹98)"
BTN_10_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_10_AMT  = 98

BTN_11_NAME = "11. Pack 11 (₹98)"
BTN_11_LINK  = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_11_AMT  = 98

BTN_12_NAME = "12. Pack 12 (₹98)"
BTN_12_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"
BTN_12_AMT  = 98

# =====================================================================
# ⚙️ SYSTEM CONFIGURATIONS
# =====================================================================

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))
PORT = int(os.environ.get("PORT", 10000))

RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"https://{RENDER_HOST}" if RENDER_HOST else None)

USER_MAP = {}
CONFIG = {"support_username": DEFAULT_SUPPORT_USERNAME}

DATA = {
    "welcome_text": WELCOME_MESSAGE,
    "items": [
        {"id": "btn_1",  "name": BTN_1_NAME,  "amount": BTN_1_AMT,  "link": BTN_1_LINK},
        {"id": "btn_2",  "name": BTN_2_NAME,  "amount": BTN_2_AMT,  "link": BTN_2_LINK},
        {"id": "btn_3",  "name": BTN_3_NAME,  "amount": BTN_3_AMT,  "link": BTN_3_LINK},
        {"id": "btn_4",  "name": BTN_4_NAME,  "amount": BTN_4_AMT,  "link": BTN_4_LINK},
        {"id": "btn_5",  "name": BTN_5_NAME,  "amount": BTN_5_AMT,  "link": BTN_5_LINK},
        {"id": "btn_6",  "name": BTN_6_NAME,  "amount": BTN_6_AMT,  "link": BTN_6_LINK},
        {"id": "btn_7",  "name": BTN_7_NAME,  "amount": BTN_7_AMT,  "link": BTN_7_LINK},
        {"id": "btn_8",  "name": BTN_8_NAME,  "amount": BTN_8_AMT,  "link": BTN_8_LINK},
        {"id": "btn_9",  "name": BTN_9_NAME,  "amount": BTN_9_AMT,  "link": BTN_9_LINK},
        {"id": "btn_10", "name": BTN_10_NAME, "amount": BTN_10_AMT, "link": BTN_10_LINK},
        {"id": "btn_11", "name": BTN_11_NAME, "amount": BTN_11_AMT, "link": BTN_11_LINK},
        {"id": "btn_12", "name": BTN_12_NAME, "amount": BTN_12_AMT, "link": BTN_12_LINK},
    ]
}

# ----------------- START COMMAND -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        USER_MAP[user.username.lower()] = user.id

    welcome_msg = DATA.get("welcome_text")
    
    keyboard = []
    for item in DATA["items"]:
        keyboard.append([InlineKeyboardButton(f"{item['name']} - ₹{item['amount']}", callback_data=f"select_{item['id']}")])
        
    support_user = CONFIG.get("support_username", DEFAULT_SUPPORT_USERNAME)
    keyboard.append([InlineKeyboardButton("💬 Support / Contact Admin", url=f"https://t.me/{support_user}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_msg, reply_markup=reply_markup)

# ----------------- CALLBACK HANDLER -----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Step 1: 12 buttons me se kisi par click karne par payment option dikhana
    if data.startswith("select_"):
        item_id = data.replace("select_", "")
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        
        if not selected_item:
            await query.message.reply_text("❌ Ye option abhi uplabdha nahi hai.")
            return
        
        text = f"*{selected_item['name']}*\n\nSelect your preferred payment method below:"
        
        method_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇮🇳 UPI Payment", callback_data=f"pay_upi_{item_id}")],
            [InlineKeyboardButton("💎 Crypto Payment", callback_data=f"pay_crypto_{item_id}")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_payment")]
        ])
        
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=method_keyboard)

    # Step 2: UPI Payment par click karne par turant QR Code aur Details generate karna
    elif data.startswith("pay_upi_"):
        item_id = data.replace("pay_upi_", "")
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        
        if not selected_item:
            return

        # UPI Intent aur QR Code URL banana (₹199 ya ₹98 ke hisab se)
        upi_intent = f"upi://pay?pa={YOUR_UPI_ID}&pn=TanweerStore&am={selected_item['amount']}&cu=INR"
        qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={upi_intent}"

        caption = (
            f"🛒 *{selected_item['name']}*\n\n"
            f"💰 *Amount:* ₹{selected_item['amount']}\n"
            f"💳 *UPI ID:* `{YOUR_UPI_ID}`\n\n"
            f"📲 **QR Code scan karein ya neeche diye gaye button se payment karein:**"
        )
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Pay Now (UPI App)", url=upi_intent)],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_payment")]
        ])
        
        try:
            await query.message.reply_photo(photo=qr_code_url, caption=caption, parse_mode="Markdown", reply_markup=buttons)
        except Exception:
            await query.message.reply_text(caption, parse_mode="Markdown", reply_markup=buttons)

    # Step 3: Crypto Payment Click
    elif data.startswith("pay_crypto_"):
        await query.message.reply_text("💎 Crypto payment filhal available nahi hai. Kripya 🇮🇳 UPI Payment ka upyog karein.")

    # Step 4: Cancel Button
    elif data == "cancel_payment":
        await query.message.reply_text("❌ Payment cancel kar di gayi hai.")
        try:
            await query.message.delete()
        except Exception:
            pass

# ----------------- ADMIN DIRECT MSG TO USER -----------------
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

# ----------------- ADMIN PANEL -----------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    admin_text = (
        "⚙️ TANWEER STORE - Admin Panel\n\n"
        f"👤 Support Username: @{CONFIG['support_username']}\n\n"
        "💬 Direct Msg Command:\n"
        "/send <ID or @username> <Message>"
    )
    
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Support Username", callback_data="admin_edit_support")]
    ])
    
    if update.message:
        await update.message.reply_text(admin_text, reply_markup=admin_buttons)
    elif update.callback_query:
        await update.callback_query.message.edit_text(admin_text, reply_markup=admin_buttons)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("send", send_user_message))
    app.add_handler(CallbackQueryHandler(button_handler))

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
