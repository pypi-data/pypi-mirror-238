from dataclasses import dataclass
from datetime import datetime
from typing import List, NamedTuple, Optional

from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride.core._filters.partitioners.models import ProcessFileInfo


class BlobTableInsertValues(NamedTuple):
    partition_start: int
    partition_end: int
    workflow_id: str
    session_id: str
    blob_id: str


class PrimaryTableInsertValues(NamedTuple):
    partition_start: int
    partition_end: int
    workflow_id: str
    session_id: str
    frame_idx_in_blob: int
    blob_idx_in_partition: int
    file_path: str
    timestamp: datetime
    file_id: int
    frame_idx_in_file: int
    file_name: str
    total_frames_in_file: int


@dataclass
class SinkWriterFilterInput:
    """Class for input params for sink writer filter."""

    file_metadata_list: List[ProcessFileInfo]
    dataset_id: str
    workflow_id: str
    session_id: str
    pipeline_tables_info: PipelineTablesInfo


class SummaryTableInsertValues(NamedTuple):
    partition_start: int
    partition_end: int
    workflow_id: str
    session_id: str
    checksum: Optional[str]
    feature: Optional[str]
    coreset: str
    projections: str
    sketch: str
    thumbnail: str
