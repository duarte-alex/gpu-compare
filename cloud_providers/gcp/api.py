from aiohttp import ClientSession
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from .models import GCPZone, GPU
from .zones import ZONES
import asyncio

async def fetch_gpus_in_zone(session: ClientSession, token: str, project_id: str, zone: GCPZone) -> list[GPU]:
    pass