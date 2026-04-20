from agno.agent import Agent
from agno.models.llama_cpp import LlamaCpp

agent = Agent(
    model=LlamaCpp(
        id='ggml-org/gemma-3-1b-it-GGUF',
        base_url="http://localhost:8080/v1"
    ),
    markdown=True
)

agent.print_response("Share a 2 sentence summary of the book 'The Three-Body Problem'")