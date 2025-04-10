from cloud_providers import CloudProvider, GPU
from cloud_providers.gcp.models import GCPGPUSKU
import asyncio
from typing import List
from aiohttp import ClientSession
from cloud_providers.gcp.api import fetch_gpus_in_zone
from cloud_providers.gcp.zones import ZONES

class GoogleCloudProvider(CloudProvider):
    """Google Cloud Provider"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.gpus = []

    async def get_available_gpus(self) -> List[GPU]:
        """Get available GPUs"""
        tasks: list[asyncio.Task[list[GPU]]] = []
        async with ClientSession() as session:
            for zone in ZONES:
                tasks.append(asyncio.create_task(fetch_gpus_in_zone(session, zone)))

            results: list[list[GPU]] = await asyncio.gather(*tasks)

        all_available_gpus: list[GPU] = []
        for result in results:
            all_available_gpus.extend(result)

        return all_available_gpus

    async def get_gpu_skus(self) -> List[GCPGPUSKU]:
        """Get GPU SKUs"""
        pass