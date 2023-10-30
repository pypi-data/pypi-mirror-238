from typing import List

import akridata_akrimanager_v2 as am

from akride._utils.catalog.dataset_tables_info import DatasetTablesInfo
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo


class CatalogTablesHelper:
    def __init__(self, catalog_tables_resp: am.CatalogTableResponse):
        self._dataset_tables_info = DatasetTablesInfo(
            dataset_tables=catalog_tables_resp.dataset_tables
        )

        self._pipelines = [
            PipelineTablesInfo(pipeline_table=pipeline)
            for pipeline in catalog_tables_resp.pipelines
        ]

    def get_pipelines(self) -> List[PipelineTablesInfo]:
        return self._pipelines

    def get_dataset_tables_info(self) -> DatasetTablesInfo:
        return self._dataset_tables_info
