from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Token del bot
TOKEN = "8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE"

# ID de administrador
ADMIN_ID = 7727617732  # Tu ID de Telegram

# Diccionario para aprobar videos
usuarios_pendientes = {}  # {username: "video1/video2/video3"}

# Mensajes de cada video
videos_info = {
    "video1": {
        "instrucciones": "Ey, bro/mami 👀🙏\nSi quieres descargar el video viral 🔥:\n1️⃣ Dale like al video 👍\n2️⃣ Suscríbete 💎\n3️⃣ (Opcional) deja un comentario ✍️\n4️⃣ Mándame captura 📸 de que lo hiciste\nY te mando el link de Mega sin contraseña 💾✨\n\nMira el video aquí 👇\nhttps://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM",
        "password": "123YESTERDFC"
    },
    "video2": {
        "instrucciones": "Ey, bro/mami 👀🙏\nSi quieres descargar el video de pajitaaa 🔥:\n1️⃣ Dale like al video 👍\n2️⃣ Suscríbete 💎\n3️⃣ (Opcional) deja un comentario ✍️\n4️⃣ Mándame captura 📸 de que lo hiciste\nEso no te tomará ni 10 segundos ☺️\nY no te olvides de seguir el canal para llegar ª mas contactos 😇\n\nMira el video aquí 👇\nhttps://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/file/PElVRahY#A2lXWSmVEbFw6TAMnATqMSHuYdOTB53-YWONsMqn0X4",
        "password": None
    },
    "video3": {
        "instrucciones": "🎬✨ PARA OBTENER EL VIDEO 🎥💫\n📌 SÍGA LOS PASOS 👣👇:\nAGRÉGAME, si no me agrega no paso 🙅🏽‍♂️\n👀 SÍGUEME AQUI 👇👇\n\n🔗 https://www.facebook.com/share/1FDuFq3pJe/?mibextid=wwXIfr\n🔗 https://www.instagram.com/yesther_smith_xl?igsh=Z2Y4b2R5amNjb2Jh&utm_source=qr\n❌ SI NO TIENES FACEBOOK O IG, SÍGAME AQUI 👇👇\n🔗 www.tiktok.com/@papi_yester_dfc\n📸 MANDA CAPTURE SI NO NO PASO ❌🚫💥\n😎 SI ME DEJAS DE SEGUIR 🤨 TENGO BOTS PARA ESO 🤖⚡💣\n⚠️ LO QUE PASARÁ 📲 ES QUE SU NÚMERO SERÁ ENVIADO AUTOMÁTICAMENTE A 2 BOTS QUE TE MANDARÁN AUTOMÁTICAMENTE PARA SOPORTE\n\nMira el video aquí 👇\nhttps://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE",
        "mega": "https://mega.nz/collection/3NEW2TYA#jwKl6r2C1Ljid4QFDQg6zA",
        "password": None
    }
}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hola 😎\nMándame captura del video que quieres y yo verificaré que cumplas los pasos antes de darte el link 🔥"
    )

def handle_capture(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    usuarios_pendientes[username] = "pendiente"
    update.message.reply_text(
        "📸 Gracias por enviar tu captura! Papi Yester prømø 🥷 👅 revisará y aprobará pronto. Paciencia 😎"
    )

def aprobar(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("❌ No tienes permisos para aprobar.")
        return

    if len(context.args) != 2:
        update.message.reply_text("Uso: /aprobar @username videoX")
        return

    username = context.args[0].replace("@", "")
    video = context.args[1]

    if username not in usuarios_pendientes:
        update.message.reply_text("Usuario no encontrado o no envió captura.")
        return

    if video not in videos_info:
        update.message.reply_text("Video no válido.")
        return

    info = videos_info[video]
    respuesta = f"🔥 Aquí tienes tu video {video} 🔥\nMega: {info['mega']}"
    if info['password']:
        respuesta += f"\nContraseña: {info['password']}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ Aprobado a @{username}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta)
    usuarios_pendientes.pop(username)

def otro_video(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Ah paj3r0 te atrapé 😏💥🔥\nPara conseguir otro video pregúntale a papi Yester prømø øwø Aqui 👉 https://wa.me/message/5RCSCBNHHGMUB1"
    )

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("aprobar", aprobar))
dp.add_handler(CommandHandler("otrovideo", otro_video))
dp.add_handler(MessageHandler(Filters.photo, handle_capture))

updater.start_polling()
updater.idle()