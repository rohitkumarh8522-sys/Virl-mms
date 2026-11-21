import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# =====================================================================
# ✏️ EASY EDIT SECTION: Welcome Message, 7 Buttons & Settings
# =====================================================================

WELCOME_MESSAGE = """𝗦𝗘𝗟𝗟𝗘𝗥 𝗜𝗗 :- @STARK_SELLER7

𝗣𝗥𝗢𝗢𝗙:- t.me/+QtunfHJIqyowMjg9

𝗗𝗘𝗠𝗢:- t.me/+AXcdDYSki31kMmM1"""

REPORT_USERNAME = "STARK_SELLER7"

# 7 Buttons Configuration (1 Combo ₹199 and 6 Packs ₹98)
BTN_1_NAME = "1. All Category Combo (₹199)"
BTN_1_LINK = "https://t.me/+ehTHId3ryhY3YmJl"

BTN_2_NAME = "2. Pack 2 (₹98)"
BTN_2_LINK = "https://t.me/+bPhyrYiSBQozNDBl"

BTN_3_NAME = "3. Pack 3 (₹98)"
BTN_3_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_4_NAME = "4. Pack 4 (₹98)"
BTN_4_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_5_NAME = "5. Pack 5 (₹98)"
BTN_5_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_6_NAME = "6. Pack 6 (₹98)"
BTN_6_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

BTN_7_NAME = "7. Pack 7 (₹98)"
BTN_7_LINK = "https://t.me/+b4HvE2hp_Cs2ZDBl"

# =====================================================================
# 🖼️ ENVIRONMENT MEDIA DEFAULTS (Render Env Vars Supported)
# Env Keys:
#   QR_IMAGE         -> 1 QR file_id or URL
#   QR_IS_VIDEO      -> "true" or "false"
#   WELCOME_VIDEOS   -> comma-separated video file_ids/URLs (5+ supported)
#   HOW_TO_USE_VIDEO -> 1 guide video file_id or URL
# =====================================================================

DEFAULT_QR = os.getenv(
    "QR_IMAGE",
    "https://raw.githubusercontent.com/telegram-bot-sdk/telegram-bot-sdk/main/tests/fixtures/image.jpg",
).strip() or "https://raw.githubusercontent.com/telegram-bot-sdk/telegram-bot-sdk/main/tests/fixtures/image.jpg"

DEFAULT_QR_IS_VIDEO = os.getenv("QR_IS_VIDEO", "false").strip().lower() in ("1", "true", "yes", "on")

_env_welcome_videos = os.getenv("WELCOME_VIDEOS", "")
WELCOME_VIDEOS = [v.strip() for v in _env_welcome_videos.split(",") if v.strip()]

_env_how_to = os.getenv("HOW_TO_USE_VIDEO", "").strip()
HOW_TO_USE_VIDEO = _env_how_to if _env_how_to else None

DATA_FILE = "bot_data.json"

# =====================================================================
# ⚙️ SYSTEM CONFIGURATIONS
# =====================================================================

TOKEN = os.getenv("BOT_TOKEN")
_raw_admin = os.getenv("ADMIN_ID", "0").strip()
ADMIN_ID = int(_raw_admin) if _raw_admin.isdigit() else 0
PORT = int(os.environ.get("PORT", 10000))

RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"https://{RENDER_HOST}" if RENDER_HOST else None)

STATS = {"pending": 0, "approved": 0, "rejected": 0}
UNIQUE_USERS = set()
USER_MAP = {}
CONFIG = {
    "report_username": REPORT_USERNAME,
}

MEDIA_CONFIG = {
    "welcome_videos": list(WELCOME_VIDEOS),
    "how_to_use_video": HOW_TO_USE_VIDEO,
}

QR_IMAGE = DEFAULT_QR
QR_IS_VIDEO = DEFAULT_QR_IS_VIDEO

DETAILS_199 = (
    "━━━━━━━━━━━━━━━━━━━\n"
    "💎 PAYMENT INVOICE - ₹199\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "💰 Price: ₹199\n"
    "📌 Step 1: Scan QR and pay exact amount.\n"
    "📌 Step 2: Tap “I HAVE PAID” below.\n"
    "📌 Step 3: Send your payment screenshot.\n\n"
    "🔐 Instant delivery after manual verification.\n"
    "🎁 Lifetime Access | No Extra Charges"
)

DETAILS_98 = (
    "━━━━━━━━━━━━━━━━━━━\n"
    "💎 PAYMENT INVOICE - ₹98\n"
    "━━━━━━━━━━━━━━━━━━━\n\n"
    "💰 Price: ₹98\n"
    "📌 Step 1: Scan QR and pay exact amount.\n"
    "📌 Step 2: Tap “I HAVE PAID” below.\n"
    "📌 Step 3: Send your payment screenshot.\n\n"
    "🔐 Instant delivery after manual verification.\n"
    "🎁 Lifetime Access | No Extra Charges"
)

DATA = {
    "welcome_text": WELCOME_MESSAGE,
    "items": [
        {"id": "btn_1", "name": BTN_1_NAME, "details": DETAILS_199, "link": BTN_1_LINK, "price_type": "199"},
        {"id": "btn_2", "name": BTN_2_NAME, "details": DETAILS_98, "link": BTN_2_LINK, "price_type": "98"},
        {"id": "btn_3", "name": BTN_3_NAME, "details": DETAILS_98, "link": BTN_3_LINK, "price_type": "98"},
        {"id": "btn_4", "name": BTN_4_NAME, "details": DETAILS_98, "link": BTN_4_LINK, "price_type": "98"},
        {"id": "btn_5", "name": BTN_5_NAME, "details": DETAILS_98, "link": BTN_5_LINK, "price_type": "98"},
        {"id": "btn_6", "name": BTN_6_NAME, "details": DETAILS_98, "link": BTN_6_LINK, "price_type": "98"},
        {"id": "btn_7", "name": BTN_7_NAME, "details": DETAILS_98, "link": BTN_7_LINK, "price_type": "98"},
    ],
}


def save_persistent_data():
    payload = {
        "welcome_text": DATA.get("welcome_text", WELCOME_MESSAGE),
        "deleted_item_ids": [
            item_id
            for item_id in ["btn_1", "btn_2", "btn_3", "btn_4", "btn_5", "btn_6", "btn_7"]
            if all(existing["id"] != item_id for existing in DATA.get("items", []))
        ],
        "report_username": CONFIG.get("report_username", REPORT_USERNAME),
        "welcome_videos": list(MEDIA_CONFIG.get("welcome_videos", [])),
        "how_to_use_video": MEDIA_CONFIG.get("how_to_use_video"),
        "qr_image": QR_IMAGE,
        "qr_is_video": QR_IS_VIDEO,
        "stats": dict(STATS),
        "unique_users": list(UNIQUE_USERS),
        "user_map": dict(USER_MAP),
    }
    try:
        tmp_file = f"{DATA_FILE}.tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp_file, DATA_FILE)
    except Exception as e:
        print("Error saving persistent data:", e)


def load_persistent_data():
    global QR_IMAGE, QR_IS_VIDEO
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if not isinstance(payload, dict):
            return

        if payload.get("welcome_text"):
            DATA["welcome_text"] = payload["welcome_text"]

        deleted_ids = set(payload.get("deleted_item_ids", []))
        if deleted_ids:
            DATA["items"] = [item for item in DATA["items"] if item["id"] not in deleted_ids]

        if payload.get("report_username"):
            CONFIG["report_username"] = payload["report_username"]

        if not WELCOME_VIDEOS and isinstance(payload.get("welcome_videos"), list) and payload["welcome_videos"]:
            MEDIA_CONFIG["welcome_videos"] = list(payload["welcome_videos"])

        if not HOW_TO_USE_VIDEO and payload.get("how_to_use_video"):
            MEDIA_CONFIG["how_to_use_video"] = payload["how_to_use_video"]

        if not os.getenv("QR_IMAGE") and payload.get("qr_image"):
            QR_IMAGE = payload["qr_image"]
            QR_IS_VIDEO = bool(payload.get("qr_is_video", False))

        if isinstance(payload.get("stats"), dict):
            STATS.update({
                "pending": int(payload["stats"].get("pending", 0)),
                "approved": int(payload["stats"].get("approved", 0)),
                "rejected": int(payload["stats"].get("rejected", 0)),
            })

        if isinstance(payload.get("unique_users"), list):
            UNIQUE_USERS.update(int(u) for u in payload["unique_users"])

        if isinstance(payload.get("user_map"), dict):
            USER_MAP.update(payload["user_map"])
    except Exception as e:
        print("Error loading persistent data:", e)


load_persistent_data()

WAITING_WELCOME_TEXT, WAITING_REPORT_USER = range(2)


def reset_admin_media_flags(context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_welcome_video"] = False
    context.user_data["waiting_for_how_to_video"] = False
    context.user_data["waiting_for_qr"] = False


def get_main_menu_markup():
    keyboard = []
    for item in DATA["items"]:
        keyboard.append([InlineKeyboardButton(item["name"], callback_data=f"select_{item['id']}")])

    keyboard.append([
        InlineKeyboardButton("📌 How to Use", callback_data="how_to_use"),
        InlineKeyboardButton("🚨 Report Issue", callback_data="report_issue"),
    ])

    return InlineKeyboardMarkup(keyboard)


def get_admin_panel_view():
    total_users = len(UNIQUE_USERS)
    approved_orders = STATS["approved"]
    pending_orders = STATS["pending"]
    rejected_orders = STATS["rejected"]
    how_to_status = "Uploaded ✅" if MEDIA_CONFIG["how_to_use_video"] else "Not Uploaded ❌"

    panel_text = (
        "👑 ADMIN & OWNER CONTROL PANEL 👑\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Total Users: {total_users}\n"
        f"✅ Approved Orders: {approved_orders}\n"
        f"⏳ Pending Requests: {pending_orders}\n"
        f"❌ Rejected Requests: {rejected_orders}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚨 Report Username: @{CONFIG['report_username']}\n"
        f"🎬 Welcome Videos: {len(MEDIA_CONFIG['welcome_videos'])}\n"
        f"🎥 How to Use Video: {how_to_status}\n\n"
        "💬 Direct Message: /send <User_ID or @username> <Message>"
    )

    panel_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ Edit Welcome Text", callback_data="admin_edit_welcome")],
        [InlineKeyboardButton("🎬 Add Welcome Video", callback_data="admin_add_video")],
        [InlineKeyboardButton("🎥 Add/Change How to Use Video", callback_data="admin_how_to_video")],
        [InlineKeyboardButton("🗑️ Clear Welcome Videos", callback_data="admin_clear_videos")],
        [InlineKeyboardButton("🖼️ Change Payment QR Code", callback_data="admin_change_qr")],
        [InlineKeyboardButton("✏️ Edit Report Username", callback_data="admin_edit_users")],
        [InlineKeyboardButton("🗑️ Delete Pack Button", callback_data="admin_del_btn")],
        [InlineKeyboardButton("🔄 Refresh Panel", callback_data="admin_refresh")],
    ])
    return panel_text, panel_keyboard


async def send_welcome_media_album(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    videos = MEDIA_CONFIG["welcome_videos"]
    if not videos:
        return
    for i in range(0, len(videos), 10):
        chunk = videos[i : i + 10]
        try:
            if len(chunk) == 1:
                await context.bot.send_video(chat_id=chat_id, video=chunk[0])
            else:
                media_group = [InputMediaVideo(media=vid) for vid in chunk]
                await context.bot.send_media_group(chat_id=chat_id, media=media_group)
        except Exception:
            pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, send_welcome_videos: bool = True):
    user = update.effective_user
    if user:
        UNIQUE_USERS.add(user.id)
        if user.username:
            USER_MAP[user.username.lower()] = user.id

    chat_id = update.effective_chat.id

    if send_welcome_videos:
        await send_welcome_media_album(chat_id, context)

    welcome_msg = DATA.get("welcome_text")
    reply_markup = get_main_menu_markup()

    if update.message:
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup)
    elif update.callback_query:
        try:
            if update.callback_query.message.photo or update.callback_query.message.video:
                await update.callback_query.message.delete()
                await context.bot.send_message(chat_id=chat_id, text=welcome_msg, reply_markup=reply_markup)
            else:
                await update.callback_query.message.edit_text(welcome_msg, reply_markup=reply_markup)
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text=welcome_msg, reply_markup=reply_markup)


async def send_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id != ADMIN_ID:
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text("⚠️ Format: /send <User_ID ya @username> <Message>")
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
    user = update.effective_user
    if not user:
        return

    if ADMIN_ID == 0:
        if update.message:
            await update.message.reply_text("⚠️ Render me ADMIN_ID set nahi hai. Environment me ADMIN_ID set karein.")
        return

    if user.id != ADMIN_ID:
        if update.message:
            await update.message.reply_text("❌ Access Denied.")
        elif update.callback_query:
            await update.callback_query.answer("❌ Access Denied.", show_alert=True)
        return

    reset_admin_media_flags(context)
    panel_text, panel_keyboard = get_admin_panel_view()

    if update.message:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=panel_text,
            reply_markup=panel_keyboard,
        )
    elif update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat_id
        try:
            if query.message.photo or query.message.video:
                await query.message.delete()
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=panel_text,
                    reply_markup=panel_keyboard,
                )
            else:
                await query.message.edit_text(
                    panel_text,
                    reply_markup=panel_keyboard,
                )
        except Exception:
            await context.bot.send_message(
                chat_id=chat_id,
                text=panel_text,
                reply_markup=panel_keyboard,
            )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if data in ("admin_refresh", "admin_back"):
        await admin_panel(update, context)
        return

    if data.startswith("select_"):
        item_id = data.replace("select_", "")
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)

        if not selected_item:
            await context.bot.send_message(chat_id=chat_id, text="❌ Ye option abhi uplabdha nahi hai.")
            return

        context.user_data["selected_item_id"] = item_id

        text = f"🛒 {selected_item['name']}\n\nSelect your preferred payment method below:"

        method_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇮🇳 UPI Payment", callback_data=f"pay_upi_{item_id}")],
            [InlineKeyboardButton("💎 Crypto Payment", callback_data=f"pay_crypto_{item_id}")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="customer_back")],
        ])

        try:
            if query.message.photo or query.message.video:
                await query.message.delete()
                await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=method_keyboard)
            else:
                await query.message.edit_text(text, reply_markup=method_keyboard)
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=method_keyboard)

    elif data.startswith("pay_upi_"):
        item_id = data.replace("pay_upi_", "")
        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)

        if not selected_item:
            return

        context.user_data["selected_item_id"] = item_id
        caption = f"🛒 {selected_item['name']}\n\n{selected_item['details']}"

        pay_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I Have Paid", callback_data="paid")],
            [InlineKeyboardButton("🔙 Back", callback_data=f"select_{item_id}")],
        ])

        try:
            await query.message.delete()
            if QR_IS_VIDEO:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=QR_IMAGE,
                    caption=caption,
                    reply_markup=pay_buttons,
                )
            else:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=QR_IMAGE,
                    caption=caption,
                    reply_markup=pay_buttons,
                )
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text=caption, reply_markup=pay_buttons)

    elif data.startswith("pay_crypto_"):
        item_id = data.replace("pay_crypto_", "")
        text = "💎 Crypto payment filhal available nahi hai. Kripya 🇮🇳 UPI Payment ka upyog karein."
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=f"select_{item_id}")]])
        try:
            await query.message.edit_text(text, reply_markup=back_kb)
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=back_kb)

    elif data == "how_to_use":
        vid = MEDIA_CONFIG.get("how_to_use_video")

        try:
            try:
                await query.message.delete()
            except Exception:
                pass

            back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="customer_back")]])

            if vid:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=vid,
                    caption="📌 How to Use / Guide Video",
                    reply_markup=back_kb,
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="⚠️ 'How to Use' video abhi set nahi kiya gaya hai.",
                    reply_markup=back_kb,
                )
        except Exception as e:
            print("Error sending how to use video:", e)

    elif data == "report_issue":
        rep_user = CONFIG.get("report_username", REPORT_USERNAME)
        text = (
            "🚨 Report an Issue\n\n"
            "Agar aapko koi samasya aa rahi hai ya payment verification mein deri ho rahi hai, "
            f"toh turant hamare support se contact karein:\n\n👉 @{rep_user}"
        )
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Menu", callback_data="customer_back")]])
        try:
            if query.message.photo or query.message.video:
                await query.message.delete()
                await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=back_kb)
            else:
                await query.message.edit_text(text, reply_markup=back_kb)
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=back_kb)

    elif data == "paid":
        context.user_data["waiting_for_proof"] = True
        await context.bot.send_message(chat_id=chat_id, text="📸 Kripya apne payment ka Screenshot yahan bhejein:")

    elif data == "customer_back":
        await start(update, context, send_welcome_videos=False)

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
        save_persistent_data()

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"🎉 Aapka payment Approve ho gaya hai!\n\nAapka Access Link ye raha:\n🔗 {delivery_link}",
            )
            await query.edit_message_caption(
                caption=(query.message.caption or "")
                + "\n\n━━━━━━━━━━━━━━━━━━━\n✅ STATUS: APPROVED BY ADMIN\n━━━━━━━━━━━━━━━━━━━"
            )
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Approved! Par user ko message nahi bhej paaye: {str(e)}")

    elif data.startswith("reject:"):
        payload = data.replace("reject:", "")
        user_id = int(payload)

        if STATS["pending"] > 0:
            STATS["pending"] -= 1
        STATS["rejected"] += 1
        save_persistent_data()

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Aapka payment Reject kar diya gaya hai. Kripya sahi screenshot bhejein ya Support se contact karein.",
            )
            await query.edit_message_caption(
                caption=(query.message.caption or "")
                + "\n\n━━━━━━━━━━━━━━━━━━━\n❌ STATUS: REJECTED BY ADMIN\n━━━━━━━━━━━━━━━━━━━"
            )
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Rejected! Par user ko message nahi bhej paaye: {str(e)}")

    elif data == "admin_clear_videos":
        if query.from_user.id != ADMIN_ID:
            return
        MEDIA_CONFIG["welcome_videos"] = []
        save_persistent_data()
        await context.bot.send_message(chat_id=chat_id, text="✅ Sabhi welcome videos hata diye gaye hain!")
        await admin_panel(update, context)

    elif data == "admin_del_btn":
        if query.from_user.id != ADMIN_ID:
            return
        keyboard = []
        for item in DATA["items"]:
            keyboard.append([InlineKeyboardButton(f"❌ Delete {item['name']}", callback_data=f"confirm_del_{item['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_back")])
        try:
            await query.message.edit_text("Kis Button ko Delete karna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            await context.bot.send_message(chat_id=chat_id, text="Kis Button ko Delete karna chahte hain?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("confirm_del_"):
        if query.from_user.id != ADMIN_ID:
            return
        item_id = data.replace("confirm_del_", "")
        DATA["items"] = [item for item in DATA["items"] if item["id"] != item_id]
        save_persistent_data()
        await context.bot.send_message(chat_id=chat_id, text="✅ Button delete ho gaya!")
        await admin_panel(update, context)


async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        UNIQUE_USERS.add(user.id)
        if user.username:
            USER_MAP[user.username.lower()] = user.id

    user_id = user.id if user else None

    if user_id == ADMIN_ID and context.user_data.get("waiting_for_welcome_video"):
        if update.message.video:
            file_id = update.message.video.file_id
            MEDIA_CONFIG["welcome_videos"].append(file_id)
            save_persistent_data()
            await update.message.reply_text(
                f"✅ Welcome video add ho gaya! Total Welcome Videos: {len(MEDIA_CONFIG['welcome_videos'])}\n"
                f"File ID: {file_id}\n\n"
                "Aur welcome video bhejna ho toh bhejein, ya /owner dabayein."
            )
        else:
            await update.message.reply_text("⚠️ Welcome video ke liye kripya video file bhejein.")
        return

    if user_id == ADMIN_ID and context.user_data.get("waiting_for_how_to_video"):
        if update.message.video:
            file_id = update.message.video.file_id
            MEDIA_CONFIG["how_to_use_video"] = file_id
            reset_admin_media_flags(context)
            save_persistent_data()
            await update.message.reply_text(
                f"✅ 'How to Use' video successfully set ho gaya!\nFile ID: {file_id}"
            )
            await admin_panel(update, context)
        else:
            await update.message.reply_text("⚠️ 'How to Use' ke liye kripya video file bhejein.")
        return

    if user_id == ADMIN_ID and context.user_data.get("waiting_for_qr"):
        global QR_IMAGE, QR_IS_VIDEO
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            QR_IMAGE = file_id
            QR_IS_VIDEO = False
            reset_admin_media_flags(context)
            save_persistent_data()
            await update.message.reply_text(
                f"✅ Naya Payment QR Code (Photo) set ho gaya!\nFile ID: {file_id}"
            )
            await admin_panel(update, context)
        elif update.message.video:
            file_id = update.message.video.file_id
            QR_IMAGE = file_id
            QR_IS_VIDEO = True
            reset_admin_media_flags(context)
            save_persistent_data()
            await update.message.reply_text(
                f"✅ Naya Payment QR Code (Video) set ho gaya!\nFile ID: {file_id}"
            )
            await admin_panel(update, context)
        else:
            await update.message.reply_text("⚠️ QR ke liye photo ya video bhejein.")
        return

    if context.user_data.get("waiting_for_proof") and update.message.photo:
        item_id = context.user_data.get("selected_item_id")
        photo_id = update.message.photo[-1].file_id

        selected_item = next((item for item in DATA["items"] if item["id"] == item_id), None)
        item_name = selected_item["name"] if selected_item else "Unknown Item"

        context.user_data["waiting_for_proof"] = False
        STATS["pending"] += 1
        save_persistent_data()

        await update.message.reply_text("⏳ Aapka screenshot admin ko bhej diya gaya hai. Verification ke baad link mil jayega.")

        admin_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user.id}:{item_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{user.id}"),
            ]
        ])

        proof_caption = (
            "📥 NEW PAYMENT PROOF RECEIVED\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Customer: @{user.username or 'No Username'}\n"
            f"🆔 User ID: {user.id}\n"
            f"📦 Selected Pack: {item_name}\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "👇 Review payment screenshot below and take action:"
        )

        if ADMIN_ID:
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=photo_id,
                caption=proof_caption,
                reply_markup=admin_markup,
            )


async def start_edit_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return ConversationHandler.END
    reset_admin_media_flags(context)
    await context.bot.send_message(chat_id=query.message.chat_id, text="📝 Naya Welcome Message text likhkar bhejein:")
    return WAITING_WELCOME_TEXT


async def get_welcome_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    DATA["welcome_text"] = update.message.text
    save_persistent_data()
    await update.message.reply_text("✅ Welcome Message update ho gaya!")
    await admin_panel(update, context)
    return ConversationHandler.END


async def start_add_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return
    reset_admin_media_flags(context)
    context.user_data["waiting_for_welcome_video"] = True
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="🎬 Welcome videos bhejein (5 ya usse zyada bhi add kar sakte hain):",
    )


async def start_how_to_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return
    reset_admin_media_flags(context)
    context.user_data["waiting_for_how_to_video"] = True
    await context.bot.send_message(chat_id=query.message.chat_id, text="🎥 'How to Use' ke liye apna guide video bhejein:")


async def start_change_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return
    reset_admin_media_flags(context)
    context.user_data["waiting_for_qr"] = True
    await context.bot.send_message(chat_id=query.message.chat_id, text="🖼️ Naya Payment QR Code (Photo ya Video) bhejein:")


async def start_edit_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return ConversationHandler.END
    reset_admin_media_flags(context)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="✏️ Naya Report Issue Username bhejein (bina @ ke, jaise: STARK_SELLER7):",
    )
    return WAITING_REPORT_USER


async def get_report_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uname = update.message.text.replace("@", "").strip()
    CONFIG["report_username"] = uname
    save_persistent_data()
    await update.message.reply_text(f"✅ Report username update ho gaya: @{uname}")
    await admin_panel(update, context)
    return ConversationHandler.END


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable set nahi hai!")

    app = ApplicationBuilder().token(TOKEN).build()

    edit_welcome_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_edit_welcome, pattern="^admin_edit_welcome$")],
        states={
            WAITING_WELCOME_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_welcome_text)],
        },
        fallbacks=[],
    )

    edit_users_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_edit_users, pattern="^admin_edit_users$")],
        states={
            WAITING_REPORT_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_report_user)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("owner", admin_panel))
    app.add_handler(CommandHandler("send", send_user_message))

    app.add_handler(edit_welcome_conv)
    app.add_handler(edit_users_conv)

    app.add_handler(CallbackQueryHandler(start_add_video, pattern="^admin_add_video$"))
    app.add_handler(CallbackQueryHandler(start_how_to_video, pattern="^admin_how_to_video$"))
    app.add_handler(CallbackQueryHandler(start_change_qr, pattern="^admin_change_qr$"))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO | filters.TEXT) & ~filters.COMMAND, handle_media))

    print(f"Starting webhook on port {PORT} with URL {WEBHOOK_URL} | ADMIN_ID={ADMIN_ID}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
        bootstrap_retries=3,
    )


if __name__ == "__main__":
    main()
