"""
Enhanced AI Tone Generator for FM9
Generates guitar tones using AI with comprehensive FM9 block data
Enhanced version with caching, analysis, and advanced features
"""

import hashlib
from typing import Dict, List, Any, Optional
from tonegpt.core.clean_ai_tone_generator import CleanAIToneGenerator


class EnhancedAIToneGenerator(CleanAIToneGenerator):
    """Enhanced AI tone generator with caching, analysis, and advanced features"""

    def __init__(self):
        super().__init__()
        
        # Enhanced features
        self._cache = {}
        self._cache_hits = 0
        self._cache_misses = 0

    def _get_cache_key(self, query: str) -> str:
        """Generate cache key for query"""
        return hashlib.md5(query.encode()).hexdigest()

    def _get_from_cache(self, query: str) -> Optional[Dict]:
        """Get result from cache"""
        cache_key = self._get_cache_key(query)
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]
        self._cache_misses += 1
        return None

    def _save_to_cache(self, query: str, result: Dict) -> None:
        """Save result to cache"""
        cache_key = self._get_cache_key(query)
        self._cache[cache_key] = result

    def generate_tone_from_query(self, query: str) -> Dict[str, Any]:
        """
        Generate a complete tone patch from natural language query with caching.
        
        Args:
            query: Natural language description of desired tone
            
        Returns:
            Dictionary containing tone patch and metadata
        """
        # Check cache first
        cached_result = self._get_from_cache(query)
        if cached_result:
            return cached_result

        # Generate using parent class
        result = super().generate_tone_from_query(query)
        
        # Add enhanced metadata
        result["metadata"] = {
            "generated_at": "2024-01-01T00:00:00Z",
            "generator": "EnhancedAIToneGenerator",
            "version": "1.0.0",
            "cached": False
        }
        
        # Save to cache
        self._save_to_cache(query, result)
        
        return result

    def analyze_tone_complexity(self, tone_patch: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the complexity of a tone patch.
        
        Args:
            tone_patch: The tone patch to analyze
            
        Returns:
            Dictionary containing complexity analysis
        """
        enabled_blocks = [block for block in tone_patch.values() if block.get("enabled", False)]
        
        # Count different types of effects
        effect_types = set()
        for block in enabled_blocks:
            block_type = block.get("type", "").lower()
            if any(effect in block_type for effect in ["drive", "delay", "reverb", "pitch", "dynamics"]):
                effect_types.add(block_type.split()[0])
        
        # Calculate complexity score
        complexity_score = len(enabled_blocks) + len(effect_types)
        
        return {
            "total_blocks": len(enabled_blocks),
            "effect_types": len(effect_types),
            "complexity_score": complexity_score,
            "complexity_level": "Simple" if complexity_score < 5 else "Moderate" if complexity_score < 8 else "Complex"
        }

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = (self._cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(self._cache),
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "hit_rate": f"{hit_rate:.1f}%"
        }

    def clear_cache(self) -> None:
        """Clear the cache"""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0
