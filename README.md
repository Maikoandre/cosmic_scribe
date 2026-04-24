# Cosmic Scribe - The Myriad Veil Cosmos

Este projeto é um sistema de **RAG (Retrieval-Augmented Generation)** projetado para atuar como um assistente especializado no universo fictício "The Myriad Veil Cosmos". Ele utiliza uma base de conhecimento local para garantir que as respostas sejam precisas e fundamentadas exclusivamente na lore (história) fornecida.

## 🚀 Tecnologias

- **[Agno](https://agno.com/)**: Framework para construção de agentes de IA.
- **Nvidia AI Foundation**: Interface para modelos de linguagem (usando `qwen/qwen3.5-122b-a10b`).
- **ChromaDB**: Banco de dados vetorial para armazenamento e busca de documentos.
- **Sentence Transformers**: Utiliza o modelo local `all-MiniLM-L6-v2` para gerar embeddings.
- **FastAPI**: Interface web para interação com o agente.
- **Python 3.11+** com gerenciamento de dependências via **uv**.

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
    ```

4.  **Adicione seus documentos**:
    Coloque os arquivos de markdown na pasta `docs/`. O sistema indexa automaticamente arquivos nesta pasta.

## 📖 Como Usar

### Servidor de Desenvolvimento
Para iniciar o servidor FastAPI e usar a interface web do Agno:
```bash
uv run fastapi dev src/agent.py
```

### Funcionalidades Especiais
- **Persistência de Lore**: O agente possui a ferramenta `save_to_markdown`. Peça ao agente para "salvar a resposta em um arquivo" para persistir novas entradas de história na pasta `docs/`.
- **RAG Local**: Busca semântica em toda a documentação dentro de `docs/`.
- **Modo Debug**: Ativado por padrão para mostrar chamadas de ferramentas e logs detalhados no terminal.

## 📁 Estrutura do Projeto

- `src/agent.py`: Configuração principal do Agente e servidor FastAPI.
- `src/tools/save.py`: Implementação da ferramenta de persistência de arquivos.
- `docs/`: Base de conhecimento e destino de novas entradas de lore.
- `tmp/chromadb/`: Banco de dados vetorial persistente.
- `agno.db`: Histórico de sessões do agente (SQLite).

---
Criado para exploração imersiva e expansão de lore.
