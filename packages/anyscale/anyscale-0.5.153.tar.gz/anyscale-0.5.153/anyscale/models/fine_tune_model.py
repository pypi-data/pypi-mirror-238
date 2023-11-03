from typing import Optional

from pydantic import BaseModel


class FineTuneConfig(BaseModel):
    base_model: str
    train_file: str
    valid_file: Optional[str]
    cloud_id: str
    suffix: Optional[str]
