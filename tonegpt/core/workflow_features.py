"""
Workflow Features System for ToneGPT
Implements undo/redo functionality, tone history navigation, batch tone generation, 
preset organization and tagging, search and filter tones, and rating system
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import copy


class HistoryAction(Enum):
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    IMPORT = "import"
    EXPORT = "export"
    COPY = "copy"
    PASTE = "paste"


class BatchOperation(Enum):
    GENERATE = "generate"
    MODIFY = "modify"
    EXPORT = "export"
    DELETE = "delete"
    TAG = "tag"
    RATE = "rate"


class SearchFilter(Enum):
    NAME = "name"
    GENRE = "genre"
    ARTIST = "artist"
    TAG = "tag"
    RATING = "rating"
    DATE_CREATED = "date_created"
    DATE_MODIFIED = "date_modified"
    BLOCK_TYPE = "block_type"
    PARAMETER = "parameter"


class SortOrder(Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


@dataclass
class HistoryEntry:
    """History entry for undo/redo functionality"""

    entry_id: str
    action: HistoryAction
    timestamp: datetime
    tone_data: Dict[str, Any]
    description: str
    metadata: Dict[str, Any]


@dataclass
class ToneTag:
    """Tone tag for organization"""

    tag_id: str
    name: str
    color: str
    description: str
    created_date: datetime


@dataclass
class ToneRating:
    """Tone rating system"""

    tone_id: str
    rating: int  # 1-5 stars
    review: str
    rated_by: str
    rated_date: datetime
    helpful_votes: int = 0


@dataclass
class ToneMetadata:
    """Comprehensive tone metadata"""

    tone_id: str
    name: str
    genre: str
    artist: Optional[str]
    tags: List[str]
    rating: float
    created_date: datetime
    modified_date: datetime
    created_by: str
    description: str
    file_size: int
    block_count: int
    parameter_count: int
    custom_fields: Dict[str, Any]


@dataclass
class BatchJob:
    """Batch processing job"""

    job_id: str
    operation: BatchOperation
    tone_ids: List[str]
    parameters: Dict[str, Any]
    status: str  # pending, running, completed, failed
    progress: float  # 0.0 - 1.0
    created_date: datetime
    completed_date: Optional[datetime]
    results: List[Dict[str, Any]]
    error_message: Optional[str]


@dataclass
class SearchQuery:
    """Search query for tone filtering"""

    query_id: str
    filters: Dict[SearchFilter, Any]
    sort_by: SearchFilter
    sort_order: SortOrder
    limit: int
    offset: int
    created_date: datetime


class WorkflowFeatures:
    """Workflow features system for FM9"""

    def __init__(self):
        self.history: List[HistoryEntry] = []
        self.history_index: int = -1
        self.tone_metadata: Dict[str, ToneMetadata] = {}
        self.tone_tags: Dict[str, ToneTag] = {}
        self.tone_ratings: Dict[str, ToneRating] = {}
        self.batch_jobs: Dict[str, BatchJob] = {}
        self.search_queries: Dict[str, SearchQuery] = {}

        # Initialize default tags
        self._initialize_default_tags()

        # Workflow settings
        self.workflow_settings = {
            "max_history_entries": 100,
            "auto_save_interval": 300,  # seconds
            "batch_size": 10,
            "search_cache_size": 1000,
            "enable_undo_redo": True,
            "enable_auto_backup": True,
        }

    def _initialize_default_tags(self):
        """Initialize default tone tags"""
        default_tags = [
            {"name": "Clean", "color": "#4CAF50", "description": "Clean guitar tones"},
            {
                "name": "Crunch",
                "color": "#FF9800",
                "description": "Crunchy overdrive tones",
            },
            {"name": "Lead", "color": "#F44336", "description": "Lead guitar tones"},
            {
                "name": "Rhythm",
                "color": "#2196F3",
                "description": "Rhythm guitar tones",
            },
            {"name": "Metal", "color": "#9C27B0", "description": "Metal guitar tones"},
            {"name": "Blues", "color": "#00BCD4", "description": "Blues guitar tones"},
            {"name": "Jazz", "color": "#795548", "description": "Jazz guitar tones"},
            {
                "name": "Country",
                "color": "#8BC34A",
                "description": "Country guitar tones",
            },
            {
                "name": "Ambient",
                "color": "#607D8B",
                "description": "Ambient guitar tones",
            },
            {
                "name": "Experimental",
                "color": "#E91E63",
                "description": "Experimental guitar tones",
            },
            {"name": "Favorite", "color": "#FFD700", "description": "Favorite tones"},
            {
                "name": "Work in Progress",
                "color": "#FF5722",
                "description": "Tones being developed",
            },
            {
                "name": "Live",
                "color": "#3F51B5",
                "description": "Live performance tones",
            },
            {
                "name": "Studio",
                "color": "#009688",
                "description": "Studio recording tones",
            },
        ]

        for tag_data in default_tags:
            tag = ToneTag(
                tag_id=str(uuid.uuid4()),
                name=tag_data["name"],
                color=tag_data["color"],
                description=tag_data["description"],
                created_date=datetime.now(),
            )
            self.tone_tags[tag.tag_id] = tag

    def add_to_history(
        self,
        action: HistoryAction,
        tone_data: Dict[str, Any],
        description: str,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Add entry to history for undo/redo"""
        if not self.workflow_settings["enable_undo_redo"]:
            return ""

        # Remove any history after current index (for redo)
        if self.history_index < len(self.history) - 1:
            self.history = self.history[: self.history_index + 1]

        # Create history entry
        entry = HistoryEntry(
            entry_id=str(uuid.uuid4()),
            action=action,
            timestamp=datetime.now(),
            tone_data=copy.deepcopy(tone_data),
            description=description,
            metadata=metadata or {},
        )

        # Add to history
        self.history.append(entry)
        self.history_index = len(self.history) - 1

        # Limit history size
        max_entries = self.workflow_settings["max_history_entries"]
        if len(self.history) > max_entries:
            self.history = self.history[-max_entries:]
            self.history_index = len(self.history) - 1

        return entry.entry_id

    def undo(self) -> Optional[Dict[str, Any]]:
        """Undo last action"""
        if not self.workflow_settings["enable_undo_redo"]:
            return None

        if self.history_index > 0:
            self.history_index -= 1
            entry = self.history[self.history_index]
            return entry.tone_data

        return None

    def redo(self) -> Optional[Dict[str, Any]]:
        """Redo last undone action"""
        if not self.workflow_settings["enable_undo_redo"]:
            return None

        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            entry = self.history[self.history_index]
            return entry.tone_data

        return None

    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return self.workflow_settings["enable_undo_redo"] and self.history_index > 0

    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return (
            self.workflow_settings["enable_undo_redo"]
            and self.history_index < len(self.history) - 1
        )

    def get_history_summary(self) -> Dict[str, Any]:
        """Get history summary"""
        return {
            "total_entries": len(self.history),
            "current_index": self.history_index,
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo(),
            "recent_actions": [
                {
                    "action": entry.action.value,
                    "description": entry.description,
                    "timestamp": entry.timestamp.isoformat(),
                }
                for entry in self.history[-5:]  # Last 5 entries
            ],
        }

    def create_tone_metadata(
        self,
        tone_id: str,
        name: str,
        tone_data: Dict[str, Any],
        created_by: str = "ToneGPT",
    ) -> ToneMetadata:
        """Create tone metadata"""
        # Count blocks and parameters
        block_count = sum(
            1
            for block in tone_data.values()
            if isinstance(block, dict) and block.get("enabled", False)
        )
        parameter_count = sum(
            len(block.get("parameters", {}))
            for block in tone_data.values()
            if isinstance(block, dict) and "parameters" in block
        )

        # Calculate file size (approximate)
        file_size = len(json.dumps(tone_data))

        metadata = ToneMetadata(
            tone_id=tone_id,
            name=name,
            genre="Unknown",
            artist=None,
            tags=[],
            rating=0.0,
            created_date=datetime.now(),
            modified_date=datetime.now(),
            created_by=created_by,
            description="",
            file_size=file_size,
            block_count=block_count,
            parameter_count=parameter_count,
            custom_fields={},
        )

        self.tone_metadata[tone_id] = metadata
        return metadata

    def update_tone_metadata(self, tone_id: str, updates: Dict[str, Any]) -> bool:
        """Update tone metadata"""
        if tone_id not in self.tone_metadata:
            return False

        metadata = self.tone_metadata[tone_id]

        # Update fields
        for key, value in updates.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)

        # Update modified date
        metadata.modified_date = datetime.now()

        return True

    def add_tone_tag(self, tone_id: str, tag_name: str) -> bool:
        """Add tag to tone"""
        if tone_id not in self.tone_metadata:
            return False

        # Find tag by name
        tag_id = None
        for tid, tag in self.tone_tags.items():
            if tag.name.lower() == tag_name.lower():
                tag_id = tid
                break

        if tag_id is None:
            # Create new tag
            tag = ToneTag(
                tag_id=str(uuid.uuid4()),
                name=tag_name,
                color="#757575",  # Default gray
                description=f"Custom tag: {tag_name}",
                created_date=datetime.now(),
            )
            self.tone_tags[tag.tag_id] = tag
            tag_id = tag.tag_id

        # Add tag to tone
        if tag_id not in self.tone_metadata[tone_id].tags:
            self.tone_metadata[tone_id].tags.append(tag_id)

        return True

    def remove_tone_tag(self, tone_id: str, tag_name: str) -> bool:
        """Remove tag from tone"""
        if tone_id not in self.tone_metadata:
            return False

        # Find tag by name
        tag_id = None
        for tid, tag in self.tone_tags.items():
            if tag.name.lower() == tag_name.lower():
                tag_id = tid
                break

        if tag_id and tag_id in self.tone_metadata[tone_id].tags:
            self.tone_metadata[tone_id].tags.remove(tag_id)
            return True

        return False

    def rate_tone(
        self, tone_id: str, rating: int, review: str = "", rated_by: str = "User"
    ) -> bool:
        """Rate a tone"""
        if tone_id not in self.tone_metadata:
            return False

        if not (1 <= rating <= 5):
            return False

        # Create or update rating
        if tone_id in self.tone_ratings:
            self.tone_ratings[tone_id].rating = rating
            self.tone_ratings[tone_id].review = review
            self.tone_ratings[tone_id].rated_date = datetime.now()
        else:
            tone_rating = ToneRating(
                tone_id=tone_id,
                rating=rating,
                review=review,
                rated_by=rated_by,
                rated_date=datetime.now(),
            )
            self.tone_ratings[tone_id] = tone_rating

        # Update metadata rating
        self.tone_metadata[tone_id].rating = rating

        return True

    def create_batch_job(
        self, operation: BatchOperation, tone_ids: List[str], parameters: Dict[str, Any]
    ) -> str:
        """Create batch processing job"""
        job = BatchJob(
            job_id=str(uuid.uuid4()),
            operation=operation,
            tone_ids=tone_ids,
            parameters=parameters,
            status="pending",
            progress=0.0,
            created_date=datetime.now(),
            completed_date=None,
            results=[],
            error_message=None,
        )

        self.batch_jobs[job.job_id] = job
        return job.job_id

    def execute_batch_job(self, job_id: str) -> bool:
        """Execute batch processing job"""
        if job_id not in self.batch_jobs:
            return False

        job = self.batch_jobs[job_id]
        job.status = "running"
        job.progress = 0.0

        try:
            total_tones = len(job.tone_ids)
            results = []

            for i, tone_id in enumerate(job.tone_ids):
                # Execute operation based on type
                if job.operation == BatchOperation.GENERATE:
                    result = self._batch_generate_tone(tone_id, job.parameters)
                elif job.operation == BatchOperation.MODIFY:
                    result = self._batch_modify_tone(tone_id, job.parameters)
                elif job.operation == BatchOperation.EXPORT:
                    result = self._batch_export_tone(tone_id, job.parameters)
                elif job.operation == BatchOperation.DELETE:
                    result = self._batch_delete_tone(tone_id, job.parameters)
                elif job.operation == BatchOperation.TAG:
                    result = self._batch_tag_tone(tone_id, job.parameters)
                elif job.operation == BatchOperation.RATE:
                    result = self._batch_rate_tone(tone_id, job.parameters)
                else:
                    result = {"success": False, "error": "Unknown operation"}

                results.append(result)
                job.progress = (i + 1) / total_tones

            job.results = results
            job.status = "completed"
            job.completed_date = datetime.now()

            return True

        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_date = datetime.now()
            return False

    def _batch_generate_tone(
        self, tone_id: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Batch generate tone"""
        # This would integrate with the tone generator
        return {"success": True, "tone_id": tone_id, "operation": "generate"}

    def _batch_modify_tone(
        self, tone_id: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Batch modify tone"""
        # This would modify existing tones
        return {"success": True, "tone_id": tone_id, "operation": "modify"}

    def _batch_export_tone(
        self, tone_id: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Batch export tone"""
        # This would export tones
        return {"success": True, "tone_id": tone_id, "operation": "export"}

    def _batch_delete_tone(
        self, tone_id: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Batch delete tone"""
        # This would delete tones
        return {"success": True, "tone_id": tone_id, "operation": "delete"}

    def _batch_tag_tone(
        self, tone_id: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Batch tag tone"""
        tag_name = parameters.get("tag_name", "")
        if tag_name:
            success = self.add_tone_tag(tone_id, tag_name)
            return {"success": success, "tone_id": tone_id, "operation": "tag"}
        return {"success": False, "error": "No tag name provided"}

    def _batch_rate_tone(
        self, tone_id: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Batch rate tone"""
        rating = parameters.get("rating", 0)
        review = parameters.get("review", "")
        rated_by = parameters.get("rated_by", "Batch")

        if 1 <= rating <= 5:
            success = self.rate_tone(tone_id, rating, review, rated_by)
            return {"success": success, "tone_id": tone_id, "operation": "rate"}
        return {"success": False, "error": "Invalid rating"}

    def create_search_query(
        self,
        filters: Dict[SearchFilter, Any],
        sort_by: SearchFilter = SearchFilter.NAME,
        sort_order: SortOrder = SortOrder.ASCENDING,
        limit: int = 50,
        offset: int = 0,
    ) -> str:
        """Create search query"""
        query = SearchQuery(
            query_id=str(uuid.uuid4()),
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset,
            created_date=datetime.now(),
        )

        self.search_queries[query.query_id] = query
        return query.query_id

    def execute_search(self, query_id: str) -> List[Dict[str, Any]]:
        """Execute search query"""
        if query_id not in self.search_queries:
            return []

        query = self.search_queries[query_id]
        results = []

        # Apply filters
        for tone_id, metadata in self.tone_metadata.items():
            if self._matches_filters(metadata, query.filters):
                results.append(
                    {
                        "tone_id": tone_id,
                        "metadata": asdict(metadata),
                        "tags": [
                            self.tone_tags[tag_id].name
                            for tag_id in metadata.tags
                            if tag_id in self.tone_tags
                        ],
                        "rating": self.tone_ratings.get(tone_id, None),
                    }
                )

        # Sort results
        results = self._sort_results(results, query.sort_by, query.sort_order)

        # Apply limit and offset
        start = query.offset
        end = start + query.limit
        return results[start:end]

    def _matches_filters(
        self, metadata: ToneMetadata, filters: Dict[SearchFilter, Any]
    ) -> bool:
        """Check if metadata matches filters"""
        for filter_type, filter_value in filters.items():
            if filter_type == SearchFilter.NAME:
                if filter_value.lower() not in metadata.name.lower():
                    return False
            elif filter_type == SearchFilter.GENRE:
                if filter_value.lower() != metadata.genre.lower():
                    return False
            elif filter_type == SearchFilter.ARTIST:
                if (
                    metadata.artist
                    and filter_value.lower() not in metadata.artist.lower()
                ):
                    return False
            elif filter_type == SearchFilter.TAG:
                if filter_value not in metadata.tags:
                    return False
            elif filter_type == SearchFilter.RATING:
                if metadata.rating < filter_value:
                    return False
            elif filter_type == SearchFilter.DATE_CREATED:
                if metadata.created_date < filter_value:
                    return False
            elif filter_type == SearchFilter.DATE_MODIFIED:
                if metadata.modified_date < filter_value:
                    return False

        return True

    def _sort_results(
        self,
        results: List[Dict[str, Any]],
        sort_by: SearchFilter,
        sort_order: SortOrder,
    ) -> List[Dict[str, Any]]:
        """Sort search results"""

        def get_sort_key(result):
            metadata = result["metadata"]
            if sort_by == SearchFilter.NAME:
                return metadata["name"].lower()
            elif sort_by == SearchFilter.GENRE:
                return metadata["genre"].lower()
            elif sort_by == SearchFilter.ARTIST:
                return metadata.get("artist", "").lower()
            elif sort_by == SearchFilter.RATING:
                return metadata["rating"]
            elif sort_by == SearchFilter.DATE_CREATED:
                return metadata["created_date"]
            elif sort_by == SearchFilter.DATE_MODIFIED:
                return metadata["modified_date"]
            else:
                return metadata["name"].lower()

        results.sort(key=get_sort_key, reverse=(sort_order == SortOrder.DESCENDING))
        return results

    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get workflow summary"""
        return {
            "total_tones": len(self.tone_metadata),
            "total_tags": len(self.tone_tags),
            "total_ratings": len(self.tone_ratings),
            "total_batch_jobs": len(self.batch_jobs),
            "total_search_queries": len(self.search_queries),
            "history_entries": len(self.history),
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo(),
            "workflow_settings": self.workflow_settings,
        }

    def export_workflow_data(self) -> Dict[str, Any]:
        """Export all workflow data"""
        return {
            "history": [asdict(entry) for entry in self.history],
            "tone_metadata": {
                tid: asdict(metadata) for tid, metadata in self.tone_metadata.items()
            },
            "tone_tags": {tid: asdict(tag) for tid, tag in self.tone_tags.items()},
            "tone_ratings": {
                tid: asdict(rating) for tid, rating in self.tone_ratings.items()
            },
            "batch_jobs": {jid: asdict(job) for jid, job in self.batch_jobs.items()},
            "search_queries": {
                qid: asdict(query) for qid, query in self.search_queries.items()
            },
            "workflow_settings": self.workflow_settings,
        }

    def save_workflow_to_file(self, filepath: str):
        """Save workflow data to file"""
        data = self.export_workflow_data()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def load_workflow_from_file(self, filepath: str):
        """Load workflow data from file"""
        with open(filepath, "r") as f:
            data = json.load(f)

        # Reconstruct objects
        self.history = [
            HistoryEntry(**entry_data) for entry_data in data.get("history", [])
        ]
        self.tone_metadata = {
            tid: ToneMetadata(**meta_data)
            for tid, meta_data in data.get("tone_metadata", {}).items()
        }
        self.tone_tags = {
            tid: ToneTag(**tag_data)
            for tid, tag_data in data.get("tone_tags", {}).items()
        }
        self.tone_ratings = {
            tid: ToneRating(**rating_data)
            for tid, rating_data in data.get("tone_ratings", {}).items()
        }
        self.batch_jobs = {
            jid: BatchJob(**job_data)
            for jid, job_data in data.get("batch_jobs", {}).items()
        }
        self.search_queries = {
            qid: SearchQuery(**query_data)
            for qid, query_data in data.get("search_queries", {}).items()
        }

        self.workflow_settings = data.get("workflow_settings", self.workflow_settings)

        # Set history index
        self.history_index = len(self.history) - 1
