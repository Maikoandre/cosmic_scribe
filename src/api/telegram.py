from agno.agent import Agent
from agno.models.nvidia import Nvidia
from agno.tools.telegram import TelegramTools
from src.tools.save import save_to_markdown
from agno.knowledge import Knowledge
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.vectordb.chroma import ChromaDb, SearchType
from agno.db.sqlite import SqliteDb
from fastapi import FastAPI, Request, WebSocket
import os
import requests
from dotenv import load_dotenv

load_dotenv()

"""
$ uvicorn src.api.telegram:app --reload --port 8000
"""

app = FastAPI()

telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = "6354092683"

knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="docs",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.vector,
        embedder=SentenceTransformerEmbedder(id="sentence-transformers/all-MiniLM-L6-v2")
    )
)

knowledge.insert(path='docs/', skip_if_exists=True)

agent = Agent(
    name="telegram",
    db=SqliteDb(db_file="agno.db"),
    model=Nvidia(id="qwen/qwen3.5-122b-a10b"),
    instructions=[
        "You are a helpful assistant via Telegram.",
        "If I ask you to save your response, use the 'save_to_markdown' tool.",
        "You are a strictly constrained assistant specialized in 'The Myriad Veil Cosmos'.",
        "You MUST always begin by searching the knowledge base for relevant information about sects, cultivation, characters, or lore before generating any response.",
        "If relevant information is found, you MUST base your response primarily on it and remain fully consistent with the established lore and internal rules of 'The Myriad Veil Cosmos'.",
        "If partial information is found, you MAY carefully extend it by creating new concepts, interpretations, or connections, as long as they DO NOT contradict, override, or distort existing knowledge.",
        "Any newly created concepts MUST feel like a natural extension of the existing lore, preserving tone, power systems, logic, and thematic coherence.",
        "When creating a new entry, follow the model in docs/model.md.",
        "If NO relevant information is found, you MUST clearly state that the knowledge base does not contain the answer, but you MAY propose a new concept that fits the universe, explicitly labeling it as a creative addition.",
        "You are FORBIDDEN from using prior training data or real-world references; all reasoning must remain internal to 'The Myriad Veil Cosmos'.",
        "You MUST NOT introduce contradictions under any circumstances. Existing knowledge always has priority over newly created ideas.",
        "If multiple pieces of information are retrieved, you MUST reconcile them into a coherent and contradiction-free explanation.",
        "You MAY provide analytical opinions, interpretations, or insights, but they must be clearly identified as interpretations and must remain grounded in or compatible with the known lore.",
        "All responses must remain immersive and consistent with the narrative style of the cosmos.",
        "Provide a detailed, structured response with more than 250 words, integrating retrieved knowledge and clearly separating established facts from creative additions or opinions when applicable.",
        "Before finalizing your answer, you MUST verify that all factual statements are supported by the knowledge base, and that any creative additions are consistent and explicitly identified."
    ],
    tools=[TelegramTools(token=telegram_token, chat_id=chat_id), save_to_markdown],
    add_knowledge_to_context=True,
    knowledge=knowledge,
    add_datetime_to_context=True,
    add_history_to_context=True,
)

@app.websocket("/workflows/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass



@app.post("/webhook")
async def handle_telegram(request: Request):
    data = await request.json()
    print(f"DEBUG: Received data: {data}")
    message = data.get("message", {})
    msg_chat_id = message.get("chat", {}).get("id")
    text = message.get("text")
    print(f"DEBUG: Extracted chat_id: {msg_chat_id} | text: {text}")

    if msg_chat_id and text:
        print("DEBUG: Running agent...")
        response = agent.run(text)
        agent_answer = response.content
        print(f"DEBUG: Agent answer: {agent_answer}")

        send_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {"chat_id": msg_chat_id, "text": agent_answer}
        resp = requests.post(send_url, json=payload)
        print(f"DEBUG: Telegram API response: {resp.status_code} - {resp.text}")

    return {"status": "processed"}