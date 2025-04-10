import asyncio
import os
import psycopg2
from cloud_providers.gcp.provider import GoogleCloudProvider
from cloud_providers.gcp.models import GPU, GCPGPUSKU, GCPGPUNames
from cloud_providers.gcp.models import GCPGPU, GPUS_BY_NAME
from connect import store_gpus
from dotenv import load_dotenv

async def main():

    load_dotenv()
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_SERVICE_ACCOUNT_FILE = os.getenv("GCP_SERVICE_ACCOUNT_FILE")
    GCP = GoogleCloudProvider(GCP_PROJECT_ID, GCP_SERVICE_ACCOUNT_FILE)

    # Fetch the list of available GPUs: returns List[GPU]
    available_gpus = await GCP.get_available_gpus()
    # Fetch the list of GPU SKUs (pricing information): returns List[GCPGPUSKU]
    gpu_skus = await GCP.get_gpu_skus()

    # Build a lookup for pricing: (gpu_name, zone) -> price.
    sku_map = {}
    for sku in gpu_skus:
        key = (sku.name, sku.zone)
        sku_map[key] = sku.price

    # Prepare a list to hold GPU data for database insertion.
    gpu_data_for_db = []

    # 5. Merge availability, pricing, and efficiency data.
    for g in available_gpus:
        # Convert enum values to strings.
        name_str = g.name.value
        zone_str = g.zone.value

        # Look up price; if not found, default to 0.0.
        price = sku_map.get((name_str, g.zone), 0.0)
        # Get efficiency from the GPUS_BY_NAME lookup.
        efficiency = GPUS_BY_NAME[g.name].efficiency if g.name in GPUS_BY_NAME else 0.0

        # Print one row of data.
        print(f"{name_str:<25} {zone_str:<15} {price:<10} {efficiency:<10}")

        # Prepare a description combining price and efficiency.
        description = f"Price: {price}, Efficiency: {efficiency}"

        # Append the record matching the DB table structure.
        gpu_data_for_db.append({
            "Zone": zone_str,
            "GPU_Name": name_str,
            "Description": description,
        })

    # Store the GPU records in the Postgres table.
    store_gpus(gpu_data_for_db)

if __name__ == "__main__":
    asyncio.run(main())
