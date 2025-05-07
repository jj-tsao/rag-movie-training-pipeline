from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
QUERY_GEN_MODEL = "gpt-3.5-turbo"

if not OPENAI_API_KEY or not TMDB_API_KEY:
    raise ValueError("Missing API key(s).")


def get_output_path(media_type: str) -> str:
    base_dir = r"C:\Users\JJ\Projects\RAG_Movie\RAG_Moive_Assistant\fine_tuned_retriever\data\processed"
    return os.path.join(base_dir, f"{media_type}_train.jsonl")


def get_cache_path(media_type: str) -> str:
    base_dir = r"C:\Users\JJ\Projects\RAG_Movie\RAG_Moive_Assistant\fine_tuned_retriever\data\cache"
    return os.path.join(base_dir, f"{media_type}_vibe_cache.jsonl")


VIBE_PROMPT_TEMPLATE = """
You are a helpful AI assistant helping generate training data for a {media_type} search system.

Given the following {media_type} metadata and plot overview, generate {num_queries} short natural-sounding queries a user might type if they are looking for a {media_type} *like this*. 

Focus on emotional tone, mood, or storytelling vibe — not just factual filters like genre or year. Use adjectives like "inspiring", "feel-good", "satirical", "heartbreaking", "suspenseful", "captivating", "though-provoking", etc.

For example: Mind-bending sci-fi {media_type}s with deep philosophical themes, Dark and gritty dramas with character-driven narratives.

Each response should be a plain string on a new line. Do **not** include any numbering, bullet points, or dashes. 

---
Title: {title}
Genres: {genres}
Director: {director}
Stars: {stars}
Keywords: {keywords}
Overview: {overview}
---
Queries:
"""

METADATA_QUERY_TEMPLATES = [
    # Fuzzy Matching
    "Any {genre} {media_type}s starring {star_1}?",
    "I'm in the mood for {genre} {media_type}s from {decade} about {keyword_1}",
    "Something like a {genre} story dealing with {keyword_1} or {keyword_2}",
    "{genre} {media_type}s directed by {director}",

    # Medium Specificity
    "What are some must-watch {genre} {media_type}s from the {decade}s reflecting on {keyword_1} and {keyword_2}",
    "Any recommendations for top {genre} {media_type}s from {decade} featuring {star_2}?",
    "Memorable {genre} {media_type}s focused on {keyword_1} and grappling with {keyword_2}",
    "Know any good {media_type}s with both {star_1} and {star_2}?",
    "Can you recommend something where {star_1} struggles with {keyword_1} and {keyword_2}",
    "Could you suggest some intriguing {genre} {media_type}s by {director} that are built around {keyword_1} and {keyword_2}",
    "Looking for {media_type}s with {star_1} and {star_2} in the main cast and centered around {keyword_2}",

    # Precise Requirement
    "Iconic {genre} {media_type}s from the {decade}s touching on {keyword_1} and {keyword_2} with standout performances by {star_2}",
    "Please suggest {genre} {media_type}s portraying {keyword_1} and {keyword_2}, starring {star_1}, that came out in {year}",
    "Critically acclaimed {genre} {media_type}s directed by {director} exploring the themes of {keyword_1} and {keyword_2}",
]

