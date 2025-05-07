import asyncio
from tmdb_client import TMDBClient
from build_dataset import generate_dataset_jsonl
from config import TMDB_API_KEY, get_output_path

MEDIA_TYPE = "movie"  # "movie" or "tv"
SAMPLE_COUNT_IN_K = 6  # Number of media samples to get
MIN_RATING = 6  # Minimum media rating score


async def main():
    tmdb_client = TMDBClient(api_key=TMDB_API_KEY, max_connections=15, timeout=10)

    try:
        # Fetch movie data from TMDB
        media_ids = await tmdb_client.fetch_media_ids_bulk(
            media_type=MEDIA_TYPE, 
            media_count_in_k=SAMPLE_COUNT_IN_K, 
            rating=MIN_RATING
        )

        media_details = await tmdb_client.fetch_all_media_details(
            media_type=MEDIA_TYPE, 
            media_ids=media_ids
        )

        # Check data availability
        if not media_details:
            print("⚠️ No media details fetched. Exiting early.")
            return

        # Build dataset for model training
        await generate_dataset_jsonl(
            media_raw=media_details,
            media_type=MEDIA_TYPE,
            output_path=get_output_path(MEDIA_TYPE),
            num_metadata_queries=3,  # Number of metadata-based queries to generate
            num_vibe_queries=3,  # Number of vibe-style queries to generate
            max_workers=10,
        )
    
    finally:
        await tmdb_client.aclose()

if __name__ == "__main__":
    asyncio.run(main())
