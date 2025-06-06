from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, validator
from typing import List

EFFICIENCY_MAP = {
    'NVIDIA TESLA P100':    "High",
    'NVIDIA V100':          "High",
    'NVIDIA A100 40GB':     "High",
    'NVIDIA A100 80GB':     "High",
    'NVIDIA H100 80GB':     "Medium",
    'NVIDIA H100 80GB MEGA':"Medium",
    'NVIDIA T4':           "Medium",
    'NVIDIA L4':           "Low",
    'NVIDIA TESLA P4':      "Medium",
    'NVIDIAH200 141GB':    "High",
}

class GPU(BaseModel):
    name: str
    zone: str
    efficiency: str = Field(default='unkown')

    @validator('efficiency', pre=True, always=True)
    def compute_efficiency(cls, v, values):
        return EFFICIENCY_MAP.get(values['name'].upper(), 'unkown')

class CloudProvider(ABC):
    @abstractmethod
    async def get_available_gpus(self) -> List[GPU]:
        pass