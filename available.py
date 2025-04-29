# run to get a .json file with the available GPUs

import asyncio
import os
from cloud_providers.gcp import GoogleCloudProvider
from dotenv import load_dotenv
import json
from typing import List
from cloud_providers import GPU

def save_to_json(path: str, data: List[GPU]):
    serializable = [
        {
            "name": gpu.name,
            "zone": gpu.zone,
            "efficiency": gpu.efficiency,
        }
        for gpu in data
    ]
    with open(path, "w") as json_file:
        json.dump(serializable, json_file, indent=4)

async def main():

    load_dotenv()
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_SERVICE_ACCOUNT_FILE = os.getenv("GCP_SERVICE_ACCOUNT_FILE")
    GCP = GoogleCloudProvider(GCP_PROJECT_ID, GCP_SERVICE_ACCOUNT_FILE)
    available_gpus = await GCP.get_available_gpus()
    save_to_json("available_gpus.json", available_gpus)

if __name__ == "__main__":
    asyncio.run(main())