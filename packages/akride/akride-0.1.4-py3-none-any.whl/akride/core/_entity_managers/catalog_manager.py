import os
import types
from collections import defaultdict
from typing import Any, Dict, List, Optional

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
import pandas as pd
import requests

from akride import logger
from akride._utils.exception_utils import translate_api_exceptions
from akride.core._entity_managers.manager import Manager
from akride.core.entities.catalogs import Catalog
from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity
from akride.core.exceptions import ServerError
from akride.core.types import ClientManager, SampleInfoList


class CatalogManager(Manager):
    """Class managing external catalog operations on DataExplorer"""

    def __init__(self, cli_manager: ClientManager):
        super().__init__(cli_manager)
        self.catalog_api = am.CatalogApi(cli_manager.am_client)
        self.ext_catalog_api = am.ExternalCatalogApi(cli_manager.am_client)
        self.catalog_source_api = dsp.CatalogSourceTagApi(
            cli_manager.dsp_client
        )

    @translate_api_exceptions
    def create_entity(self, spec: Dict[str, Any]) -> Optional[Catalog]:
        """
        Creates a new catalog.

        Parameters
        ----------
        spec : Dict[str, Any]
            The catalog spec.

        Returns
        -------
        Entity
            The created catalog
        """
        return self._create_catalog(**spec)

    def _create_catalog(self, **kwargs) -> Optional[Catalog]:
        logger.debug("Got %s", kwargs)
        # TODO: Implement this
        return None

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
        dataset_id = entity.dataset_id
        delete_request = am.DeleteCatalogTableRequest(dataset_id, [entity.id])
        api_response = self.catalog_api.delete_catalog_table(delete_request)
        return api_response.message == "Table deleted successfully."

    @translate_api_exceptions
    def get_entities(self, attributes: Dict[str, Any]) -> List[Catalog]:
        """
        Retrieves information about external catalogs.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields:
                name : str
                    filter by catalog name
                status : str
                    filter by catalog status, can be one of
                    "active","inactive", "refreshing", "offline",
                    "invalid-config"

        Returns
        -------
        List[Entity]
            A list of Entity objects representing external catalogs.
        """
        logger.debug("got attributes %s", attributes)
        valid_keys = ["name", "status"]
        invalid_keys = [
            key for key in attributes.keys() if key not in valid_keys
        ]
        if invalid_keys:
            raise ValueError(f"Invalid attributes: {', '.join(invalid_keys)}")

        api_response: am.ListCatalogsResponse = (
            self.ext_catalog_api.list_external_catalogs()
        )  # type: ignore
        if api_response.response and len(api_response.response) == 0:
            return []
        filtered_catalogs = api_response.response
        assert filtered_catalogs is not None
        if attributes:
            for key, val in attributes.items():
                filtered_catalogs = [
                    obj
                    for obj in filtered_catalogs  # type: ignore
                    if getattr(obj, key) == val
                ]
        ext_catalog_list = [Catalog(info) for info in filtered_catalogs]
        return ext_catalog_list

    @translate_api_exceptions
    def get_catalogs(
        self, dataset: Dataset, attributes: Dict[str, Any] = {}
    ) -> List[Entity]:
        """
        Retrieves information about entities that have the given attributes.

        Parameters
        ----------
        dataset: Dataset
            The dataset to import the catalog into.
        attributes: Dict[str, Any]
            The filter specification.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing catalogs.
        """
        logger.debug("got attributes %s", attributes)
        api_response: am.CatalogTableResponse = (
            self.catalog_api.get_catalog_tables(dataset.get_id())
        )  # type: ignore

        # TODO: filter according to the attributes argument
        catalog_list = [
            Catalog(types.SimpleNamespace(id=table.abs_name, name=table.name))
            for table in api_response.dataset_tables
        ]

        for catalog in catalog_list:
            catalog.dataset_id = dataset.id
        return catalog_list

    @translate_api_exceptions
    def get_catalog_by_name(
        self, dataset: Dataset, name: str
    ) -> Optional[Entity]:
        """
        Retrieves an entity with the given name.

        Parameters
        ----------
        dataset: Dataset
            The dataset to import the catalog into.
        name : str
            The name of the catalog to retrieve.

        Returns
        -------
        Entity
            The Entity object.
        """
        attrs = {"search_key": name}
        entity_list = self.get_catalogs(dataset, attrs)
        if entity_list is None:
            return None

        for entity in entity_list:
            if entity.name == name:
                return entity
        return None

    @translate_api_exceptions
    def get_catalog_tags(self, samples: SampleInfoList) -> pd.DataFrame:
        """
        Retrieves the catalog tags corresponding to the samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve catalog tags for.

        Returns
        -------
        pd.DataFrame
            A dataframe of catalog tags.
        """
        job_id = samples.job_id
        points = ",".join(map(str, samples.get_point_ids()))
        api_response = self.catalog_source_api.get_request_catalog_tag_source(
            rid=job_id, points=points
        )
        columns = [item.column_name for item in api_response.column_meta]
        data = api_response.data

        # Convert from list of list of lists to a list of lists
        rows = [row for data_rows in data for row in data_rows.tags]

        # Extract the values for every row
        tags = [[item.value for item in tags] for tags in rows]
        return pd.DataFrame(tags, columns=columns)

    @translate_api_exceptions
    def import_catalog(
        self,
        dataset: Dataset,
        table_name: str,
        csv_file_path: str,
    ) -> bool:
        """
        Imports a catalog into a dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing the catalog data.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        sql_mapping = defaultdict(lambda: "VARCHAR(255)")
        sql_mapping.update(
            {
                "object": "VARCHAR(255)",
                "int64": "BIGINT",
                "float64": "DOUBLE",
                "datetime64[ns]": "DATETIME",
                "int32": "INT",
                "float32": "FLOAT",
                "timedelta[ns]": "TIME",
            }
        )
        df = pd.read_csv(csv_file_path)
        col_list = [
            {"name": col_name, "type": sql_mapping[str(col_type)]}
            for col_name, col_type in zip(df.columns, df.dtypes)
        ]
        table = am.ExternalCatalogTable(
            name=table_name,
            columns=col_list,
            description=table_name,
            visualizable=False,
        )
        catalog_request = am.CreateCatalogTableRequest(
            dataset_id=dataset.id, catalog_table=table
        )
        self.catalog_api.create_catalog_table(catalog_request)

        return self.add_to_catalog(dataset, table_name, csv_file_path, df)

    @translate_api_exceptions
    def add_to_catalog(
        self,
        dataset: Dataset,
        table_name: str,
        csv_file_path: str,
        df: pd.DataFrame = None,
    ) -> bool:
        """
        Adds new items to an existing catalog.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing new catalog data.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        # upload CSV file to S3
        file_name = os.path.basename(csv_file_path)
        file_id = self._upload_to_s3(
            table_name, dataset.get_id(), file_name, csv_file_path
        )

        # create an import job
        if df is None:
            df = pd.read_csv(csv_file_path)
        header_map = [
            {"header_name": col_name, "position": i}
            for i, col_name in enumerate(df.columns)
        ]
        file_list_entry = {
            "file_id": file_id,
            "file_name": file_name,
            "url": None,
            "delimiter": ",",
            "header_map": header_map,
        }
        import_request = am.ImportCatalogJobRequest(
            table_name=table_name,
            dataset_id=dataset.id,
            file_list=[file_list_entry],
        )
        import_response = self.catalog_api.import_catalog_job(import_request)
        return import_response.job_id is not None

    def _upload_to_s3(
        self, table_name: str, dataset_id: str, file_name: str, file_path: str
    ):
        url_request = am.GetPreSignedUrlRequest(
            file_list=[file_name], table_name=table_name, dataset_id=dataset_id
        )
        url_response = self.catalog_api.get_pre_signed_url(url_request)

        pre_signed_url_resp = url_response["presignedurls"][0]
        presigned_url = pre_signed_url_resp["url"]
        fields = pre_signed_url_resp["fields"]
        logger.debug(
            f"Uploading file {file_path} to s3, pre-signed url {presigned_url}"
        )

        with open(file_path, "rb") as file:
            files = {"file": (file_path, file)}
            upload_response = requests.post(
                url=presigned_url, data=fields, files=files
            )
            logger.debug(f"Upload response: {upload_response}")
        if upload_response.status_code not in range(200, 299):
            raise ServerError(
                f"Failed to upload to s3, Upload response: {upload_response}"
            )

        return pre_signed_url_resp["file_id"]
