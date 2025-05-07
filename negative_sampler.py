import random
from collections import defaultdict


class NegativeSampler:
    def __init__(self, all_media):
        self.all_media = all_media
        self.usage_counter = defaultdict(int)

    # Media with no overlapping genres
    def genre_contrast(self, current_media):
        target_genres = set(current_media.get("genres", []))
        candidates = [
            m for m in self.all_media
            if m["media_id"] != current_media["media_id"] and not target_genres.intersection(set(m.get("genres", [])))
        ]
        return self._fallback_if_empty(candidates, current_media)

    # Media with different themes (No overlapping keywords)
    def theme_mismatch(self, current_media):
        target_keywords = set(current_media.get("keywords", []))
        candidates = [
            m for m in self.all_media
            if m["media_id"] != current_media["media_id"] and not target_keywords.intersection(set(m.get("keywords", [])))
        ]
        return self._fallback_if_empty(candidates, current_media)

    # Media with overlapping stars, but no overlapping keywords
    def same_star_diff_theme(self, current_media):
        stars = set(current_media.get("stars", []))
        keywords = set(current_media.get("keywords", []))
        candidates = [
            m for m in self.all_media
            if m["media_id"] != current_media["media_id"]
            and stars.intersection(set(m.get("stars", [])))
            and not keywords.intersection(set(m.get("keywords", [])))
        ]
        return self._fallback_if_empty(candidates, current_media)

    # Randomly selected
    def random_negative(self, current_media):
        candidates = [m for m in self.all_media if m["media_id"] != current_media["media_id"]]
        return random.choice(candidates)

    # Randomly choose among nagative sampling strategies
    def mixed(self, current_media):
        strategies = [
            self.genre_contrast,
            self.theme_mismatch,
            self.same_star_diff_theme,
            self.random_negative
        ]
        strategy = random.choice(strategies)
        return strategy(current_media)

    # Fall back to randomly select strategy
    def _fallback_if_empty(self, candidates, current_media):
        if not candidates:
            return self.random_negative(current_media)
        return random.choice(candidates)