from datetime import datetime
from typing import Dict, List, Tuple

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
from pyakri_de_filters.utils.file_utils import get_input_files_dir

from akride._utils.store_utils import upload_file_to_data_store
from akride.core._filters.sink.models import SinkWriterFilterInput
from akride.core.constants import Constants
from akride.core.exceptions import ServerError


class SinkWriterFilter:
    def __init__(
        self,
        filter_input: SinkWriterFilterInput,
        workflow_api: am.WorkflowsApi,
        dsp_dataset_api: dsp.DatasetApi,
        ccs_api: am.CcsApi,
    ):
        self._filter_input = filter_input
        self._workflow_api = workflow_api
        self._dsp_dataset_api = dsp_dataset_api
        self._ccs_api = ccs_api

    def run_from_input_dir(
        self,
        blobs_dir: str,
        coreset_dir: str,
        sketch_dir: str,
        projections_dir: str,
        thumbnail_dir: str,
    ):
        files_path_map = {}
        for data_dir, file_type in [
            (blobs_dir, am.DatastoreFileType.BLOBS),
            (coreset_dir, am.DatastoreFileType.CORESET),
            (sketch_dir, am.DatastoreFileType.SKETCH),
            (projections_dir, am.DatastoreFileType.PROJECTIONS),
            (thumbnail_dir, am.DatastoreFileType.THUMBNAIL),
        ]:
            arrow_files = get_input_files_dir(directory=data_dir)
            files_path_map[file_type] = str(arrow_files[0])

        self._run_from_files_map(files_map=files_path_map)

    def _get_partition_details(self) -> Tuple[int, int, str]:
        partition_start = self._filter_input.file_metadata_list[
            0
        ].partition_start
        partition_end = self._filter_input.file_metadata_list[0].partition_end
        partition_id = f"{partition_start}_{partition_end}"
        return partition_start, partition_end, partition_id

    def run(
        self,
        blobs_arrow_path: str,
        coreset_arrow_path: str,
        sketch_arrow_path: str,
        projections_arrow_path: str,
        thumbnail_arrow_path: str,
    ):
        files_map = {
            am.DatastoreFileType.BLOBS: blobs_arrow_path,
            am.DatastoreFileType.CORESET: coreset_arrow_path,
            am.DatastoreFileType.SKETCH: sketch_arrow_path,
            am.DatastoreFileType.PROJECTIONS: projections_arrow_path,
            am.DatastoreFileType.THUMBNAIL: thumbnail_arrow_path,
        }

        self._run_from_files_map(files_map=files_map)

    def _run_from_files_map(self, files_map: Dict[am.DatastoreFileType, str]):
        (
            partition_start,
            partition_end,
            partition_id,
        ) = self._get_partition_details()

        store_path_map = self._store_files_to_data_store(
            partition_id=partition_id, files_map=files_map
        )

        self._update_dataset_partition(
            partition_id=partition_id,
            partition_start=partition_start,
            partition_end=partition_end,
            store_path_map=store_path_map,
        )

        self._insert_entries_to_pipeline_tables(
            store_path_map=store_path_map,
            partition_start=partition_start,
            partition_end=partition_end,
        )

    def _store_files_to_data_store(
        self, partition_id: str, files_map: Dict[am.DatastoreFileType, str]
    ):
        # Get pre-signed url for each file type
        list_pre_signed_response: am.ListPreSignedUrlResponseWithOperation = (
            self._workflow_api.generate_presigned_url_for_workflow_files(
                dataset_id=self._filter_input.dataset_id,
                file_types=Constants.FILE_TYPES,
                partition_id=partition_id,
                session_id=self._filter_input.session_id,
            )
        )

        store_path_map = {}
        # Store file metadata to sink store using pre-signed url
        for pre_signed_url_resp in list_pre_signed_response.presignedurls:
            pre_signed_url_resp: am.GetPreSignedUrlResponseWithOperation = (
                pre_signed_url_resp
            )

            fields = pre_signed_url_resp.fields
            store_path_with_dataset_id = fields.get("key")
            if not store_path_with_dataset_id:
                raise ServerError(
                    "Key is not present in the presigned url resp"
                )

            store_path_without_dataset_id = "/".join(
                store_path_with_dataset_id.split("/")[1:]
            )

            upload_file_to_data_store(
                file_path=files_map[pre_signed_url_resp.file_type],
                presigned_url=pre_signed_url_resp.url,
                fields=fields,
            )

            store_path_map[
                pre_signed_url_resp.file_type
            ] = store_path_without_dataset_id

        return store_path_map

    def _update_dataset_partition(
        self,
        partition_id: str,
        partition_start: int,
        partition_end: int,
        store_path_map: Dict[am.DatastoreFileType, str],
    ):
        partition_create_request = dsp.PipelinePartitionCreateRequest(
            partition_end=partition_end,
            partition_start=partition_start,
            projections=store_path_map[am.DatastoreFileType.PROJECTIONS],
            blobs=[store_path_map[am.DatastoreFileType.BLOBS]],
            sketch=store_path_map[am.DatastoreFileType.SKETCH],
            thumbnail_blobs=[store_path_map[am.DatastoreFileType.THUMBNAIL]],
            coreset=store_path_map[am.DatastoreFileType.CORESET],
            start_frame_indices=[0],
            img_end_indices=[len(self._filter_input.file_metadata_list) - 1],
        )

        self._dsp_dataset_api.put_dataset_partition_update(
            partition_id=partition_id,
            session_id=self._filter_input.session_id,
            pipeline_id=(
                self._filter_input.pipeline_tables_info.get_pipeline_id()
            ),
            dataset_id=self._filter_input.dataset_id,
            pipeline_partition_create_request=partition_create_request,
        )

    def _insert_entries_to_pipeline_tables(
        self,
        store_path_map: Dict[am.DatastoreFileType, str],
        partition_start: int,
        partition_end: int,
    ):
        blobs_table_insert_values: List[List[str]] = [
            [
                partition_start,
                partition_end,
                self._filter_input.workflow_id,
                self._filter_input.session_id,
                store_path_map[am.DatastoreFileType.BLOBS],
            ]
        ]

        summary_table_insert_values: List[List[str]] = [
            [
                partition_start,
                partition_end,
                self._filter_input.workflow_id,
                self._filter_input.session_id,
                store_path_map[am.DatastoreFileType.CORESET],
                store_path_map[am.DatastoreFileType.PROJECTIONS],
                store_path_map[am.DatastoreFileType.SKETCH],
                store_path_map[am.DatastoreFileType.THUMBNAIL],
            ]
        ]

        # populate insert values for primary table
        primary_table_insert_values: List[List[str]] = []
        for file_info in self._filter_input.file_metadata_list:
            primary_table_insert_values.append(
                [
                    partition_start,
                    partition_end,
                    self._filter_input.workflow_id,
                    self._filter_input.session_id,
                    file_info.frame_idx_in_blob,
                    file_info.blob_idx_in_partition,
                    file_info.file_path,
                    datetime.now(),
                    file_info.file_id,
                    file_info.frame_idx_in_file,
                    file_info.file_name,
                    file_info.total_frames_in_file,
                ]
            )

        pipeline_tables_info = self._filter_input.pipeline_tables_info
        # Insert entries to db
        for abs_table_name, columns, values in [
            (
                pipeline_tables_info.get_blobs_abs_table(),
                Constants.BLOB_TABLE_COLUMNS,
                blobs_table_insert_values,
            ),
            (
                pipeline_tables_info.get_summary_abs_table(),
                Constants.SUMMARY_TABLE_COLUMNS,
                summary_table_insert_values,
            ),
            (
                pipeline_tables_info.get_primary_abs_table(),
                Constants.PRIMARY_TABLE_COLUMNS,
                primary_table_insert_values,
            ),
        ]:
            self._ccs_api.insert_data_in_catalog_table(
                am.InsertCatalogData(
                    dataset_id=self._filter_input.dataset_id,
                    columns=columns,
                    values=values,
                    abs_table_name=abs_table_name,
                )
            )
