import math
import os
from dataclasses import dataclass
from typing import Any, List, Tuple

import akridata_akrimanager_v2 as am
import pandas as pd
from pyakri_de_filters.utils.arrow_utils import write_arrow_from_df
from pyakri_de_filters.utils.file_utils import create_directory

from akride import logger
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride._utils.file_utils import copy_files_to_dir, get_file_name_from_path
from akride._utils.progress_manager.manager import ProgressStep
from akride.core._filters.partitioners.models import ProcessFileInfo
from akride.core._filters.partitioners.partitioner_filter import (
    PartitionerFilter,
)
from akride.core.constants import Constants


@dataclass
class ProcessTokenInfo:
    file_info_list: List[ProcessFileInfo]
    file_meta_list: List[List[Any]]
    files: List[str]
    token_number: int
    total_num_tokens: int


class ProcessPartitionerFilter(PartitionerFilter):
    DF_COLUMNS = ["file_id", "filename", "frame_idx_in_file"]
    DEST_ARROW_FILE = "0-1"

    def __init__(
        self,
        dataset_id: str,
        partitioned_abs_table: str,
        pipeline_info: PipelineTablesInfo,
        ccs_api: am.CcsApi,
        process_step: ProgressStep,
    ):
        super().__init__(dataset_id=dataset_id, ccs_api=ccs_api)
        self._pipeline_info = pipeline_info
        self._partitioned_abs_table = partitioned_abs_table

        self._process_step = process_step

    def run(self):
        pipeline_name = self._pipeline_info.get_pipeline_name()
        logger.debug(
            f"Getting un-processed files for pipeline {pipeline_name}"
        )
        return self.get_tokenized_unprocessed_files()

    def get_tokenized_unprocessed_files(self):
        partition_start = 0
        primary_table_name = self._pipeline_info.get_primary_abs_table()

        next_file_id = self._get_next_file_id(primary_table_name)

        # Tokenize and return metadata details
        token_count = self._get_token_count(
            primary_table_name=primary_table_name
        )

        self._process_step.set_total_steps(token_count)

        token_index = 0
        while token_index < token_count:
            files = self._get_unprocessed_files(primary_table_name)
            token_number = token_index + 1

            (
                file_info_list,
                filemeta_arr_list,
            ) = self._prepare_file_meta_and_file_info_list(
                files=files,
                partition_start=partition_start,
                file_id=next_file_id,
            )

            yield ProcessTokenInfo(
                file_info_list=file_info_list,
                file_meta_list=filemeta_arr_list,
                token_number=token_number,
                total_num_tokens=token_count,
                files=files,
            )

            partition_start += Constants.PARTITION_SIZE
            next_file_id += Constants.PROCESS_WF_TOKEN_SIZE
            token_index += 1

    @staticmethod
    def prepare_output_dir(files: List[str], output_dir: str):
        copy_files_to_dir(files, output_dir)

    def _get_token_count(self, primary_table_name: str) -> int:
        response: am.CCSFetchUnprocessedFileCntResponse = (
            self.ccs_api.fetch_unprocessed_file_count(
                dataset_id=self.dataset_id,
                primary_table=primary_table_name,
                partition_table=self._partitioned_abs_table,
            )
        )
        token_count = math.ceil(
            response.file_count / Constants.PROCESS_WF_TOKEN_SIZE
        )
        return token_count

    def _get_unprocessed_files(self, primary_table_name: str) -> List[str]:
        response: am.CCSFetchUnprocessedFileNamesResponse = (
            self.ccs_api.fetch_unprocessed_file_names(
                dataset_id=self.dataset_id,
                primary_table=primary_table_name,
                partition_table=self._partitioned_abs_table,
                batch_size=Constants.PROCESS_WF_TOKEN_SIZE,
            )
        )
        return response.file_names

    @classmethod
    def _prepare_file_meta_and_file_info_list(
        cls,
        files: List[str],
        partition_start: int,
        file_id: int,
    ) -> Tuple[List[ProcessFileInfo], List[List[Any]]]:
        filemeta_arr_list = []
        file_info_list = []
        frame_idx_in_blob = 0
        partition_end = partition_start + Constants.PARTITION_SIZE - 1
        frame_idx_in_file = 0

        for file in files:
            file_info_list.append(
                ProcessFileInfo(
                    file_path=file,
                    file_id=file_id,
                    frame_idx_in_blob=frame_idx_in_blob,
                    partition_start=partition_start,
                    partition_end=partition_end,
                    file_name=get_file_name_from_path(file),
                    frame_idx_in_file=frame_idx_in_file,
                )
            )
            filemeta_arr_list.append([file_id, file, frame_idx_in_file])
            frame_idx_in_blob += 1
            file_id += 1

        return file_info_list, filemeta_arr_list

    @classmethod
    def prepare_metadata_dir(
        cls, metadata_dir: str, filemeta_list: List[List[Any]]
    ):
        data_frame_to_write = pd.DataFrame(
            filemeta_list, columns=cls.DF_COLUMNS
        )
        create_directory(metadata_dir)

        dst_arrow_file_path = os.path.join(metadata_dir, cls.DEST_ARROW_FILE)

        write_arrow_from_df(data_frame_to_write, dst_arrow_file_path)

    def _get_next_file_id(self, primary_table_name: str) -> int:
        response: am.CCSFetchMaxFileIdPartitionIdResponse = (
            self.ccs_api.fetch_max_fileid_partitionid(
                dataset_id=self.dataset_id,
                abs_table_name=primary_table_name,
                is_fetch_max_partition=False,
            )
        )
        max_file_id = response.max_file_id
        next_file_id = 0 if max_file_id is None else max_file_id + 1
        return next_file_id
