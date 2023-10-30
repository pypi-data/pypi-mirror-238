import tempfile
from typing import List, Optional, Tuple

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
from pyakri_de_filters.data_ingest_filter.data_ingest_filter_wrapper import (
    DataIngestWrapper,
)

from akride import logger
from akride._utils.catalog.catalog_tables_helper import CatalogTablesHelper
from akride._utils.catalog.pipeline_tables_info import PipelineTablesInfo
from akride._utils.class_executor import ClassExecutor
from akride._utils.progress_manager.manager import (
    ProgressManager,
    ProgressStep,
)
from akride._utils.workflow_helper import WorkflowHelper
from akride.core._filters.enums import FilterTypes
from akride.core._filters.partitioners.ingest_partitioner_filter import (
    IngestPartitionerFilter,
)
from akride.core._filters.partitioners.process_partitioner_filter import (
    ProcessPartitionerFilter,
    ProcessTokenInfo,
)
from akride.core._filters.sink.models import SinkWriterFilterInput
from akride.core._filters.sink.sink_writer_filter import SinkWriterFilter
from akride.core.constants import Constants
from akride.core.exceptions import ServerError


class PipelineExecutor:
    INGEST_WORKFLOW_PROGRESS_WEIGHTAGE = 1
    PROCESS_WORKFLOW_PROGRESS_WEIGHTAGE = 3

    """Class to run ingest and process workflow."""

    def __init__(
        self,
        dataset: am.DataSetJSON,
        data_dir: str,
        catalog_tables_helper: CatalogTablesHelper,
        pipeline_filters_info_list: List[am.AkriSDKWorkflowResponse],
        workflow_api: am.WorkflowsApi,
        dsp_dataset_api: dsp.DatasetApi,
        ccs_api: am.CcsApi,
        progress_manager: ProgressManager,
    ):
        self._dataset = dataset
        self._data_dir = data_dir
        self._catalog_tables_helper = catalog_tables_helper
        self._pipeline_filters_info_list = pipeline_filters_info_list
        self._workflow_api = workflow_api
        self._dsp_dataset_api = dsp_dataset_api
        self._ccs_api = ccs_api

        self._progress_manager = progress_manager

    def run(self):
        logger.info("Ingestion in progress!")
        self._progress_manager.set_msg("Ingestion in progress!")

        ingest_step: ProgressStep = self._progress_manager.register_step(
            "Ingest", weight=self.INGEST_WORKFLOW_PROGRESS_WEIGHTAGE
        )
        process_step: ProgressStep = self._progress_manager.register_step(
            "Process", weight=self.PROCESS_WORKFLOW_PROGRESS_WEIGHTAGE
        )

        self._run_ingest_workflow(ingest_step=ingest_step)

        self._run_process_workflow(process_step=process_step)

        self._progress_manager.set_msg("Ingestion completed!")
        logger.info("Ingestion completed!")

    def _run_ingest_workflow(self, ingest_step: ProgressStep):
        session_id, workflow_id = WorkflowHelper.get_session_and_workflow_id(
            workflow_id_prefix="reg", dataset_id=self._dataset.id
        )

        IngestPartitionerFilter(
            dataset=self._dataset,
            data_dir=self._data_dir,
            session_id=session_id,
            workflow_id=workflow_id,
            dataset_tables_info=(
                self._catalog_tables_helper.get_dataset_tables_info()
            ),
            ccs_api=self._ccs_api,
            ingest_step=ingest_step,
        ).run()

    def _run_process_workflow(self, process_step):
        # Run process workflow
        session_id, workflow_id = WorkflowHelper.get_session_and_workflow_id(
            workflow_id_prefix="process", dataset_id=self._dataset.id
        )

        for index, pipeline_info in enumerate(
            self._catalog_tables_helper.get_pipelines()
        ):
            pipeline_filters_info = self._pipeline_filters_info_list[index]
            self._run_process_workflow_per_pipeline(
                pipeline_info=pipeline_info,
                pipeline_filters_info=pipeline_filters_info,
                session_id=session_id,
                workflow_id=workflow_id,
                process_step=process_step,
            )

    def _run_process_workflow_per_pipeline(
        self,
        pipeline_info: PipelineTablesInfo,
        pipeline_filters_info: am.AkriSDKWorkflowResponse,
        session_id: str,
        workflow_id: str,
        process_step: ProgressStep,
    ):
        dataset_tables_info = (
            self._catalog_tables_helper.get_dataset_tables_info()
        )
        process_partitioner_filter = ProcessPartitionerFilter(
            dataset_id=self._dataset.id,
            pipeline_info=pipeline_info,
            partitioned_abs_table=(
                dataset_tables_info.get_partitioned_abs_table()
            ),
            ccs_api=self._ccs_api,
            process_step=process_step,
        )

        for process_token_info in process_partitioner_filter.run():
            # Create temp folder per token
            with tempfile.TemporaryDirectory() as tmp_dir:
                (
                    _,
                    metadata_output_dir,
                ) = self._prepare_partitioner_and_metadata_dir(
                    process_token_info=process_token_info,
                    tmp_dir=tmp_dir,
                )

                # Map to get filter output directory by filter type
                filters_output_dir_map: dict = (
                    self._get_filters_output_dir_map(
                        parent_dir=tmp_dir,
                        token_number=process_token_info.token_number,
                    )
                )

                filter_execution_order_list: List[
                    dict
                ] = self._get_filter_execution_order_list(
                    pipeline_filters_info=pipeline_filters_info,
                    filters_output_dir_map=filters_output_dir_map,
                )
                for sdk_details in filter_execution_order_list:
                    self._run_filter(
                        filter_details=sdk_details["filter_details"],
                        src_dir=sdk_details["src_dir"],
                        dst_dir=sdk_details["dst_dir"],
                        filter_type=sdk_details["filter_type"],
                    )

                # init params for data ingest would be same as featurizer
                data_ingest_init_params = (
                    pipeline_filters_info.featurizer.init_params
                )
                data_ingest_output_dir = filters_output_dir_map[
                    FilterTypes.DataIngest
                ]
                # Run Data ingest filter
                with tempfile.NamedTemporaryFile(dir=tmp_dir) as fp:
                    logger.debug("Data ingestion filter is in progress!")

                    ingest_filter = DataIngestWrapper()
                    ingest_filter.init(**data_ingest_init_params)

                    # Featurizer output will be input for data ingest filter
                    ingest_src_dir = filters_output_dir_map[
                        FilterTypes.Featurizer
                    ]

                    ingest_filter.run(
                        src_dir=ingest_src_dir,
                        dst_dir=data_ingest_output_dir,
                        tmp_file=fp.name,
                    )
                    logger.debug(
                        "Data ingestion filter completed successfully!"
                    )

                thumbnail_aggregator_output_dir = filters_output_dir_map[
                    FilterTypes.ThumbnailAggregator
                ]
                # Run sink writer filter
                logger.debug("Sync filter is in progress!")
                SinkWriterFilter(
                    filter_input=SinkWriterFilterInput(
                        dataset_id=self._dataset.id,
                        pipeline_tables_info=pipeline_info,
                        workflow_id=workflow_id,
                        session_id=session_id,
                        file_metadata_list=(process_token_info.file_info_list),
                    ),
                    workflow_api=self._workflow_api,
                    dsp_dataset_api=self._dsp_dataset_api,
                    ccs_api=self._ccs_api,
                ).run_from_input_dir(
                    coreset_dir=f"{data_ingest_output_dir}/{DataIngestWrapper.DEST_CORESET_SUB_DIR}",  # noqa
                    projections_dir=f"{data_ingest_output_dir}/{DataIngestWrapper.DEST_PROJECTIONS_SUB_DIR}",  # noqa
                    sketch_dir=f"{data_ingest_output_dir}/{DataIngestWrapper.DEST_SKETCH_SUB_DIR}",  # noqa
                    thumbnail_dir=thumbnail_aggregator_output_dir,
                    blobs_dir=metadata_output_dir,
                )

                process_step.increment_processed_steps(completed=1)

            #  Update dsp session
            session_create_request = dsp.PipelineSessionCreateRequest(
                status="COMPLETE"
            )
            self._dsp_dataset_api.put_dataset_session(
                session_id=session_id,
                pipeline_id=pipeline_info.get_pipeline_id(),
                dataset_id=self._dataset.id,
                pipeline_session_create_request=session_create_request,
            )

    @classmethod
    def _prepare_partitioner_and_metadata_dir(
        cls, process_token_info: ProcessTokenInfo, tmp_dir: str
    ) -> Tuple[str, str]:
        token_number = process_token_info.token_number
        partitioner_parent_output_dir = cls._get_output_dir(
            par_dir=tmp_dir, filter_type=FilterTypes.Partitioner
        )

        # Prepare partitioner output directory
        partitioner_output_dir = (
            f"{partitioner_parent_output_dir}/{token_number}/o1"
        )
        ProcessPartitionerFilter.prepare_output_dir(
            files=process_token_info.files, output_dir=partitioner_output_dir
        )

        # Prepare metadata dir
        metadata_output_dir = (
            f"{partitioner_parent_output_dir}/metadata/{token_number}/o1"
        )
        ProcessPartitionerFilter.prepare_metadata_dir(
            filemeta_list=process_token_info.file_meta_list,
            metadata_dir=metadata_output_dir,
        )
        return partitioner_output_dir, metadata_output_dir

    @classmethod
    def _get_filter_execution_order_list(
        cls,
        pipeline_filters_info: am.AkriSDKWorkflowResponse,
        filters_output_dir_map: dict,
    ) -> List[dict]:
        """
        :param pipeline_filters_info: List of Filter info that attached to
            pipeline
        :return: List[dict]:
                List of required details to run a filter where src_dir value
                refer from where to read and dst_dir value refer where to write
        """

        filter_execution_order_list = [
            {
                "filter_type": FilterTypes.Preprocessor,
                "src_dir": filters_output_dir_map[FilterTypes.Partitioner],
                "filter_details": pipeline_filters_info.pre_processor,
                "dst_dir": filters_output_dir_map[FilterTypes.Preprocessor],
            },
            {
                "filter_type": FilterTypes.Featurizer,
                "src_dir": filters_output_dir_map[FilterTypes.Preprocessor],
                "filter_details": pipeline_filters_info.featurizer,
                "dst_dir": filters_output_dir_map[FilterTypes.Featurizer],
            },
            {
                "filter_type": FilterTypes.Thumbnail,
                "src_dir": filters_output_dir_map[FilterTypes.Partitioner],
                "filter_details": pipeline_filters_info.thumbnail,
                "dst_dir": filters_output_dir_map[FilterTypes.Thumbnail],
            },
            {
                "filter_type": FilterTypes.ThumbnailAggregator,
                "src_dir": filters_output_dir_map[FilterTypes.Thumbnail],
                "filter_details": (Constants.THUMBNAIL_AGGREGATOR_SDK_DETAILS),
                "dst_dir": filters_output_dir_map[
                    FilterTypes.ThumbnailAggregator
                ],
            },
        ]

        return filter_execution_order_list

    @classmethod
    def _get_filters_output_dir_map(
        cls, parent_dir: str, token_number: int
    ) -> dict:
        output_dir_map = {}
        for filter_type in FilterTypes:
            output_dir_map[filter_type] = cls._get_output_dir(
                par_dir=parent_dir,
                token_number=token_number,
                filter_type=filter_type,
            )
        return output_dir_map

    @staticmethod
    def _get_output_dir(
        par_dir: str,
        filter_type: FilterTypes,
        token_number: Optional[int] = None,
    ) -> str:
        output_dir = f"{par_dir}/{filter_type.value}/outputs"
        if token_number:
            output_dir = f"{output_dir}/{token_number}/o1"
        return output_dir

    @staticmethod
    def _run_filter(
        filter_details: am.AkriSDKFilterDetails,
        src_dir: str,
        dst_dir: str,
        filter_type: FilterTypes,
    ):
        try:
            logger.debug(f"{filter_type.value} filter is in progress!")
            module = filter_details.module
            class_name = filter_details.class_name
            run_method = filter_details.run_method
            init_method = filter_details.init_method
            cleanup_method = filter_details.cleanup_method
            init_params = {}
            if filter_details.init_params:
                init_params = filter_details.init_params

            class_executor = ClassExecutor(
                module_path=module, klass_name=class_name
            )

            if init_method:
                class_executor.call_method(init_method, **init_params)

            run_method_params = {"src_dir": src_dir, "dst_dir": dst_dir}
            class_executor.call_method(run_method, **run_method_params)

            if cleanup_method:
                class_executor.call_method(method_name=cleanup_method)
            logger.debug(f"{filter_type.value} filter completed successfully!")
        except Exception as ex:
            logger.error(f"Failed to run sdk filter due to {ex}")
            raise ServerError(f"Failed to run sdk filter due to {ex}")
