# backend/app/ai_utils.py

import json
import httpx
from typing import Tuple

# URL da sua API gpt4free/OpenAI-compatível local
BASE_URL = "http://localhost:3000/v1"

async def classify_issue(texto: str) -> Tuple[str, str]:
    """
    Chama o endpoint /chat/completions da sua API local
    para obter um JSON com tipo_problema e prioridade.
    Em caso de qualquer falha, faz fallback simples.
    """
    prompt = (
        "Você é um sistema de classificação de chamados de TI.\n"
        "Dado o texto abaixo, retorne apenas um JSON com:\n"
        "- tipo_problema: Hardware, Rede, Software ou Outro\n"
        "- prioridade: Alta, Média ou Baixa\n\n"
        f"Texto:\n\"\"\"{texto}\"\"\"\n\n"
        "Exemplo de resposta JSON:\n"
        '{"tipo_problema":"Rede","prioridade":"Alta"}'
    )

    payload = {
        "model": "gpt-3.5-turbo",        # ou o modelo que seu container suporta
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50,
        "temperature": 0.0
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BASE_URL}/chat/completions", json=payload, timeout=20.0)
            resp.raise_for_status()

            data = resp.json()
            # extrai o texto do primeiro choice
            content = data["choices"][0]["message"]["content"]
            # parseia o JSON vindo da IA
            obj = json.loads(content)
            tipo = obj.get("tipo_problema", "Outro")
            pri  = obj.get("prioridade",    "Média")
            print(f"🔍 [IA] resposta válida da API local: {tipo}/{pri}")
            return tipo, pri

    except Exception as e:
        # qualquer erro: log + fallback
        print(f"❌ [IA] falhou ao classificar via API local ({e}), usando fallback")
        txt = texto.lower()
        if "rede" in txt or "internet" in txt:
            return "Rede", "Alta"
        if "impressora" in txt:
            return "Hardware", "Média"
        if "erro" in txt or "falha" in txt:
            return "Software", "Média"
        return "Outro", "Baixa"
