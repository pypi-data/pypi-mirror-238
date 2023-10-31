from dataclasses import dataclass
import enum
import json

MAX_MEMORY = 256
MAX_GPU_COUNT = 8
MAX_CPU = 48

MIN_CPU = 1
MIN_MEMORY = 2

DEFAULT_COOLDOWN = 60
DEFAULT_CPU = 2
DEFAULT_MEMORY = 8
DEFAULT_MIN_REPLICAS = 0
DEFAULT_HARDWARE_SELECTION = "AMPERE_A6000"
DEFAULT_PYTHON_VERSION = "3.10"


class PythonVersion(enum.Enum):
    PYTHON_3_8 = "3.8"
    PYTHON_3_9 = "3.9"
    PYTHON_3_10 = "3.10"
    PYTHON_3_11 = "3.11"


@dataclass
class HardwareOption:
    def __init__(
        self,
        name: str,
        VRAM: int,
        gpu_model: str,
        max_memory: float = 128.0,
        max_cpu: int = 36,
        max_gpu_count: int = MAX_GPU_COUNT,
        has_nvlink: bool = False,
    ):
        self.name = name
        self.gpu_model = gpu_model
        self.max_memory = max_memory
        self.max_cpu = max_cpu
        self.max_gpu_count = max_gpu_count
        self.VRAM = VRAM
        self.has_nvlink = has_nvlink

    def validate(self, cpu: int, memory: float, gpu_count: int) -> str:
        message = ""
        if cpu > self.max_cpu:
            message += f"CPU must be at most {self.max_cpu} for {self.name}.\n"
        if cpu < MIN_CPU:
            message += f"CPU must be at least {MIN_CPU} for {self.name}.\n"
        if memory > self.max_memory:
            message += f"Memory must be at most {self.max_memory} GB"
            "for {self.name}.\n"
        if memory < MIN_MEMORY:
            message += f"Memory must be at least {MIN_MEMORY} GB"
            " for {self.name}.\n"
        if gpu_count > self.max_gpu_count:
            message += f"Number of GPUs must be at most {self.max_gpu_count}"
            " for {self.name}.\n"
        if gpu_count < 1:
            message += f"Number of GPUs must be at least 1 for {self.name}.\n"

        return message

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=False)


class Hardware:
    GPU: HardwareOption = HardwareOption(
        name="TURING_4000", VRAM=8, gpu_model="Quadro RTX 4000"
    )
    TURING_4000: HardwareOption = HardwareOption(
        name="TURING_4000", VRAM=8, gpu_model="Quadro RTX 4000"
    )
    TURING_5000: HardwareOption = HardwareOption(
        name="TURING_5000", VRAM=8, gpu_model="RTX 5000"
    )
    AMPERE_A4000: HardwareOption = HardwareOption(
        name="AMPERE_A4000", VRAM=16, gpu_model="RTX A4000"
    )
    AMPERE_A5000: HardwareOption = HardwareOption(
        name="AMPERE_A5000", VRAM=24, gpu_model="RTX A5000"
    )
    AMPERE_A6000: HardwareOption = HardwareOption(
        name="AMPERE_A6000",
        max_memory=256.0,
        max_cpu=48,
        VRAM=48,
        gpu_model="RTX A6000",
    )
    AMPERE_A100: HardwareOption = HardwareOption(
        name="AMPERE_A100",
        max_memory=256.0,
        max_cpu=48,
        VRAM=80,
        has_nvlink=True,
        gpu_model="A100",
    )
    AMPERE_A100_40GB: HardwareOption = HardwareOption(
        name="AMPERE_A100_40GB",
        max_memory=256.0,
        max_cpu=48,
        VRAM=40,
        has_nvlink=True,
        gpu_model="A100 40GB",
    )

    @classmethod
    def available_hardware(cls):
        return list(cls.__annotations__.keys())
