# provider.py

from cloud_providers import CloudProvider, GPU
from cloud_providers.gcp.models import GCPGPUSKU
import asyncio
from typing import List
from aiohttp import ClientSession
from cloud_providers.gcp.api import fetch_gpus_in_zone
from cloud_providers.gcp.zones import ZONES
from itertools import chain
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

class GoogleCloudProvider(CloudProvider):
    """Google Cloud Provider"""

    def __init__(self, project_id: str, service_account_file: str):
        self._project_id = project_id
        self._service_account_file = service_account_file
        self._token = self._get_oauth_token()

    def _get_oauth_token(self) -> str:
        credentials = Credentials.from_service_account_file(
                self._service_account_file,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
        credentials.refresh(Request())
        return credentials.token

    async def get_available_gpus(self) -> List[GPU]:
        async with ClientSession() as session:
            tasks = [
                asyncio.create_task(
                    fetch_gpus_in_zone(session, token=self._token, project_id=self._project_id, zone=zone)
                )
                for zone in ZONES
            ]
            results: list[list[GPU]] = await asyncio.gather(*tasks)
        
        return list(chain.from_iterable(results))


    async def get_gpu_skus(self) -> List[GCPGPUSKU]:
        """Get GPU SKUs"""
        pass