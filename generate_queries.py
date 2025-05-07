import random
import re
from openai import OpenAI
from config import OPENAI_API_KEY, METADATA_QUERY_TEMPLATES, VIBE_PROMPT_TEMPLATE, QUERY_GEN_MODEL

openai_client = OpenAI(api_key=OPENAI_API_KEY)


def generate_vibe_query_gpt(cache, media_type, media_data: dict, num_queries:int = 3) -> list:
    # Check if vibe-style queries already exist in cache
    media_id = media_data.get("media_id")
    title = media_data.get("title", "")
    cached = cache.get(media_id, title, QUERY_GEN_MODEL)
    
    # If Yes, return cached queries
    if cached:
        return cached[:num_queries]

    # If No, generate vibe queries using LLM with customized prompt
    prompt = VIBE_PROMPT_TEMPLATE.format(
        num_queries=num_queries,
        media_type=media_type,
        title=title,
        genres=", ".join(media_data.get("genres", [])),
        director=media_data.get("director", ""),
        stars=", ".join(media_data.get("stars", [])),
        keywords=", ".join(media_data.get("keywords", [])),
        overview=media_data.get("overview", "")
    )

    try:
        response = openai_client.chat.completions.create(
            model=QUERY_GEN_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        queries = response.choices[0].message.content
        queries = re.sub(r'^\s*(\d+\.|[-•])', '', queries, flags=re.MULTILINE)
        queries_list = [line.strip() for line in queries.split("\n") if line.strip()]
        
        # Cache and return the newly generated vibe queries
        cache.set(media_id, title, QUERY_GEN_MODEL, queries_list)
        return queries_list
    except Exception as e:
        print(f"⚠️ GPT failed for media {media_id}: {e}")
        return []


def get_media_term(media_type: str) -> str:
    if media_type == "movie":
        return random.choice(["movie", "film"])
    if media_type == "tv":
        return random.choice(["TV show", "TV serie", "TV program"])  
    return media_type


def generate_metadata_query(media_type, media_data: list, num_queries: int = 3) -> list:
    # Define elements to be used in templates with smart fallback
    genre_list = media_data.get("genres", [])
    genre = random.choice(genre_list) if genre_list else "drama"
    director = media_data.get("director", "")
    star_list = media_data.get("stars", [])
    stars = (star_list[:2]) if star_list else ["an ensemble cast", "various actors"]
    keyword_list = media_data.get("keywords", [])
    keywords = random.sample(keyword_list[:5], min(2, len(keyword_list))) if keyword_list else ["life", "relationships"]
    year = media_data.get("release_date", "2000").split("-")[0]
    decade = year[:3] + "0"

    # Fitler templates to use based on media type
    filtered_templates = [
        t for t in METADATA_QUERY_TEMPLATES
        if not ("{director}" in t and media_type == "tv")
    ]

    # Generate metadata-based queries with randomly selected templates
    queries = []
    templates = random.sample(filtered_templates, min(len(METADATA_QUERY_TEMPLATES), num_queries))
    for template in templates:
        queries.append(template.format(
            media_type= get_media_term(media_type), 
            genre=genre.lower(),
            director=director,
            star_1=stars[0],
            star_2=stars[1] if len(stars) > 1 else "an ensemble cast",
            keyword_1=keywords[0],
            keyword_2=keywords[1] if len(keywords) >1 else "life",
            year=year,
            decade=decade
        ))
    return queries