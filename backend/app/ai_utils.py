# backend/app/ai_utils.py

import os, json
from dotenv import load_dotenv
import openai

load_dotenv()                       # garante carregar o .env
openai.api_key = os.getenv("OPENAI_API_KEY")
print("🔑 OPENAI_API_KEY:", bool(openai.api_key))  # log de chave

async def classify_issue(texto: str) -> tuple[str, str]:
    print("🔍 [IA] classify_issue foi chamado com texto:", texto)
    prompt = f"""
Você é um sistema de classificação de chamados de TI.
Dado o texto abaixo, responda em JSON com:
- tipo_problema: (Hardware, Rede, Software, Outro)
- prioridade: (Alta, Média, Baixa)

Texto:
\"\"\"{texto}\"\"\"

JSON:
{{
  "tipo_problema": "",
  "prioridade": ""
}}
"""
    resp = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0.0,
        max_tokens=50,
    )
    content = resp.choices[0].message.content
    print("🔍 [IA] resposta bruta:", content)
    data = json.loads(content)
    print("🔍 [IA] JSON parseado:", data)
    return data.get("tipo_problema"), data.get("prioridade")
