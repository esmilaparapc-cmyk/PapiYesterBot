from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image
import io

# ---------------- CONFIG ----------------
TOKEN = "8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE"
ADMIN_USERNAME = "Papi Yester prømø 🥷 👅"

VIDEOS = {
    "video1": {
        "youtube": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM",
        "password": "123YESTERDFC",
        "instructions": """Ey, bro/mami 👀🙏
Si quieres descargar el video viral 🔥:
1️⃣ Dale like al video 👍
2️⃣ Suscríbete 💎
3️⃣ (Opcional) deja un comentario ✍️
4️⃣ Mándame captura 📸 de que lo hiciste
Y te mando el link de Mega sin contraseña 💾✨

Mira el video aquí 👇
"""
    },
    "video2": {
        "youtube": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/file/PElVRahY#A2lXWSmVEbFw6TAMnATqMSHuYdOTB53-YWONsMqn0X4",
        "password": None,
        "instructions": """Ey, bro/mami 👀🙏
Si quieres descargar el video viral 🔥:
1️⃣ Dale like al video 👍
2️⃣ Suscríbete 💎
3️⃣ (Opcional) deja un comentario ✍️
4️⃣ Mándame captura 📸 de que lo hiciste
Eso no te tomará ni 10 segundos ☺️
Y no te olvides de seguir el canal para llegar ª mas contactos 😇
Mira el video aquí 👇
"""
    },
    "video3": {
        "youtube": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/collection/3NEW2TYA#jwKl6r2C1Ljid4QFDQg6zA",
        "password": None,
        "instructions": """🎬✨ PARA OBTENER EL VIDEO 🎥💫
📌 SÍGA LOS PASOS 👣👇:
AGRÉGAME, si no me agrega no paso 🙅🏽‍♂️
👀 SÍGUEME AQUI 👇👇

🔗 https://www.facebook.com/share/1FDuFq3pJe/?mibextid=wwXIfr
🌟 & AQUI 👇👇

🔗 https://www.instagram.com/yesther_smith_xl?igsh=Z2Y4b2R5amNjb2Jh&utm_source=qr

❌ SI NO TIENES FACEBOOK O IG, SÍGAME AQUI 👇👇

🔗 www.tiktok.com/@papi_yester_dfc

📸 MANDA CAPTURE SI NO NO PASO ❌🚫💥
😎 SI ME DEJAS DE SEGUIR 🤨 TENGO BOTS PARA ESO 🤖⚡💣
⚠️ LO QUE PASARÁ 📲 ES QUE SU NÚMERO SERÁ ENVIADO AUTOMÁTICAMENTE A 2 BOTS QUE TE MANDARÁN AUTOMÁTICAMENTE PARA SOPORTE
"""
    }
}

# Usuarios que enviaron captura
pending_captures = {}  # username: video_key

# ---------------- FUNCIONES ----------------
def get_image_type(image_bytes):
    """Detecta tipo de imagen usando Pillow"""
    with Image.open(io.BytesIO(image_bytes)) as img:
        return img.format.lower()


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Hola {update.effective_user.first_name} 😎\n"
        "Mándame una captura 📸 del video que cumpliste para que te envíe el link 🔗."
    )


def handle_photo(update: Update, context: CallbackContext):
    username = update.effective_user.username
    if not username:
        update.message.reply_text("Debes tener un @username para usar el bot.")
        return

    photo_file = update.message.photo[-1].get_file()
    photo_bytes = photo_file.download_as_bytearray()
    img_type = get_image_type(photo_bytes)

    pending_captures[username] = None  # Esperando tu revisión
    update.message.reply_text(
        f"Gracias {username}! 🥷\n"
        f"Esperando que {ADMIN_USERNAME} revise tu captura. Por favor, sé paciente hay mucha gente 📸⏳"
    )


def approve_capture(username: str, video_key: str, context: CallbackContext):
    """Llamar esta función manualmente cuando apruebes la captura"""
    if username in pending_captures:
        pending_captures[username] = video_key
        instructions = VIDEOS[video_key]["instructions"]
        youtube_link = VIDEOS[video_key]["youtube"]
        mega_link = VIDEOS[video_key]["mega"]
        password = VIDEOS[video_key]["password"]

        message = f"{instructions}\nYouTube: {youtube_link}\nMega: {mega_link}"
        if password:
            message += f"\n🔑 Contraseña: {password}"

        context.bot.send_message(
            chat_id=f"@{username}",
            text=message
        )


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Ah paj3r0 te atrapé 😏🔥\n"
        f"Para conseguir otro video pregúntale a {ADMIN_USERNAME} øwø Aqui 👉 https://wa.me/message/5RCSCBNHHGMUB1"
    )


# ---------------- INICIO BOT ----------------
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.photo, handle_photo))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown))

updater.start_polling()
updater.idle()