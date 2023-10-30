"""
 Copyright (C) 2023, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import akridata_dsp as dsp

from akride.core.entities.entity import Entity


class Resultset(Entity):
    """
    Class representing a result set entity.
    """

    def __init__(self, info: dsp.ResultsetListResponseItem):
        """
        Constructor for the Resultset class.

        Parameters
        ----------
        info : dsp.ResultsetListResponseItem
            The resultset response.
        """
        super().__init__(info.id, info.name)
        self.info = info

    @property
    def job_id(self):
        return self.info.request_id

    @property
    def version(self):
        return self.info.version

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
