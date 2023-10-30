from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp

from akride import logger
from akride._utils.background_task_helper import BackgroundTask
from akride._utils.catalog.catalog_tables_helper import CatalogTablesHelper
from akride._utils.exception_utils import translate_api_exceptions
from akride._utils.pipeline.pipeline_helper import PipelineHelper
from akride._utils.progress_manager.manager import ProgressManager
from akride.core._entity_managers.catalog_manager import CatalogManager
from akride.core._entity_managers.manager import Manager
from akride.core._pipeline_executor import PipelineExecutor
from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity
from akride.core.enums import BackgroundTaskType, DataType, FeaturizerType
from akride.core.exceptions import ServerError, UserError
from akride.core.models.catalog_details import CatalogDetails
from akride.core.types import ClientManager


class DatasetManager(Manager):
    """
    Class Managing Dataset related operations on DataExplorer
    """

    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.dataset_api = am.DatasetsApi(cli_manager.am_client)
        self.catalog_api: am.CatalogApi = am.CatalogApi(cli_manager.am_client)
        self.pipeline_api: am.PipelineApi = am.PipelineApi(
            cli_manager.am_client
        )
        self.workflow_api: am.WorkflowsApi = am.WorkflowsApi(
            cli_manager.am_client
        )
        self.dsp_dataset_api: dsp.DatasetApi = dsp.DatasetApi(
            cli_manager.dsp_client
        )
        self.ccs_api: am.CcsApi = am.CcsApi(cli_manager.am_client)
        self._catalogs = CatalogManager(cli_manager)

    @translate_api_exceptions
    def create_entity(self, spec: Dict[str, Any]) -> Entity:
        """
        Creates a new dataset.

        Parameters
        ----------
        spec : Dict[str, Any]
            The dataset spec.

        Returns
        -------
        Entity
            The created dataset
        """
        return self._create_dataset(**spec)

    @translate_api_exceptions
    def delete_entity(self, entity: Entity) -> bool:
        """
        Deletes an entity.

        Parameters
        ----------
        entity : Entity
            The entity object to delete.

        Returns
        -------
        bool
            Indicates whether this entity was successfully deleted
        """
        dataset_id = entity.get_id()
        api_response = self.dataset_api.delete_dataset(dataset_id)
        return api_response.success == "True"

    def _create_dataset(
        self,
        dataset_name: str,
        dataset_namespace: str = "default",
        data_type: DataType = DataType.IMAGE,
        glob_pattern: str = "*(png|jpg|gif|jpeg|tiff|tif|bmp)",
        overwrite: bool = False,
    ) -> Dataset:
        """
        Method for creating a new dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the new dataset.
        dataset_namespace : str, optional
            The namespace for the dataset, by default 'default'.
        data_type : DataType, optional
            The type of data to store in the dataset, by default
            DataType.IMAGE.
        glob_pattern : str, optional
            The glob pattern for the dataset, by default
            '*(png|jpg|gif|jpeg|tiff|tif|bmp)'.
        overwrite : bool, optional
            Overwrite if a dataset with the same name exists.

        Returns
        -------
        Dataset
            The newly created dataset.
        """
        logger.debug(
            "Creating dataset %s in %s namespace of data_type %s, with file"
            "pattern %s",
            dataset_name,
            dataset_namespace,
            data_type,
            glob_pattern,
        )
        logger.debug("overwrite set to %s", overwrite)
        if overwrite:
            raise NotImplementedError

        dataset_spec = {"access_type": "default", "glob": glob_pattern}

        containers = {"source": {"local": True}, "sink": {"internal": True}}
        dataset_type = "basic"
        am_dataset = am.DataSet(
            dataset_name=dataset_name,
            namespace=dataset_namespace,
            type=dataset_type,
            data_type=data_type.value,
            containers=containers,
            dataset_spec=dataset_spec,
        )
        api_response = self.dataset_api.create_new_dataset(am_dataset)
        return self.get_entity_by_id(entity_id=api_response.dataset_id)

    def _attach_pipeline(
        self,
        featurizer_type: FeaturizerType,
        dataset_id: str,
        data_type: DataType,
    ) -> None:
        """
        Attaches a pipeline based on featurizer_type
        Parameters
        ----------
        featurizer_type: Type of featurizer to be used for attachment
        dataset_id : str
            dataset_id to attach.
        data_type : DataType
            data type of dataset

        Returns
        -------
        None
        """
        pipeline_internal_id = PipelineHelper.get_pipeline_internal_id(
            featurizer_type=featurizer_type, data_type=data_type
        )

        pipeline: am.PipelineItem = self._get_internal_pipeline_details(
            pipeline_internal_id=pipeline_internal_id
        )

        if not pipeline:
            raise ServerError(
                f"Pipeline details not found for featurizer "
                f"{featurizer_type.value} and data type {data_type}!"
            )

        # Create attachment
        self.pipeline_api.attach_pipeline_to_datasets(
            pipeline_id=pipeline.pipeline_id,
            pipeline_attach_body=am.PipelineAttachBody(
                dataset_ids=[dataset_id]
            ),
        )

    def _get_internal_pipeline_details(
        self, pipeline_internal_id: int
    ) -> Optional[am.PipelineItem]:
        # Get pipeline filter by pipeline_internal_id
        pipelines_resp: am.Pipelines = self.pipeline_api.get_all_pipelines(
            filter_by_internal_id=pipeline_internal_id
        )

        internal_pipeline = None
        if pipelines_resp.pipelines:
            internal_pipeline = pipelines_resp.pipelines[0]

        return internal_pipeline

    @translate_api_exceptions
    def ingest_dataset(
        self,
        dataset: Dataset,
        data_directory: str,
        featurizer_type: FeaturizerType = FeaturizerType.FULL_IMAGE,
        catalog_details: Optional[CatalogDetails] = None,
    ) -> BackgroundTask:
        """
        Starts an asynchronous ingest task for the specified dataset.
        Attaches a pipeline based on featurizer_type and executes the pipeline

        Parameters
        ----------
        dataset : Dataset
            The dataset to ingest.
        data_directory : str
            The path to the directory containing the dataset files.
        featurizer_type: Type of featurizer to be used
        catalog_details: Optional[CatalogDetails]
            parameters details for creating a catalog

        Returns
        -------
        BackgroundTask
            A task object
        """
        # Check to avoid concurrent ingestion of same dataset.
        if self.client_manager.background_task_manager.is_task_running(
            entity_id=dataset.get_id(),
            task_type=BackgroundTaskType.DATASET_INGESTION,
        ):
            raise UserError("Ingestion already in progress!")

        if catalog_details:
            self._catalogs.import_catalog(
                dataset=dataset,
                csv_file_path=catalog_details.catalog_csv_file,
                table_name=catalog_details.table_name,
            )

        self._attach_pipeline(
            data_type=DataType(dataset.info.data_type),
            dataset_id=dataset.get_id(),
            featurizer_type=featurizer_type,
        )

        dataset_json = self._get_dataset_json(
            dataset_id=dataset.get_id(), version=dataset.info.latest_version
        )

        catalog_tables_resp: am.CatalogTableResponse = (
            self.catalog_api.get_catalog_tables(dataset_id=dataset.get_id())
        )
        catalog_tables_helper = CatalogTablesHelper(
            catalog_tables_resp=catalog_tables_resp
        )

        # Get filters info for all pipelines
        pipeline_filters_info_list: List[am.AkriSDKWorkflowResponse] = []
        for pipeline in catalog_tables_helper.get_pipelines():
            pipeline_filters_info_list.append(
                self.workflow_api.get_akrisdk_details(
                    dataset_id=dataset.get_id(),
                    pipeline_id=pipeline.get_pipeline_id(),
                )
            )

        workflow_params = {
            "dataset_json": dataset_json,
            "data_dir": data_directory,
            "catalog_tables_helper": catalog_tables_helper,
            "pipeline_filters_info_list": pipeline_filters_info_list,
            "workflow_api": self.workflow_api,
            "dsp_dataset_api": self.dsp_dataset_api,
            "ccs_api": self.ccs_api,
        }

        task = self.client_manager.background_task_manager.start_task(
            entity_id=dataset.get_id(),
            task_type=BackgroundTaskType.DATASET_INGESTION,
            target_function=self._run_workflow,
            **workflow_params,
        )

        return task

    @staticmethod
    def _run_workflow(
        progress_manager: ProgressManager,
        dataset_json: am.DataSetJSON,
        data_dir: str,
        catalog_tables_helper: CatalogTablesHelper,
        pipeline_filters_info_list: List[am.AkriSDKWorkflowResponse],
        workflow_api: am.WorkflowsApi,
        dsp_dataset_api: dsp.DatasetApi,
        ccs_api: am.CcsApi,
    ):
        PipelineExecutor(
            dataset=dataset_json,
            data_dir=data_dir,
            catalog_tables_helper=catalog_tables_helper,
            pipeline_filters_info_list=pipeline_filters_info_list,
            workflow_api=workflow_api,
            dsp_dataset_api=dsp_dataset_api,
            ccs_api=ccs_api,
            progress_manager=progress_manager,
        ).run()

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[Dataset]:
        """
        Retrieves information about datasets that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields: search_key : str
                    Filter across fields like dataset id, and dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing datasets.
        """
        attributes = attributes.copy()
        if "data_type" in attributes:
            attributes["filter_by_datatype"] = attributes["data_type"]
            del attributes["data_type"]
        if "search_key" in attributes:
            attributes["search_str"] = attributes["search_key"]
            del attributes["search_key"]
        api_response = self.dataset_api.list_datasets(**attributes)
        dataset_list = [Dataset(info) for info in api_response.datasets]
        return dataset_list

    @translate_api_exceptions
    def get_entity_by_id(self, entity_id: str) -> Optional[Dataset]:
        """
        Retrieves information about dataset for the given ID.

        Parameters
        ----------
        entity_id: str
            Dataset Id

        Returns
        -------
        Entity
            Entity object representing dataset.
        """
        dataset_info: am.DataSetsItem = self.dataset_api.get_dataset_info(
            dataset_id=entity_id
        )

        dataset = None
        if dataset_info:
            dataset = Dataset(info=dataset_info)
        return dataset

    def _get_dataset_json(
        self, dataset_id: str, version: str
    ) -> am.DataSetJSON:
        """
        Get DataSetJSON object for dataset with given version..

        Parameters
        ----------
        dataset_id: str
            Dataset Id

        Returns
        -------
        DataSetJSON
            Dataset json details.
        """
        return self.dataset_api.get_dataset_json(
            dataset_id=dataset_id, version=version
        )
