import akridata_akrimanager_v2 as am


class Constants:
    LOG_CONFIG_FILE_NAME = "pylogconf.yaml"
    INGEST_WF_TOKEN_SIZE = 1024
    INGEST_FILES_COUNT_IN_ONE_PARTITION = 10000
    PARTITION_SIZE = 300000000
    PROCESS_WF_TOKEN_SIZE = 1500
    FILE_TYPES = [
        am.DatastoreFileType.BLOBS,
        am.DatastoreFileType.CORESET,
        am.DatastoreFileType.PROJECTIONS,
        am.DatastoreFileType.SKETCH,
        am.DatastoreFileType.THUMBNAIL,
    ]
    THUMBNAIL_AGGREGATOR_SDK_DETAILS = am.AkriSDKFilterDetails(
        run_method="run",
        module="pyakri_de_filters.thumbnail.thumbnail_aggregator",
        class_name="ThumbnailAggregator",
    )
    DATASET_FILES_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "file_path",
    ]
    PARTITIONED_TABLE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "file_path",
        "file_id",
        "partition_id",
    ]
    BLOB_TABLE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "blob_id",
    ]
    SUMMARY_TABLE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "coreset",
        "projections",
        "sketch",
        "thumbnail",
    ]
    PRIMARY_TABLE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "frame_idx_in_blob",
        "blob_idx_in_partition",
        "file_path",
        "timestamp",
        "file_id",
        "frame_idx_in_file",
        "file_name",
        "total_frames_in_file",
    ]
