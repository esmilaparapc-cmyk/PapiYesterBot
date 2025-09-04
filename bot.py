import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters

# ⚡ Variables de entorno (configura en Render)
TOKEN = "8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE"
ADMIN_USERNAME = "PapiYester prømø 🥷 👅"

# Base de datos temporal en memoria para usuarios
user_data = {}

# Links de los videos
videos = {
    "video1": {
        "youtube": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM",
        "password": "123YESTERDFC",
        "instructions": "1️⃣ Dale like 👍\n2️⃣ Suscríbete 💎\n3️⃣ (Opcional) comenta ✍️\n4️⃣ Mándame captura 📸"
    },
    "video2": {
        "youtube": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/file/PElVRahY#A2lXWSmVEbFw6TAMnATqMSHuYdOTB53-YWONsMqn0X4",
        "password": "No tiene contraseña 🙅🏽‍♂️",
        "instructions": "1️⃣ Dale like 👍\n2️⃣ Suscríbete 💎\n3️⃣ (Opcional) comenta ✍️\n4️⃣ Mándame captura 📸\nEso no te tomará ni 10 segundos ☺️\nSigue el canal para más contactos 😇\nhttps://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13"
    },
    "video3": {
        "youtube": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/collection/3NEW2TYA#jwKl6r2C1Ljid4QFDQg6zA",
        "password": "No tiene contraseña 🙅🏽‍♂️",
        "instructions": "🎬✨ PARA OBTENER EL VIDEO 🎥💫\n📌 SÍGA LOS PASOS 👣\nAgrégame, si no me agrega no paso 🙅🏽‍♂️\nSÍGUEME AQUI 👇\nFacebook: https://www.facebook.com/share/1FDuFq3pJe/?mibextid=wwXIfr\nInstagram: https://www.instagram.com/yesther_smith_xl?igsh=Z2Y4b2R5amNjb2Jh&utm_source=qr\nTikTok: www.tiktok.com/@papi_yester_dfc\n📸 Manda capture si no no paso ❌🚫💥"
    }
}

# Comando /start
def start(update: Update, context: CallbackContext):
    username = update.effective_user.username
    user_data[username] = {"selected_video": None, "approved": False}
    update.message.reply_text(
        f"Ey @{username} 👀, envíame el capture del video que quieras ver y {ADMIN_USERNAME} lo revisará antes de darte el link 🔗."
    )

# Recepción de capture
def review_capture(update: Update, context: CallbackContext):
    username = update.effective_user.username
    if username not in user_data:
        user_data[username] = {"selected_video": None, "approved": False}

    # Si ya eligieron video y está aprobado
    if user_data[username]["approved"]:
        update.message.reply_text(
            f"Ah paj3r0 te atrapé 😏🔥\nPara conseguir otro video pregúntale a {ADMIN_USERNAME} aquí 👉 https://wa.me/message/5RCSCBNHHGMUB1 😎📸💥"
        )
        return

    # Guardamos temporalmente que mandó capture
    user_data[username]["approved"] = False
    update.message.reply_text(
        f"Gracias @{username} 😎, esperando que {ADMIN_USERNAME} 🥷 👅 revise tu capture. Paciencia 😉⏳"
    )

# Comando de administrador para aprobar video
def approve_video(update: Update, context: CallbackContext):
    if update.effective_user.username != ADMIN_USERNAME:
        update.message.reply_text("No tienes permiso para usar esto 😅")
        return

    args = context.args
    if len(args) != 2:
        update.message.reply_text("Uso: /approve <username> <video1|video2|video3>")
        return

    target_user, video_key = args
    if target_user in user_data and video_key in videos:
        user_data[target_user]["approved"] = True
        user_data[target_user]["selected_video"] = video_key
        video_info = videos[video_key]
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"@{target_user} ✅ Aprobado! Aquí está tu link 🔗:\nMega: {video_info['mega']}\nContraseña: {video_info['password']}\nYouTube: {video_info['youtube']}"
        )

# Handlers
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("approve", approve_video))
dispatcher.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, review_capture))

# Arranca el bot
updater.start_polling()
updater.idle()