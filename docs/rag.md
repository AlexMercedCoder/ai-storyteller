# RAG & Vector Search

Storyteller now supports Retrieval-Augmented Generation (RAG) to allow the AI to "remember" vast amounts of lore without stuffing the context window.

## How it Works

1.  **Ingestion**: When you start the application, `LoreManager` reads all `.md` files in the `lore/` directory.
2.  **Embedding**: It uses `sentence-transformers` (specifically `all-MiniLM-L6-v2`) to convert your lore text into vector embeddings.
3.  **Storage**: These vectors are stored locally in a LanceDB database (`db/lancedb`).
4.  **Retrieval**: When you ask a question, the system searches for the most semantically similar lore chunks and feeds them to the AI.

## Configuration & Troubleshooting

### Opting Out of RAG
If you prefer to use the simple keyword search or want to save disk space, you can disable RAG by simply uninstalling the dependencies:

```bash
pip uninstall lancedb sentence-transformers
```

Storyteller will automatically detect that these packages are missing and fall back to keyword search.

### GPU Compatibility
By default, Storyteller attempts to use your GPU for faster embedding generation. 

- **Automatic Fallback**: If the application detects a GPU issue (e.g., CUDA errors or incompatibility), it will automatically fall back to using the CPU.
- **Performance**: CPU embedding is generally fast enough for typical lore usage, so you shouldn't notice a significant slowdown unless you are ingesting thousands of documents at once.

### Common Issues
- **First Run Slowness**: The first time you run Storyteller, it downloads the embedding model (approx. 80MB). This happens only once.
- **No Results**: Ensure your lore files are not empty and contain meaningful text.
