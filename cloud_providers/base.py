from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class GPU(BaseModel):
    name: str
    zone: str
    maximumCardsPerInstance: int

class CloudProvider(ABC):
    @abstractmethod
    async def get_available_gpus(self) -> List[GPU]:
        pass