# 🧠 RAG Movie & TV Retriever Training Pipeline

A training data generator for contrastive learning — designed to build triplet datasets (query, positive, negative) for fine-tuning embedding models to power smarter movie/TV recommendations.

---

## 🔗 Related Projects

- 💬 Embedding pipeline: [rag-movie-embedding-pipeline](https://github.com/jj-tsao/rag-movie-embedding-pipeline)
- 🎬 Frontend app: [rag-movie-recommender-app](https://github.com/jj-tsao/rag-movie-recommender-app)  
- 🚀 Live demo: [Hugging Face Spaces](https://huggingface.co/spaces/JJTsao/RAG_Movie_Recommendation_Assistant)

---

## 📌 What It Does

- 🎬 **Data Extraction**: Pulls movie metadata from TMDB (titles, genres, cast, plot, streaming, keywords, etc.)
- 🧠 **Vibe Query Generation** — Uses GPT to generate tone/mood-driven natural language queries based on movie data for training
- 🏷️ **Metadata Query Generation** — Defines templates to generate queries focusing on genres, stars, and themes for training
- ⚖️ **Negative Sampling** — Hard negatives selected using genre contrast, theme mismatch, or similar stars
- 🗃️ **Triplet Dataset Builder** — Outputs JSONL rows for training: `{query, positive, negative, source}`
- 🧵 **Async + Cached** — Supports multithreaded GPT calls and caching to reduce API costs

---

## 💡 Use Cases

- Fine-tune SentenceTransformers (e.g., `bge`, `miniLM`, `MPNet`) using MultipleNegativesRankingLoss or TripletLoss
- Build training data for **semantic retrievers**, **hybrid search**, or **vibe-based discovery engines**

---

## 🛠️ Tech Stack

- Python 3.10+
- TMDB API
- OpenAI GPT-3.5 (for query generation)
- TQDM + AsyncIO for batching
- SentenceTransformers-compatible triplet output
- Base models: `bge`, `miniLM`, `MPNet`

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourname/rag-movie-training-pipeline.git
cd rag-movie-training-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file:
```
OPENAI_API_KEY=your_openai_key
TMDB_API_KEY=your_tmdb_key
```

### 4. Run the pipeline

```bash
python training_data_pipeline_main.py
```

---

## 🧪 Sample Output Format
```json
{
  "query": "Mind-bending sci-fi films with deep emotional arcs",
  "positive": "Title: Arrival...\nOverview: ...\nStars: Amy Adams...",
  "negative": "Title: Pitch Perfect...\nOverview: ...",
  "source": "semantic"
}
```

---

## 📂 Folder Overview
```graphql
├── main.py               # Pipeline runner
├── tmdb_client.py        # Fetches TMDB movie data
├── build_dataset.py      # Builds JSONL with queries + negatives
├── generate_queries.py   # LLM-powered & templatized query creation
├── negative_sampler.py   # Metadata(genre/theme/star/year, etc.)-based negatives
├── format_utils.py       # Format movie text blocks
├── config.py             # .env + output/cache paths
├── data/                 # Cache and output folders
└── requirements.txt
```

---

## 📈 Metrics

| Metric     | Fine-Tuned `bge-base-en-v1.5` | Base `bge-base-en-v1.5` |
| ---------- | :---------------------------: | :---------------------: |
| Recall\@1  |           **0.456**           |          0.214          |
| Recall\@3  |           **0.693**           |          0.361          |
| Recall\@5  |           **0.758**           |          0.422          |
| Recall\@10 |           **0.836**           |          0.500          |
| MRR        |           **0.595**           |          0.315          |

**Model Details**: [JJTsao/fine-tuned_movie_retriever-bge-base-en-v1.5](https://huggingface.co/JJTsao/fine-tuned_movie_retriever-bge-base-en-v1.5)

<br />
  
| Metric      | Fine-Tuned `all-minilm-l6-v2` | Base `all-minilm-l6-v2` |
|-------------|:-----------------------------:|:-----------------------:|
| Recall@1    |           **0.428**           |          0.149          |
| Recall@3    |           **0.657**           |          0.258          |
| Recall@5    |           **0.720**           |          0.309          |
| Recall@10   |           **0.795**           |          0.382          |
| MRR         |           **0.563**           |          0.230          |

**Model Details**: [JJTsao/fine-tuned_movie_retriever-all-minilm-l6-v2](https://huggingface.co/JJTsao/fine-tuned_movie_retriever-all-minilm-l6-v2)

<br />

**Evaluation setup**:
- Dataset: 3,598 held-out metadata and vibe-style natural queries
- Method: Top-k ranking using cosine similarity between query and positive documents
- Goal: Assess top-k retrieval quality in recommendation-like settings

---

## 📄 License
[MIT License](https://github.com/jj-tsao/rag-movie-training-pipeline/blob/main/LICENSE)
