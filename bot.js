const { Telegraf } = require('telegraf');

// ✅ Configuración básica
const bot = new Telegraf('8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE');
const adminId = 7727617732; // Tu ID de Telegram

// 📝 Videos con links completos
const videos = {
  video1: {
    name: "VIDEO VIRAL DISPONIBLE",
    megaLink: "https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM",
    password: "123YESTERDFC",
    ytLink: "https://www.youtube.com/watch?v=TU_LINK_VIDEO1"
  },
  video2: {
    name: "Niño de los 200 pesos",
    megaLink: "https://mega.nz/file/DE90AIoA#Me2o8ziI6il4I141OBJWIx6FHeb7Hgjbc0BVs8P0bzo",
    password: null,
    ytLink: "https://www.youtube.com/watch?v=TU_LINK_VIDEO2"
  },
  video3: {
    name: "Pc gratis",
    megaLink: "https://mega.nz/collection/3NEW2TYA#jwKl6r2C1Ljid4QFDQg6zA",
    password: null,
    ytLink: "https://www.youtube.com/watch?v=TU_LINK_VIDEO3"
  }
};

// 🟢 Estado de los usuarios y videos
let userState = {}; // { username: "video1" }

// ✨ Comando de inicio
bot.start((ctx) => {
  const username = ctx.from.username;
  ctx.reply(`¡Hola @${username}! 😎 Selecciona el video que quieres ver: /video1 /video2 /video3`);
});

// 🎬 Comandos para elegir video
bot.command(['video1','video2','video3'], (ctx) => {
  const username = ctx.from.username;
  const videoKey = ctx.message.text.substring(1);
  userState[username] = videoKey;

  const video = videos[videoKey];
  let msg = `✅ Has seleccionado: *${video.name}*\n`;
  msg += `Mega Link: ${video.megaLink}\n`;
  if(video.password) msg += `Contraseña: ${video.password}\n`;
  msg += `📌 Envía tu capture del video y espera aprobación de Papi Yester`;

  ctx.replyWithMarkdown(msg);
});

// 📸 Comando para enviar capture
bot.on('photo', (ctx) => {
  const username = ctx.from.username;
  if (!userState[username]) return ctx.reply("Primero elige un video con /video1 /video2 /video3");

  ctx.reply("¡Capture recibido! Espera a que Papi Yester lo apruebe 🥷");

  // Notificación a ti
  bot.telegram.sendMessage(adminId, `📸 @${username} ha enviado un capture para ${userState[username]}`);
});

// ✅ Comando de aprobación
bot.command('aprobar', (ctx) => {
  if(ctx.from.id !== adminId) return ctx.reply("🚫 Solo Papi Yester puede usar este comando");

  const replyTo = ctx.message.reply_to_message;
  if(!replyTo) return ctx.reply("Debes responder al mensaje del capture del usuario que quieres aprobar");

  const usernameMatch = replyTo.text.match(/@(\w+)/);
  if(!usernameMatch) return ctx.reply("No pude identificar al usuario en ese mensaje");

  const username = usernameMatch[1];
  const videoKey = userState[username];
  if(!videoKey) return ctx.reply("No hay video pendiente para este usuario");

  const video = videos[videoKey];
  ctx.reply(`🎉 Capture aprobado! Enlace de YouTube: ${video.ytLink}`);

  // Mensaje privado al usuario
  bot.telegram.sendMessage(replyTo.from.id, `✅ Tu capture fue aprobado, aquí tienes el link: ${video.ytLink}`);
  delete userState[username];
});

// ❌ Evitar abusos
bot.on('text', (ctx) => {
  const text = ctx.message.text.toLowerCase();
  const username = ctx.from.username;

  if(!['/video1','/video2','/video3','/aprobar','/start'].includes(text)) {
    ctx.reply(`Ah paj3r0 😏 te atrapé! Para conseguir otro video pregúntale a papi Yester prømø øwø Aqui 👉 https://wa.me/message/5RCSCBNHHGMUB1 🔥💦💯`);
  }
});

// 🔥 Arranca el bot
bot.launch();
console.log("🤖 Bot de Papi Yester corriendo...");

// ✨ Para heroku o similares
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));