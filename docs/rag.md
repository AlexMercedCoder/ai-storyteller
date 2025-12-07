# RAG & Vector Search

Storyteller now supports Retrieval-Augmented Generation (RAG) to allow the AI to "remember" vast amounts of lore without stuffing the context window.

## How it Works

1.  **Ingestion**: When you start the application, `LoreManager` reads all `.md` files in the `lore/` directory.
2.  **Embedding**: It uses `sentence-transformers` (specifically `all-MiniLM-L6-v2`) to convert your lore text into vector embeddings.
3.  **Storage**: These vectors are stored locally in a LanceDB database (`db/lancedb`).
4.  **Retrieval**: When you ask a question, the system searches for the most semantically similar lore chunks and feeds them to the AI.

## Configuration

RAG is enabled by default if you have the dependencies installed.

To disable it (and fall back to keyword search), you would need to modify the code or uninstall `lancedb`/`sentence-transformers`.

## Troubleshooting

- **First Run Slowness**: The first time you run Storyteller, it downloads the embedding model (approx. 80MB). This happens only once.
- **No Results**: Ensure your lore files are not empty and contain meaningful text.
