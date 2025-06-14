# backend/app/ai_utils.py

import re, json
import httpx
from typing import Tuple

BASE_URL = "http://localhost:3000/v1"

async def classify_issue(texto: str) -> Tuple[str, str]:
    prompt = (
        "Você é um sistema de classificação de chamados de TI.\n"
        "Dado o texto abaixo, responda em JSON com:\n"
        "- tipo_problema: Hardware, Rede, Software ou Outro\n"
        "- prioridade: Alta, Média ou Baixa\n\n"
        f"Texto:\n\"\"\"{texto}\"\"\"\n\n"
        "Exemplo de resposta JSON:\n"
        '{"tipo_problema":"Rede","prioridade":"Alta"}'
    )

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50,
        "temperature": 0.0
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BASE_URL}/chat/completions", json=payload, timeout=20.0)
            resp.raise_for_status()
            raw = resp.text

        # 1) Limpa caracteres de controle não imprimíveis
        cleaned = re.sub(r"[\x00-\x1F\x7F]", "", raw)

        # 2) Extrai o JSON (primeiro {...})
        m = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not m:
            raise ValueError("nenhum JSON encontrado na resposta")

        json_str = m.group(0)
        data = json.loads(json_str)

        tipo = data.get("tipo_problema", "Outro")
        pri  = data.get("prioridade",    "Média")
        print(f"🔍 [IA] resposta válida da API local: {tipo}/{pri}")
        return tipo, pri

    except Exception as e:
        print(f"❌ [IA] falhou ao classificar via API local ({e}), usando fallback")
        txt = texto.lower()
        if "rede" in txt or "internet" in txt:
            return "Rede", "Alta"
        if "impressora" in txt:
            return "Hardware", "Média"
        if "erro" in txt or "falha" in txt:
            return "Software", "Média"
        return "Outro", "Baixa"
