from cloud_providers.gcp.models import GCPGPUNames, GCPGPU

GPUS: list[GCPGPU] = [
    GCPGPU(name=GCPGPUNames.NVIDIA_TESLA_P100, efficiency=15.7),
    GCPGPU(name=GCPGPUNames.NVIDIA_V100, efficiency=26.0),
    GCPGPU(name=GCPGPUNames.NVIDIA_A100_40GB, efficiency=38.8),
    GCPGPU(name=GCPGPUNames.NVIDIA_A100_80GB, efficiency=48.8),
    GCPGPU(name=GCPGPUNames.NVIDIA_H100_80GB, efficiency=85.7),
    GCPGPU(name=GCPGPUNames.NVIDIA_H100_80GB_MEGA, efficiency=85.7),
    GCPGPU(name=GCPGPUNames.NVIDIA_T4, efficiency=116.0),
    GCPGPU(name=GCPGPUNames.NVIDIA_L4, efficiency=210.0),
    GCPGPU(name=GCPGPUNames.NVIDIA_TESLA_P4, efficiency=73.3),
    GCPGPU(name=GCPGPUNames.NVIDIA_H200_141GB, efficiency=48.57),]

GPUS_BY_NAME: dict[GCPGPUNames, GCPGPU] = {gpu.name: gpu for gpu in GPUS}
