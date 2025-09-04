import telebot
from telebot import types

# Token del bot
TOKEN = "8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE"
bot = telebot.TeleBot(TOKEN)

# Diccionario para controlar solicitudes
user_requests = {}

# Mensaje inicial
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"👋 Hola {message.from_user.first_name}!\nSoy el bot oficial de **Papi Yester prømø 🥷 👅**.\n\n📌 Manda tu capture del video que quieras y Papi Yester lo revisa.")

# Cuando manden una foto (capture)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    username = message.from_user.username or message.from_user.first_name
    user_id = message.from_user.id

    bot.reply_to(message, f"📸 Capture recibido de @{username}.\n⌛ Espera que **Papi Yester prømø 🥷 👅** lo revise.\n🙏 Sé paciente, hay mucha gente en la fila 😅🔥")

    # Guardamos la solicitud
    user_requests[user_id] = {"username": username, "status": "pending"}

# Admin (tú) aprueba manualmente con comandos
@bot.message_handler(commands=['video1'])
def approve_video1(message):
    if str(message.from_user.id) != "7727617732":
        return
    for user_id, data in user_requests.items():
        if data["status"] == "pending":
            bot.send_message(user_id, """📽️🔥 VIDEO VIRAL DISPONIBLE 🔥📽️
📥 DESCÁRGALO AQUI 👇👇
🔗 https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM
🔑 CONTRASEÑA: 👉 123YESTERDFC 🔐
🎥 Mira el video aquí 👇
https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE""")
            data["status"] = "approved"

@bot.message_handler(commands=['video2'])
def approve_video2(message):
    if str(message.from_user.id) != "7727617732":
        return
    for user_id, data in user_requests.items():
        if data["status"] == "pending":
            bot.send_message(user_id, """🍑💦 LOS VIDEOS PEGANDO CUERNOS 👴💔
📥 DESCARGA AQUI 👇👇
🔗 https://mega.nz/file/DE90AIoA#Me2o8ziI6il4I141OBJWIx6FHeb7Hgjbc0BVs8P0bzo
🔑 Contraseña: No tiene 🙅🏽‍♂️
🎥 Mira el video aquí 👇
https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE
Eso no te tomará ni 10 segundos ☺️
Y no te olvides de seguir el canal para llegar a más contactos 😇
https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13""")
            data["status"] = "approved"

@bot.message_handler(commands=['video3'])
def approve_video3(message):
    if str(message.from_user.id) != "7727617732":
        return
    for user_id, data in user_requests.items():
        if data["status"] == "pending":
            bot.send_message(user_id, """💻🔥 VIDEO "PC GRATIS"
📥 DESCARGA AQUI 👇👇
🔗 https://mega.nz/collection/3NEW2TYA#jwKl6r2C1Ljid4QFDQg6zA
🎥 Mira el video aquí 👇
https://youtu.be/H3P60ChH8bQ?si=o12zxApIOJ4jffnE
🎬✨ PARA OBTENER EL VIDEO 🎥💫
📌 SÍGA LOS PASOS 👣👇
📸 MANDA CAPTURE SI NO NO PASO ❌🚫💥
😎 SI ME DEJAS DE SEGUIR 🤨 TENGO BOTS PARA ESO 🤖⚡💣
⚠️ LO QUE PASARÁ 📲 ES QUE TU NÚMERO SERÁ ENVIADO AUTOMÁTICAMENTE A 2 BOTS PARA SOPORTE""")
            data["status"] = "approved"

# Si piden otro video después de uno aprobado
@bot.message_handler(commands=['otro'])
def otro_video(message):
    bot.reply_to(message, """😏 Ah paj3r0 te atrapé 🔥
Para conseguir otro video, pregúntale a **Papi Yester prømø øwø** aquí 👇👇
👉 https://wa.me/message/5RCSCBNHHGMUB1
🤣📸💎🚀🔥🥷👅""")

# Arrancar bot
bot.polling(none_stop=True)
