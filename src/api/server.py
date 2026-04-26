from fastapi import FastAPI, Request, WebSocket
from agno.models.nvidia import Nvidia
from agno.agent import Agent
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

agent = Agent(
    model=Nvidia(id="qwen/qwen3.5-122b-a10b"),
    instructions=["Você é um assistente prestativo via WhatsApp."]
)

EVOLUTION_URL = os.getenv("EVOLUTION_URL")
INSTANCE_NAME = os.getenv("INSTANCE_NAME")
API_KEY = os.getenv("API_KEY")

@app.websocket("/workflows/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass

@app.post("/webhook")
async def handle_whatsapp(request: Request):
    data = await request.json()
    print(f"\n--- Novo Webhook Recebido ---")
    
    # Extração dos dados
    message_text = data.get("data", {}).get("message", {}).get("conversation")
    key = data.get("data", {}).get("key", {})
    remote_jid = key.get("remoteJid", "")
    from_me = key.get("fromMe", False)
    
    number = remote_jid.split("@")[0] if remote_jid else ""
    
    print(f"Texto: {message_text} | Remetente: {number} | fromMe: {from_me}")

    if message_text and number and not from_me:
        # 1. Resposta do Agente
        print("Consultando Agno...")
        response = agent.run(message_text)
        agent_answer = response.content
        print(f"Agente respondeu: {agent_answer}")

        # 2. Envio para Evolution
        send_url = f"{EVOLUTION_URL}/message/sendText/{INSTANCE_NAME}"
        headers = {"apikey": API_KEY, "Content-Type": "application/json"}
        payload = {"number": number, "text": agent_answer}
        
        print(f"Enviando para Evolution em: {send_url}")
        r = requests.post(send_url, json=payload, headers=headers)
        
        print(f"Status da Evolution: {r.status_code}")
        print(f"Resposta da Evolution: {r.text}")

    return {"status": "processed"}