import express from "express";
import { create } from "venom-bot";
import axios from "axios";

const app = express();
app.use(express.json());

let client;

create({
  session: "tekbot-session",
  multidevice: true,
})
  .then((venomClient) => {
    client = venomClient;
    console.log("✅ Venom iniciado com sucesso!");

    // Toda vez que chegar qualquer mensagem, repassamos ao FastAPI:
    client.onAnyMessage(async (message) => {
      try {
        await axios.post("http://localhost:8000/webhook", {
          from: message.from,    // ex: "55119xxxxxx@c.us"
          body: message.body     // o texto da mensagem
        });
        console.log("🔔 Mensagem encaminhada ao FastAPI");
      } catch (err) {
        console.error("❌ Falha ao chamar webhook:", err.message);
      }
    });
  })
  .catch((err) => {
    console.error("❌ Erro ao iniciar Venom:", err);
  });

// Rota para envio de mensagens (mantém o POST /send-message)
app.post("/send-message", async (req, res) => {
  const { to, message } = req.body;
  if (!client) return res.status(500).json({ error: "Cliente Venom não pronto" });
  try {
    await client.sendText(to, message);
    return res.json({ status: "success" });
  } catch (error) {
    console.error("Erro ao enviar mensagem:", error);
    return res.status(500).json({ error: "Falha no envio" });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🚀 WhatsApp service rodando em http://localhost:${PORT}`);
});

