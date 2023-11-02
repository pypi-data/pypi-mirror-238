"""OctoAI Text Generation."""
from .base_model import BaseModel


class TextGenerationModel(BaseModel):
    """Text generation model."""

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    def generate(self):
        """Generate text based on request."""
        pass
