# api.py

from aiohttp import ClientSession
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from cloud_providers.gcp.models import GCPZone, GCPAcceleratorTypeList
from cloud_providers import GPU
from cloud_providers.gcp.zones import ZONES
import asyncio

async def fetch_gpus_in_zone(session: ClientSession, token: str, project_id: str, zone: GCPZone) -> list[GPU]:
    """Fetches all the GPUs in a given zone."""

    url = f"https://compute.googleapis.com/compute/v1/projects/{project_id}/zones/{zone.name.value}/acceleratorTypes"
    headers = {"Authorization": f"Bearer {token}"}
    async with session.get(url, headers=headers) as response:
        response_json = await response.json()

    accelerator_list = GCPAcceleratorTypeList.model_validate(response_json)

    gpus: list[GPU] = []
    for item in accelerator_list.items:
        if (
            "NVIDIA" not in item.description
            or "Workstation" in item.description
        ):
            continue

        zone = item.zone.split("/")[-1]
        description = item.description.upper()

        gpus.append(
            GPU(
                name=description,
                zone=zone,
                maximumCardsPerInstance=item.maximumCardsPerInstance,
            )
        )

    return gpus