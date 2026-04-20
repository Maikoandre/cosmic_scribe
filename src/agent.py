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
        search_type=SearchType.vector,
        embedder=SentenceTransformerEmbedder(id="sentence-transformers/all-MiniLM-L6-v2")
    )
)

knowledge.insert(path='docs/', skip_if_exists=True)

agent = Agent(
    model=LlamaCpp(
        id='ggml-org/gemma-3-1b-it-GGUF',
        base_url="http://localhost:8080/v1"
    ),
    instructions=[
        "You are a specialized assistant for 'The Myriad Veil Cosmos'.",
        "Always search the knowledge base for any information regarding sects, cultivation, characters, or lore.",
        "If you find information in the knowledge base, prioritize it over your own training data.",
        "Provide a detailed response of more than 250 words.",
    ],
    markdown=True,
    add_knowledge_to_context=True,
    knowledge=knowledge
)

agent.print_response("What is the Eight Desolates?")