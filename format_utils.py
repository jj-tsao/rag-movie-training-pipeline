from typing import Dict

def extract_media_data(media_type: str, media: Dict) -> Dict:
    # Common fields with type-specific fallbacks
    media_id = media.get("id", 0)
    title = media.get("title" if media_type == "movie" else "name", "Unknown")
    genre_list = [genre["name"] for genre in media.get("genres", [])]
    overview = media.get("overview", "No overview available.")
    tagline = media.get("tagline", "")
    star_list = media.get("stars", [])
    date_field = "release_date" if media_type == "movie" else "first_air_date"
    release_date = media.get(date_field, "")
    keyword_list = media.get("keywords", [])

    # Media type specific fields
    if media_type == "movie":
        director = media.get("director", "Unknown")
        collection = media.get("belongs_to_collection", {}).get("name", "") if media.get("belongs_to_collection") else ""
        specific_fields = {
            "collection": collection,
            "director": director,
        }
    else:  # TV show
        creator_list = media.get("creator", [])
        season_count = media.get('number_of_seasons', None)
        specific_fields = {
            "season_count": season_count,
            "creator": creator_list,
        }

    # Build metadata dictionary
    metadata = {
        "media_id": media_id,
        "media_type": media_type,
        "title": title,
        "genres": genre_list,
        "overview": overview,
        "tagline": tagline,
        "stars": star_list,
        "release_date": release_date,
        "keywords": keyword_list,
    }

    # Add media-specific fields to metadata
    metadata.update(specific_fields)

    return metadata


def format_media_document(media_type: str, media_data: Dict) -> str:
    # Build document with conditional parts
    parts = [
        f"Title: {media_data['title']}",
        f"Genres: {', '.join(media_data['genres'])}",
        f"Overview: {media_data['overview']}",
        f"Tagline: {media_data['tagline']}",
        f"Director: {media_data.get('director', '')}" if media_type == "movie" else f"Creator: {', '.join(media_data['creator'])}",
        f"Stars: {', '.join(media_data['stars'])}",
        f"Release Date: {media_data['release_date']}",
        f"Keywords: {', '.join(media_data['keywords'])}",
    ]
    
    content = '\n'.join(parts)

    return content