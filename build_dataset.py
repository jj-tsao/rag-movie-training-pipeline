import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from pathlib import Path
from typing import List, Dict

from format_utils import extract_media_data, format_media_document
from generate_queries import generate_metadata_query, generate_vibe_query_gpt
from negative_sampler import NegativeSampler
from vibe_cache import VibeQueryCache
from config import get_cache_path

async def generate_dataset_jsonl(
    media_raw: List[Dict],
    media_type: str,
    output_path: str,
    num_metadata_queries: int = 3,
    num_vibe_queries: int = 3,
    max_workers:int =10,
):
    print(f"🧠 Building dataset with {len(media_raw)*6} samples...")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Format media data 
    formatted_media = [extract_media_data(media_type, media) for media in media_raw]

    # Initiate cache for vibe queries
    cache_path = get_cache_path(media_type)
    cache = VibeQueryCache(cache_path)

    # Generate vibe-based queries by calling LLM api (or using cached queries) asynchronously 
    vibe_query_results = {}
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            media_data.get("media_id"): loop.run_in_executor(executor, generate_vibe_query_gpt, cache, media_type, dict(media_data), num_vibe_queries)
            for media_data in formatted_media
        }

        for media_id, coro in tqdm(futures.items(), desc="🤖 Generating vibe queries", ncols=80):
            result = await coro
            vibe_query_results[media_id] = result

    with open(output_path, "w", encoding="utf-8") as f_out:
        sampler = NegativeSampler(formatted_media)
        for idx, media_data in enumerate(tqdm(formatted_media, desc="💾 Writing dataset", ncols=80)):
            
            # Generate positive docuemnt
            document = format_media_document(media_type, media_data)
            
            # Generate metadata-based queries
            metadata_queries = generate_metadata_query(media_type, media_data, num_queries=num_metadata_queries)

            # Get vibe queries using media_id
            media_id = media_data.get("media_id")
            vibe_queries = vibe_query_results.get(media_id, [])

            # Generate a hard negative with randomly selected strategy
            negative_media = sampler.mixed(media_data)
            negative_doc = format_media_document(media_type, negative_media)

            # Write to JSONL with a query type tag
            for query in metadata_queries:
                f_out.write(json.dumps({
                    "query": query,
                    "positive": document,
                    "negative": negative_doc,
                    "source": "metadata"
                }) + "\n")
            for query in vibe_queries:
                f_out.write(json.dumps({
                    "query": query,
                    "positive": document,
                    "negative": negative_doc,
                    "source": "semantic"
                }) + "\n")                
        sampler.print_usage_summary()

    print(f"✅ Dataset with {len(media_raw)*6} samples written to {output_path}")
