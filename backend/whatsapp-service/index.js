import express from "express";
import { create } from "venom-bot";

const app = express();
app.use(express.json());

let client;

create({
  session: "tekbot-session",
  multidevice: true,
  // Remova/exclua estas linhas, pois agora queremos usar o Chromium que o Puppeteer baixar
  // executablePath: "/usr/bin/google-chrome-stable",
  // puppeteerOptions: { headless: "new", args: [ /* ... */ ] },

  // Sem configurações específicas, o Venom/Puppeteer usa seu Chromium interno:
})
  .then((venomClient) => {
    client = venomClient;
    console.log("✅ Venom iniciado com sucesso!");
  })
  .catch((err) => {
    console.error("❌ Erro ao iniciar Venom:", err);
  });

app.post("/send-message", async (req, res) => {
  const { to, message } = req.body;
  if (!client) {
    return res.status(500).json({ error: "Cliente Venom não pronto" });
  }
  try {
    await client.sendText(to, message);
    return res.json({ status: "success" });
  } catch (error) {
    console.error("Erro ao enviar mensagem:", error);
    return res.status(500).json({ error: "Falha no envio" });
  }
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`🚀 WhatsApp service rodando em http://localhost:${PORT}`);
});
