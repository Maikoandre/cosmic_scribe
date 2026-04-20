from agno.agent import Agent
from agno.models.llama_cpp import LlamaCpp
from agno.knowledge import Knowledge
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.vectordb.chroma import ChromaDb, SearchType

knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="docs",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=SentenceTransformerEmbedder(id="sentence-transformers/all-MiniLM-L6-v2")
    )
)

knowledge.insert(path='docs/')

agent = Agent(
    model=LlamaCpp(
        id='ggml-org/gemma-3-1b-it-GGUF',
        base_url="http://localhost:8080/v1"
    ),
    instructions="Write a detailed response of more than 250 words.",
    markdown=True,
    search_knowledge=True,
    knowledge=knowledge
)

agent.print_response("What is the Eight Desolates?")