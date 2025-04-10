from cloud_providers import CloudProvider, GPU
from cloud_providers.gcp.models import GCPGPUSKU
from typing import List

class GoogleCloudProvider(CloudProvider):
    """Google Cloud Provider"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.gpus = []

    async def get_available_gpus(self) -> List[GPU]:
        """Get available GPUs in the project"""
        pass

    async def get_gpu_skus(self) -> List[GCPGPUSKU]:
        """Get GPU SKUs"""
        pass