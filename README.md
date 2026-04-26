# Cosmic Scribe - The Myriad Veil Cosmos

Este projeto é um sistema de **RAG (Retrieval-Augmented Generation)** especializado em worldbuilding. Ele não apenas consulta a base de conhecimento do universo **The Myriad Veil Cosmos**, mas também é capaz de expandi-la de forma consistente. O agente segue regras estritas para evitar contradições, garantindo que novas técnicas de cultivo, seitas e personagens respeitem as leis e o tom da lore original.


## 🚀 Tecnologias

- **[Agno](https://agno.com/)**: Framework para construção de agentes de IA.
- **Nvidia AI Foundation**: Interface para modelos de linguagem.
- **ChromaDB**: Banco de dados vetorial para armazenamento e busca de documentos.
- **Sentence Transformers**: Utiliza o modelo local `all-MiniLM-L6-v2` para gerar embeddings.
- **FastAPI**: Interface web para interação com o agente.
- **Python 3.11+** com gerenciamento de dependências via **uv**.

## 📁 Estrutura do Projeto

- `src/core/agent.py`: Configuração centralizada do Agente.
- `src/api/telegram.py`: Endpoint de Webhook para Telegram.
- `src/api/whatsapp.py`: Endpoint de Webhook para WhatsApp.
- `src/tools/save.py`: Implementação da ferramenta de persistência de arquivos.
- `docs/`: Base de conhecimento e destino de novas entradas de lore.
- `data/chromadb/`: Banco de dados vetorial persistente.
- `data/agno.db`: Histórico de sessões do agente (SQLite).

## 🛠️ Configuração

1.  **Instale o `uv`** (caso não possua):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Sincronize o ambiente**:
    ```bash
    uv sync
    ```

3.  **Configure as variáveis de ambiente**:
    Crie um arquivo `.env` na raiz do projeto:
    ```text
    NVIDIA_API_KEY=sua_chave_aqui
    TELEGRAM_TOKEN=seu_token_aqui
    ```

4.  **Adicione seus documentos**:
    Coloque os arquivos de markdown na pasta `docs/`. O sistema indexa automaticamente arquivos nesta pasta.

## 📖 Como Usar

### Executar a API Central (AgentOS)
```bash
uv run fastapi dev main.py
```

### Executar Integração Telegram
```bash
uvicorn src.api.telegram:app --reload --port 8000
```

### Executar Integração WhatsApp
```bash
uvicorn src.api.whatsapp:app --reload --port 8000
```

---
Criado para exploração imersiva e expansão de lore.