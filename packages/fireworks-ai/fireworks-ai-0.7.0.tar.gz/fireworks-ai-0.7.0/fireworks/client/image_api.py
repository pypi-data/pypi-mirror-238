from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator


class Error(BaseModel):
    object: str = "error"
    type: str = "invalid_request_error"
    message: str


class ErrorResponse(BaseModel):
    error: Error = Field(default_factory=Error)


class TextPrompt(BaseModel):
    text: str
    weight: int


class TextToImageRequestBody(BaseModel):
    model: str = "stable-diffusion-xl-1024-v1-0"
    cfg_scale: int = 7
    clip_guidance_preset: str = "NONE"
    height: int = 1024
    width: int = 1024
    sampler: Optional[str] = None
    samples: int = 1
    steps: int = 50
    seed: int = 0
    style_preset: Optional[str] = None
    text_prompts: List[TextPrompt]

    safety_check: bool = False

    # LoRA parameters
    lora_adapter_name: Optional[str] = None
    lora_weight_filename: Optional[str] = None


class ImageToImageRequestBody(BaseModel):
    model: str = "stable-diffusion-xl-1024-v1-0"
    cfg_scale: int = Field(default=7)
    clip_guidance_preset: str = "NONE"
    sampler: Optional[str]
    samples: int = 1
    steps: int = 50
    seed: int = 0
    style_preset: Optional[str]

    init_image_mode: str = "IMAGE_STRENGTH"
    image_strength: Optional[float]
    step_schedule_start: Optional[float] = 0.65
    step_schedule_end: Optional[float]

    safety_check: bool = False

    prompt: str = Field(default="")
    negative_prompt: Optional[str] = None

    # LoRA parameters
    lora_adapter_name: Optional[str] = None
    lora_weight_filename: Optional[str] = None

    @validator("image_strength", pre=True, always=True)
    def validate_image_strength(cls, v, values):
        if values["init_image_mode"] == "IMAGE_STRENGTH" and v is None:
            raise ValueError(
                "image_strength is required when init_image_mode is IMAGE_STRENGTH"
            )
        return v

    @validator("step_schedule_start", "step_schedule_end", pre=True, always=True)
    def validate_step_schedule(cls, v, values):
        if values["init_image_mode"] == "STEP_SCHEDULE" and v is None:
            raise ValueError(
                "Both step_schedule_start and step_schedule_end are required when init_image_mode is STEP_SCHEDULE"
            )
        return v


class ControlNetRequestBody(BaseModel):
    model: str = "stable-diffusion-xl-1024-v1-0"
    cfg_scale: int = Field(default=7)
    clip_guidance_preset: str = "NONE"
    sampler: Optional[str]
    samples: int = 1
    steps: int = 50
    seed: int = 0
    style_preset: Optional[str]

    control_net_name: str
    conditioning_scale: float = 0.5

    step_schedule_start: Optional[float] = 0.0
    step_schedule_end: Optional[float] = 1.0

    safety_check: bool = False

    prompt: str = Field(default="")
    negative_prompt: Optional[str] = None

    # LoRA parameters
    lora_adapter_name: Optional[str] = None
    lora_weight_filename: Optional[str] = None
