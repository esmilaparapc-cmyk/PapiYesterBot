import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7727617732  # tu ID de Telegram

VIDEO_LINKS = {
    "video1": {
        "yt": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "msg": (
            "📽️🔥 VIDEO VIRAL DISPONIBLE 🔥📽️\n"
            "1️⃣ Dale like 👍\n"
            "2️⃣ Suscríbete 💎\n"
            "3️⃣ (Opcional) deja un comentario ✍️\n"
            "4️⃣ Mándame captura 📸 de que lo hiciste\n\n"
            "Mira el video aquí 👇\n"
            "🔗 https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE\n"
            "Después te pasaré el link de descarga 💾✨"
        )
    },
    "video2": {
        "yt": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "msg": (
            "🍑💦 VIDEO DE PAJITAAA 💔\n"
            "1️⃣ Dale like 👍\n"
            "2️⃣ Suscríbete 💎\n"
            "3️⃣ (Opcional) deja un comentario ✍️\n"
            "4️⃣ Mándame captura 📸 de que lo hiciste\n"
            "Eso no te tomará ni 10 segundos ☺️\n"
            "No te olvides de seguir el canal 😇\n\n"
            "https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13"
        )
    },
    "video3": {
        "yt": "https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "msg": (
            "🎬✨ PARA OBTENER EL VIDEO 🎥💫\n"
            "📌 SÍGA LOS PASOS 👣👇:\n"
            "AGRÉGAME, si no me agrega no paso 🙅🏽‍♂️\n"
            "👀 SÍGUEME AQUI 👇👇\n"
            "🔗 https://www.facebook.com/share/1FDuFq3pJe/?mibextid=wwXIfr\n"
            "🌟 & AQUI 👇👇\n"
            "🔗 https://www.instagram.com/yesther_smith_xl?igsh=Z2Y4b2R5amNjb2Jh&utm_source=qr\n"
            "❌ SI NO TIENES FACEBOOK O IG, SÍGAME AQUI 👇👇\n"
            "🔗 www.tiktok.com/@papi_yester_dfc\n"
            "📸 MANDA CAPTURE SI NO NO PASO ❌🚫💥\n"
            "😎 SI ME DEJAS DE SEGUIR 🤨 TENGO BOTS PARA ESO 🤖⚡💣\n"
            "⚠️ LO QUE PASARÁ 📲 ES QUE SU NÚMERO SERÁ ENVIADO AUTOMÁTICAMENTE A 2 BOTS PARA SOPORTE"
        )
    }
}

pendientes = {}  # user_id: video_elegido

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Ey bro/mami 👀🙏\n"
        "Mándame captura del video que quieras y yo te aprobaré si todo está OK 😎\n"
        "Solo un video a la vez!"
    )

def capture(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    username = user.username or "sin_username"

    pendientes[user_id] = None  # todavía no sabemos qué video eligió

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📸 Capture recibido de @{username} (ID: {user_id})\n"
             f"Mira el capture y decide qué video darle"
    )

    if update.message.photo:
        context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id)
    elif update.message.document:
        context.bot.send_document(chat_id=ADMIN_ID, document=update.message.document.file_id)

    update.message.reply_text(
        "⏳ Esperando que Papi Yester prømø 🥷 👅 revise tu capture... Paciencia 🙏✨"
    )

def aprobar(update: Update, context: CallbackContext):
    args = context.args
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(args) < 2:
        update.message.reply_text("Uso: /aprobar <user_id> <video1|video2|video3>")
        return

    try:
        user_id = int(args[0])
        video = args[1].lower()
    except:
        update.message.reply_text("Error con los parámetros.")
        return

    if user_id not in pendientes:
        update.message.reply_text("Ese usuario no está pendiente.")
        return

    if video not in VIDEO_LINKS:
        update.message.reply_text("Video inválido.")
        return

    pendientes.pop(user_id)
    context.bot.send_message(chat_id=user_id, text=VIDEO_LINKS[video]["msg"])

    update.message.reply_text(f"✅ Video enviado a {user_id}")

def otro_video(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Ah paj3r0 😏 te atrapé 🤭\n"
        "Para conseguir otro video pregúntale a Papi Yester prømø øwø Aquí 👉 https://wa.me/message/5RCSCBNHHGMUB1\n"
        "🔥🚀✨👀💥😎💣"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("aprobar", aprobar))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, capture))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, otro_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()