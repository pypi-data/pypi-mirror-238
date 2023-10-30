from abc import ABC, abstractmethod

import akridata_akrimanager_v2 as am


class PartitionerFilter(ABC):
    def __init__(self, dataset_id: str, ccs_api: am.CcsApi):
        self.dataset_id = dataset_id
        self.ccs_api = ccs_api

    @abstractmethod
    def run(self):
        pass
