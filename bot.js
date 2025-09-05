// keep_alive.js incluido primero
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Bot de Päpï 𝓨𝓮𝓼𝓽𝓮𝓻 prømø ØWØ𓆪 🥷 👅 funcionando ✅");
});

app.listen(3000, () => console.log("Keep-alive activo en puerto 3000"));

module.exports = app;

// --------------------------------------------------

const { Telegraf } = require("telegraf");
const bot = new Telegraf("8389580300:AAGVhDtjF0RmQHCKRSjo7FEaOUKIgnPGhiE");
const adminId = 7727617732;

const captureTimeout = 30 * 60 * 1000; // 30 minutos
let pendingCaptures = {}; // { userId: { video: 1, timer: setTimeout } }

// Mensajes con flow
const introMsg = (username) =>
  `Hola @${username} 👋, soy el bot 🤖 de los videos virales de Päpï 𝓨𝓮𝓼𝓽𝓮𝓻 prømø ØWØ𓆪 🥷 👅
Para ver los videos usa /video1, /video2 o /video3.
Antes de pedir otro video, primero envía tus captures 😎`;

const remindCapturesMsg = (username) =>
  `Tranquil@ pajer@ @${username} 😁 primero manda los captures y luego puedes pedir otro video 😎`;

const videoLinks = {
  1: {
    youtube: "https://youtube.com/@papiyesterdfc?si=7MjVrM2-OBUzlUo0",
    whatsapp: "https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13",
    mega: "https://mega.nz/file/aA9D1DBS#xg1B0F7Hh9DQJdJEGvOoMqQ-1BXDNmIuFr1a21_omMM",
    password: "123YESTERDFC",
  },
  2: {
    youtube: "https://youtube.com/@papiyesterdfc?si=7MjVrM2-OBUzlUo0",
    whatsapp: "https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13",
    mega: "https://mega.nz/file/PElVRahY#A2lXWSmVEbFw6TAMnATqMSHuYdOTB53-YWONsMqn0X4",
    password: "No tiene contraseña 🙅🏽‍♂️",
  },
  3: {
    youtube: "https://youtu.be/H3P60ChH8bQ?si=QBQxHoKBduMVn2M6",
    channel: "https://youtube.com/@papiyesterdfc?si=7MjVrM2-OBUzlUo0",
    whatsapp: "https://whatsapp.com/channel/0029VbAlDJX7NoZx5V8pMC13",
  },mega: "https://mega.nz/collection/SNNGDLaK#DHaQKN-aHiUobg3mK8wPxg"’
};

bot.start((ctx) => ctx.reply(introMsg(ctx.from.username)));

// Función para iniciar filtro de captures
function startCaptureFilter(userId, videoNum, ctx) {
  pendingCaptures[userId] = {
    video: videoNum,
    timer: setTimeout(() => {
      delete pendingCaptures[userId];
      ctx.reply(
        `Tiempo límite de 30 minutos expirado ⏱️ para video ${videoNum} @${ctx.from.username}. Vuelve a pedirlo si quieres 😎`
      );
    }, captureTimeout),
  };
}

// Comandos de videos
bot.command("video1", (ctx) => {
  if (pendingCaptures[ctx.from.id]) {
    return ctx.reply(remindCapturesMsg(ctx.from.username));
  }
  const v = videoLinks[1];
  ctx.reply(
    `🎬 VIDEO 1 🔥\nYouTube: ${v.youtube}\nWhatsApp: ${v.whatsapp}\nMega: ${v.mega}\nContraseña: ${v.password}\n\nManda los 2 captures en los próximos 30 minutos para recibir notificación! 🥷👅`
  );
  startCaptureFilter(ctx.from.id, 1, ctx);
});

bot.command("video2", (ctx) => {
  if (pendingCaptures[ctx.from.id]) {
    return ctx.reply(remindCapturesMsg(ctx.from.username));
  }
  const v = videoLinks[2];
  ctx.reply(
    `🎬 VIDEO 2 🔥\nYouTube: ${v.youtube}\nWhatsApp: ${v.whatsapp}\nMega: ${v.mega}\nContraseña: ${v.password}\n\nManda los 2 captures en los próximos 30 minutos para recibir notificación! 🥷👅`
  );
  startCaptureFilter(ctx.from.id, 2, ctx);
});

bot.command("video3", (ctx) => {
  if (pendingCaptures[ctx.from.id]) {
    return ctx.reply(remindCapturesMsg(ctx.from.username));
  }
  const v = videoLinks[3];
  ctx.reply(
    `🎬 VIDEO 3 🔥 PORNO Infantil -🔞\nYouTube Video: ${v.youtube}\nCanal: ${v.channel}\nWhatsApp: ${v.whatsapp}\n\nAntes de recibir el video final, manda los 2 captures en los próximos 30 minutos 🥷👅`
  );
  startCaptureFilter(ctx.from.id, 3, ctx);
});

// Captures (ejemplo: usuario envía imágenes)
bot.on("photo", (ctx) => {
  const pending = pendingCaptures[ctx.from.id];
  if (!pending) return;

  // Notifica al admin
  bot.telegram.sendMessage(
    adminId,
    `📸 Captures recibidos de @${ctx.from.username} para VIDEO ${pending.video}`
  );

  // Limpiar filtro
  clearTimeout(pending.timer);
  delete pendingCaptures[ctx.from.id];

  // Entregar video final automáticamente
  const v = videoLinks[pending.video];
  ctx.reply(`✅ Captures aprobados automáticamente @${ctx.from.username}! Aquí está tu link final: ${v.mega}`);
});

bot.launch();
console.log("Bot de Päpï 𝓨𝓮𝓼𝓽𝓮𝓻 prømø ØWØ𓆪 🥷 👅 activo y keep-alive funcionando ✅");