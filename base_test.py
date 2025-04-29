from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, validator
from typing import List

"""
EFFICIENCY_MAP = {
    'NVIDIA TESLA P100':    15.7,
    'NVIDIA V100':          26.0,
    'NVIDIA A100 40GB':     38.8,
    'NVIDIA A100 80GB':     48.8,
    'NVIDIA H100 80GB':     85.7,
    'NVIDIA H100 80GB MEGA':85.7,
    'NVIDIA T4':           116.0,
    'NVIDIA L4':           210.0,
    'NVIDIA TESLA P4':      73.3,
    'NVIDIAH200 141GB':    48.57,
}

0 - 60: High
60 - 120: Medium
> 120: Low
"""

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
    efficiency: str

    @validator('efficiency', pre=True, always=True)
    def compute_efficiency(cls, v, values):
        return EFFICIENCY_MAP.get(values['name'].upper(), 'unknown')