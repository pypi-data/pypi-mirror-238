"""OctoAI Fine-tuning and Assets."""
from __future__ import (
    annotations,  # required to allow 3.7+ python use type | syntax introduced in 3.10
)

from abc import abstractmethod

from octoai.client import Client


class BaseModel(Client):
    """Base model."""

    # Future inclusions:
    # tune: LoraTuneModel
    # extract: LoraExtractionModel
    # checkpoint: CheckpointModel
    #
    # asset: AssetModel

    def __init__(
        self,
        api_endpoint: str,  # Used for dependency injection, otherwise child class
        token: str | None = None,
        *args,
        **kwargs,
    ):
        if api_endpoint[-1] != "/":
            api_endpoint += "/"
        self.api_endpoint = api_endpoint
        super(BaseModel, self).__init__(token)

    @abstractmethod
    def generate(self, *args, **kwargs):
        """Generate.  Only instantiated by child class."""
        pass
