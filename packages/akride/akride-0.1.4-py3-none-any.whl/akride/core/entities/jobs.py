"""
 Copyright (C) 2023, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""
from typing import Dict

import akridata_dsp as dsp

from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity

from akride.core.enums import (  # isort:skip
    ClusterAlgoType,
    EmbedAlgoType,
    JobType,
)


class JobSpec(Dict):
    """
    Class representing a job specification.
    TODO: separate specs for different job types
    """

    def __init__(self, dataset: Dataset, **kwargs):
        """
        Constructor for the JobSpec class.

        Parameters:
        -----------
        dataset: Dataset
            The dataset to explore.
        job_type : str
            The job type - 'EXPLORE', 'ANALYZE' etc.
        job_name : str, optional
            The name of the job to create. A unique name will be generated if
            this is not given.
        predictions_file: str, optional
            The path to the catalog file containing predictions and ground
            truth.
            This file must be formatted according to the specification at:
            https://docs.akridata.ai/docs/analyze-job-creation-and-visualization
        cluster_algo : ClusterAlgoType, optional
            The clustering algorithm to use.
        embed_algo : EmbedAlgoType, optional
            The embedding algorithm to use.
        num_clusters : int, optional
            The number of clusters to create.
        max_images : int, optional
            The maximum number of images to use.
        catalog_name : str, optional
            The catalog to be used for creating this explore job. This defaults
            to the internal primary catalog that is created automatically when
            a dataset is created.
        filters : List[Condition], optional
            The filters to be used to select a subset of examples for this job.
            These filters are applied to the catalog specified by catalog_name.
        """
        defaults = {
            "dataset": dataset,
            "job_type": JobType.EXPLORE,
            "predictions_file": "",
            "job_name": "",
            "cluster_algo": ClusterAlgoType.HDBSCAN,
            "embed_algo": EmbedAlgoType.UMAP,
            "num_clusters": None,
            "max_images": 1000,
            "catalog_name": "primary",
            "filters": None,
        }

        super().__init__()
        self.update(defaults)
        self.update(kwargs)
        if not self["job_name"]:
            # TODO: generate a unique name
            self["job_name"] = "DEFAULT-JOB-NAME"


class Job(Entity):
    """
    Class representing a job entity.
    """

    def __init__(self, info: dsp.CreateJobRequestResponse):
        """
        Constructor for the Job class.

        Parameters
        ----------
        info : dsp.models.dataset_job_request.DatasetJobRequest
            The job request object.
        """
        super().__init__("", "")
        self.info = info

    def delete(self) -> None:
        """
        Deletes an entity.

        Parameters
        ----------

        Returns
        -------
        None
        """
        return None

    @property
    def dataset_id(self):
        return self.info.dataset_id  # type: ignore

    @property
    def pipeline_id(self):
        return self.info.pipeline_id  # type: ignore
