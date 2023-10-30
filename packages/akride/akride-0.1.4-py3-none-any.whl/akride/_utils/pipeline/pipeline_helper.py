from akride._utils.pipeline.constants import Constants
from akride.core.enums import DataType, FeaturizerType


class PipelineHelper:
    FEATURIZER_TYPE_AND_PIPELINE_MAPPING = {
        DataType.IMAGE: {
            FeaturizerType.FULL_IMAGE: (
                Constants.FULL_IMAGE_PIPELINE_INTERNAL_ID
            ),
            FeaturizerType.PATCH: Constants.PATCH_IMAGE_PIPELINE_INTERNAL_ID,
        }
    }

    @classmethod
    def get_pipeline_internal_id(
        cls,
        featurizer_type: FeaturizerType,
        data_type: DataType = DataType.IMAGE,
    ) -> int:
        featurizer_map_by_datatype = (
            cls.FEATURIZER_TYPE_AND_PIPELINE_MAPPING.get(data_type)
        )
        if not featurizer_map_by_datatype:
            raise ValueError(f"Data type {data_type} is not yet supported!")

        pipeline_internal_id = featurizer_map_by_datatype.get(featurizer_type)

        if not pipeline_internal_id:
            raise ValueError(
                f"Featurizer {featurizer_type} is not yet supported"
            )
        return pipeline_internal_id
