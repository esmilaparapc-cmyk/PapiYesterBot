const { Telegraf } = require('telegraf');
const bot = new Telegraf('8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE'); // Tu token
const OWNER_ID = 7727617732; // Tu ID de Telegram

// Videos y links
const videos = {
  1: {
    name: "Video 1",
    youtube: "https://youtube.com/@papiyesterdfc?si=7MjVrM2-OBUzlUo0",
    whatsapp: "https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13",
    mega: "https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM",
    password: "123YESTERDFC"
  },
  2: {
    name: "Video 2",
    youtube: "https://youtube.com/@papiyesterdfc?si=7MjVrM2-OBUzlUo0",
    whatsapp: "https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13",
    mega: "https://mega.nz/file/PElVRahY#A2lXWSmVEbFw6TAMnATqMSHuYdOTB53-YWONsMqn0X4",
    password: "No tiene contraseña"
  },
  3: {
    name: "Video 3",
    youtube: "https://youtu.be/H3P60ChH8bQ?si=QBQxHoKBduMVn2M6",
    channel: "https://youtube.com/@papiyesterdfc?si=7MjVrM2-OBUzlUo0"
  }
};

// Estado de usuarios
const userState = {}; // { userId: { video: 1|2|3, startTime: Date, captures: [] } }

// Helper para mensajes con emojis y flow
function sendMessage(userId, message) {
  bot.telegram.sendMessage(userId, message, { parse_mode: 'HTML' });
}

// Comando /start
bot.start((ctx) => {
  sendMessage(ctx.from.id, `Hola @${ctx.from.username} 🤖, soy el bot oficial de los videos virales de Päpï 𝓨𝓮𝓼𝓽𝓮𝓻 prømø ØWØ𓆪 🥷 👅\nAquí podrás acceder a los videos 🔥\nUsa /video1, /video2 o /video3 para empezar.`);
});

// Función para iniciar filtro
function startFilter(userId, videoNumber) {
  userState[userId] = { video: videoNumber, startTime: new Date(), captures: [] };
  let msg = '';
  if(videoNumber === 3){
    msg = `Hola @${userId} 🥷👅, antes de que disfrutes el 🔥 Video Adulto Legal de Päpï 𝓨𝓮𝓼𝓽𝓮𝓻 prømø ØWØ𓆪, debes:\n1️⃣ Suscribirte al canal y dar like 👍 (comentario opcional 💬)\n2️⃣ Mandarme los 2 captures 📸\nTienes 30 minutos ⏱️ para completar!`;
  } else {
    msg = `Ey @${userId} 😎, antes de que disfrutes este 🔥 ${videos[videoNumber].name}, mándame los 2 captures 📸 (YouTube + WhatsApp) para asegurarnos que eres un duro 💯. ¡Rápido, que el tiempo corre ⏱️!`;
  }
  sendMessage(userId, msg);
}

// Comandos /video1, /video2, /video3
[1,2,3].forEach(num => {
  bot.command(`video${num}`, (ctx) => {
    const userId = ctx.from.id;
    if(userState[userId] && userState[userId].captures.length < 2){
      sendMessage(userId, `Tranquilo @${ctx.from.username} 😁, primero manda los captures 📸 y después puedes pedir otro video.`);
      return;
    }
    startFilter(userId, num);
    // Enviar links iniciales
    if(num === 3){
      sendMessage(userId, `🔥 Video Adulto: ${videos[3].youtube}\nCanal: ${videos[3].channel}`);
    } else {
      sendMessage(userId, `🔥 ${videos[num].name}:\nYouTube: ${videos[num].youtube}\nWhatsApp: ${videos[num].whatsapp}`);
    }
  });
});

// Recibir captures
bot.on('photo', async (ctx) => {
  const userId = ctx.from.id;
  if(!userState[userId]){
    sendMessage(userId, `Ey @${ctx.from.username} 🤖, primero pide un video usando /video1, /video2 o /video3`);
    return;
  }
  userState[userId].captures.push(ctx.message.photo[ctx.message.photo.length-1].file_id);
  sendMessage(userId, `Capture recibido 📸, ${userState[userId].captures.length}/2`);
  // Mandar captures a ti automáticamente
  if(userState[userId].captures.length === 2){
    userState[userId].captures.forEach(c => bot.telegram.sendPhoto(OWNER_ID, c, { caption: `Captures de @${ctx.from.username}` }));
    if(userState[userId].video === 3){
      sendMessage(userId, `✅ Todo listo @${ctx.from.username}! Ya puedes disfrutar tu video 🔥`);
      delete userState[userId];
    } else {
      sendMessage(userId, `Captures recibidos! Usa /aprobar ${userState[userId].video} para liberar tu video @${ctx.from.username} 😉`);
    }
  }
});

// Comando /aprobar
bot.command(/aprobar/, (ctx) => {
  const userId = ctx.from.id;
  if(userId !== OWNER_ID) return;
  const args = ctx.message.text.split(' ')[1];
  if(!args || ![1,2].includes(parseInt(args))) return;
  const vid = parseInt(args);
  sendMessage(OWNER_ID, `Video ${vid} liberado a usuario!`);
});

// Tiempo límite automático (30 min)
setInterval(() => {
  const now = new Date();
  Object.keys(userState).forEach(uid => {
    const diff = (now - userState[uid].startTime)/60000; // minutos
    if(diff > 30){
      sendMessage(uid, `⏱️ El tiempo límite de 30 minutos ha pasado 😔, vuelve a pedir el video usando /video1, /video2 o /video3`);
      delete userState[uid];
    }
  });
}, 60000); // cada 1 minuto

bot.launch();
console.log("🤖 Bot encendido, Päpï 𝓨𝓮𝓼𝓽𝓮𝓻 prømø ØWØ𓆪 🥷 👅");