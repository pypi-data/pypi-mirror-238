from pydantic import BaseModel, Field, validator
from typing import Optional, Literal, List
import uuid



class LLMServingParams(BaseModel):
    basemodel_path: str = Field(..., description="Path to the base model can be a huggingface model or a custom model link", examples=["meta-llama/Llama-2-7b-hf"])
    loramodel_path: Optional[str] = Field(None, description="Path to the LoRA model can be a huggingface model or a custom model link", examples=["qblocks/OpenPlatypus_LLAMA2_7b"])
    prompt_template: str = Field(..., description="Template for the prompt",examples = ["{prompt}{completion}"])
    per_gpu_vram: Literal[8, 16, 24, 48, 80] = Field(..., description="GPU VRAM to be used", examples = [24])
    gpu_count: Literal[1, 2, 4, 8] = Field(..., description="Number of GPUs to be used", examples = [1])
    api_auth_token: Optional[str] = Field(str(uuid.uuid4()), description="API authentication token, auto-generated")

DEPLOY_SERVICES = ["llm", "custom_image"]

class InstanceParams(BaseModel):
    harddisk: str = Field("100", description="Hard disk size in GB. Provide value considering your model size.")
    blockName: str = Field("qb24-v2-n1", description="Name of the block to be used for the instance. Use pypi client for automation.")

class DockerImgParams(BaseModel):
    registryName: str = Field("hello-world", description="Name of the docker registry or docker image url", examples=[ "qblocks/dummy-imagepath:latest"])
    username: str = Field("", description="Username for the docker hub registry", examples=["qblocks"])
    password: str = Field("", description="Password for the docker hub registry", examples=["qblocksdummy password"])

class CustomImageParams(BaseModel):
    instance_params: InstanceParams = Field(..., description="Instance parameters for the deployment")
    image_registry: DockerImgParams = Field(..., description="Docker image parameters for the deployment")
    env_params: dict = Field(..., description="Environment variables for the deployment")
    port_numbers: List[int] = Field(..., description="Port numbers for the deployment")