"""
 Copyright (C) 2023, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""


from enum import Enum


class DatastoreType(Enum):
    """Supported datastore types"""

    LOCAL = 0
    S3 = 1
    AZURE = 2
    GCS = 3


class DataType(Enum):
    """Supported Data types"""

    IMAGE = "image/*"
    VIDEO = "video/*"


class JobType(Enum):
    """Supported Job types"""

    EXPLORE = "EXPLORE"
    ANALYZE = "ANALYZE"


class FeaturizerType(Enum):
    """Type of featurizer to be used for ingestion
    FULL_IMAGE: Features generated on the full image
    PATCH: Features generated on a grid of cells over image. Supports patch
    search
    EXTERNAL: Features are generated externally and registered against dataset
    """

    FULL_IMAGE = 0
    PATCH = 1
    EXTERNAL = 2


class ClusterAlgoType(Enum):
    """Cluster algorithms supported by DataExplorer"""

    HDBSCAN = "hdbscan"
    KMEANS = "kmeans"
    GMM = "gmm"


class EmbedAlgoType(Enum):
    """Embedding algorithms supported by DataExplorer"""

    UMAP = "umap"
    PCA = "pca"
    LLE = "lle"


class JobContext(Enum):
    """Specifies the context that samples are requested under"""

    CONFUSION_MATRIX_CELL = 0
    SIMILARITY_SEARCH = 1
    CLUSTER_RETRIEVAL = 2
    CORESET_SAMPLING = 3


class JobStatisticsContext(Enum):
    """Specifies the type of statistics to be retrieved"""

    CONFUSION_MATRIX = 0
    PRECISION_RECALL_CURVE = 1
    CONFIDENCE_HISTOGRAM = 2


class BackgroundTaskType(Enum):
    """Specifies the type of background task"""

    DATASET_INGESTION = "dataset_ingestion"
