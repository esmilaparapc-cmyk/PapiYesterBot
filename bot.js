const TelegramBot = require('node-telegram-bot-api');

// Token de Telegram como variable de entorno
const token = process.env.TELEGRAM_TOKEN;

// Tu ID de Telegram para recibir notificaciones
const adminId = '7727617732';

// Inicializa el bot
const bot = new TelegramBot(token, { polling: true });

// Videos reales
const videos = {
  1: 'https://www.youtube.com/watch?v=VIDEO1_REAL',
  2: 'https://www.youtube.com/watch?v=VIDEO2_REAL',
  3: 'https://mega.nz/collection/3NEW2TYA#jwKl6r2C1Ljid4QFDQg6zA'
};

// Cuando un usuario envía /start
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, `Bienvenido ${msg.from.first_name} 😎\nMándame el capture del video que quieres ver y yo te aprobaré.`);
});

// Cuando el usuario envía una foto (capture)
bot.on('photo', (msg) => {
  const chatId = msg.chat.id;
  const username = msg.from.username;

  // Notificación al admin
  bot.sendMessage(adminId, `Nuevo capture de @${username}. Revisa y decide qué video aprobar.`);

  // Mensaje de espera
  bot.sendMessage(chatId, 'Gracias 😏, papi Yester revisará tu capture. Cuando apruebe, te daré el video.');
});

// Comando para aprobar videos (solo tú, admin)
bot.onText(/\/aprobar (\d+) (\d+)/, (msg, match) => {
  const chatId = msg.chat.id;
  if (chatId.toString() !== adminId) return;

  const userId = match[1];
  const videoNum = match[2];

  if (!videos[videoNum]) return;

  bot.sendMessage(userId, `🔥 Aquí está tu video ${videoNum}: ${videos[videoNum]}`);
});

// Mensaje para usuarios que intenten pedir otro video sin autorización
bot.onText(/\/video/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, `Ah paj3r0 te atrapé 😏\nPara conseguir otro video, pregúntale a papi Yester prømø øwø 👉 https://wa.me/message/5RCSCBNHHGMUB1 🚀💥`);
});