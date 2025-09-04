const TelegramBot = require('node-telegram-bot-api');

// Token del bot
const token = "8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE";

// Tu ID de Telegram (para recibir captures y notificaciones)
const adminId = 7727617732;

// Links oficiales
const youtubeLink = "https://youtube.com/@papiyesterdfc?si=7MjVrM2-OBUzlUo0";
const whatsappLink = "https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13";

// Videos
const videos = {
  1: "📽️🔥 VIDEO VIRAL DISPONIBLE 🔥📽️\n📥 DESCÁRGALO AQUI 👇👇\n🔗 https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM\n\n🔑 CONTRASEÑA: 👉 123YESTERDFC 🔐",
  2: "🍑💦 Los videos de pajitaaa pegándole cuernos al viejito 👴💔🔐\n📥 DESCARGA AQUI 👇👇\n🔗 https://mega.nz/file/PElVRahY#A2lXWSmVEbFw6TAMnATqMSHuYdOTB53-YWONsMqn0X4\n\n🔑 Contraseña: No tiene 🙅🏽‍♂️\n⚠️ SOLO LOS DUROS TIENEN ACCESO 🚀",
  3: "🔥 COLECCIÓN COMPLETA DISPONIBLE 🔥\n🔗 https://mega.nz/collection/SNNGDLaK#DHaQKN-aHiUobg3mK8wPxg\n\n🔑 Contraseña: Ninguna 😎"
};

// Inicializa el bot
const bot = new TelegramBot(token, { polling: true });

// Estado de los usuarios
const userRequests = {};

// Mensaje inicial cuando alguien pide un video
function requestVideo(chatId, username, videoNumber) {
  userRequests[chatId] = { video: videoNumber, captures: [], timer: null };

  bot.sendMessage(chatId, `🤖 Hola soy el BOT OFICIAL de los videos virales de *Papi Yester Prømø* 🥷👅\n\n` +
    `Aquí nadie se queda sin su contenido 🔥, pero primero tienes que **demostrar que eres real** 👀.\n\n` +
    `👉 Para desbloquear el *Video ${videoNumber}* haz lo siguiente:\n\n` +
    `1️⃣ Suscríbete al canal de YouTube 👉 ${youtubeLink}\n` +
    `2️⃣ Únete al canal de WhatsApp 👉 ${whatsappLink}\n` +
    `3️⃣ 📸 Mándame **2 captures obligatorios** (uno de YouTube + uno de WhatsApp).\n\n` +
    `⏳ Tienes *15 minutos* pa mandar esos captures, si no, perdiste la vuelta ❌.\n\n` +
    `Cuando cumplas 👉 espera mi confirmación.`);

  // Inicia un temporizador de 15 minutos
  userRequests[chatId].timer = setTimeout(() => {
    if (userRequests[chatId] && userRequests[chatId].captures.length < 2) {
      bot.sendMessage(chatId, "⏰ Se acabó tu tiempo, perdiste la oportunidad 😢\nPídele de nuevo al bot si quieres intentar otra vez.");
      delete userRequests[chatId];
    }
  }, 15 * 60 * 1000);
}

// Comandos para pedir videos
bot.onText(/\/video1/, (msg) => requestVideo(msg.chat.id, msg.from.username, 1));
bot.onText(/\/video2/, (msg) => requestVideo(msg.chat.id, msg.from.username, 2));
bot.onText(/\/video3/, (msg) => requestVideo(msg.chat.id, msg.from.username, 3));

// Manejo de fotos (captures)
bot.on("photo", (msg) => {
  const chatId = msg.chat.id;
  const username = msg.from.username || msg.from.first_name;

  if (!userRequests[chatId]) {
    bot.sendMessage(chatId, "⚠️ Primero pide un video con /video1, /video2 o /video3.");
    return;
  }

  userRequests[chatId].captures.push(msg.photo[msg.photo.length - 1].file_id);

  if (userRequests[chatId].captures.length === 2) {
    // Enviar notificación al admin con las fotos
    bot.sendMessage(adminId, `📩 Nuevo intento de desbloqueo\n👤 Usuario: @${username}\n🆔 ID: ${chatId}\nPidió: Video ${userRequests[chatId].video}`);
    userRequests[chatId].captures.forEach((fileId) => {
      bot.sendPhoto(adminId, fileId);
    });

    bot.sendMessage(chatId, "✅ Recibí tus captures, espera que *Papi Yester* los revise y te apruebe. 🔥");
  }
});

// Comando para aprobar usuarios
bot.onText(/\/aprobar (\d+) (\d+)/, (msg, match) => {
  if (msg.chat.id !== adminId) return;

  const videoNumber = parseInt(match[1]);
  const userId = parseInt(match[2]);

  if (videos[videoNumber]) {
    bot.sendMessage(userId, `🎉 Felicidades! *Papi Yester* aprobó tus captures ✅\nAquí tienes tu premio 👇\n\n${videos[videoNumber]}`);
    bot.sendMessage(adminId, `✅ Aprobaste al usuario ${userId} para el Video ${videoNumber}.`);
    delete userRequests[userId];
  } else {
    bot.sendMessage(adminId, "⚠️ Ese número de video no existe.");
  }
});