from typing import List, Optional, Union
from .image_api import (
    ImageToImageRequestBody,
    TextToImageRequestBody,
    ControlNetRequestBody,
    TextPrompt,
)
from .api_client import FireworksClient

from PIL import Image
import httpx
import io
import os
from dataclasses import dataclass
import base64


@dataclass
class Answer:
    image: Optional[Image.Image]
    finish_reason: str


class ImageInference(FireworksClient):
    """
    Main client class for the Fireworks Image Generation API. Currently supports Stable Diffusion
    XL 1.0 (see https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0). This client
    supports both text-to-image and image-to-image generation.
    """

    def __init__(
        self,
        account: str = "fireworks",
        model: str = "stable-diffusion-xl-1024-v1-0",
        request_timeout=600,
        **kwargs,
    ) -> None:
        super().__init__(request_timeout, **kwargs)
        self.account = account
        self.model = model

    def _img_to_bytes(
        self, image: Union[Image.Image, str, os.PathLike, bytes]
    ) -> bytes:
        # Normalize all forms of `image` into a `bytes` object
        # to send over the wire
        if isinstance(image, Image.Image):
            img_bio = io.BytesIO()
            image.save(img_bio, format="PNG")
            image = img_bio.getvalue()
        elif isinstance(image, (str, os.PathLike)):
            with open(image, "rb") as f:
                image = f.read()

        return image

    def text_to_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        cfg_scale: int = 7,
        clip_guidance_preset: str = "NONE",
        height: int = 1024,
        width: int = 1024,
        sampler: Optional[str] = None,
        samples: int = 1,
        steps: int = 50,
        seed: int = 0,
        style_preset: Optional[str] = None,
        safety_check: bool = False,
        lora_adapter_name: Optional[str] = None,
        lora_weight_filename: Optional[str] = None,
        hf_access_key: Optional[str] = None,
        output_image_format: str = "PNG",
    ) -> Union[Image.Image, List[Image.Image]]:
        """
        Generate an image or images based on the given text prompt and optional negative prompt.
        See the OpenAPI spec (https://readme.fireworks.ai/reference/post_image-generation-stable-diffusion)
        for the most up-to-date description of the supported parameters

        Parameters:
        - prompt (str): The main text prompt based on which the image will be generated.
        - negative_prompt (str, optional): A secondary text prompt which can be used to guide the image generation in a negative way.
        - cfg_scale (int, optional): Configuration scale for the image generation. Defaults to 7.
        - clip_guidance_preset (str, optional): CLIP guidance preset. Defaults to "NONE".
        - height (int, optional): Desired height of the generated image. Defaults to 1024.
        - width (int, optional): Desired width of the generated image. Defaults to 1024.
        - sampler (str, optional): Sampler type. Optional.
        - samples (int, optional): Number of images to be generated. Defaults to 1.
        - steps (int, optional): Number of steps for the generation process. Defaults to 50.
        - seed (int, optional): Seed for random number generation. Defaults to 0.
        - style_preset (str, optional): Style preset for the generated image. Optional.
        - lora_adapter_name (str, optional): LoRA adapter name. This can refer to a fully-qualified HuggingFace repo name, e.g. 'foo/bar'. Optional
        - lora_weight_filename (str, optional): The filename within the LoRA repo to load LoRA weights from. Should be a single filename like 'pytorch_lora_weights.safetensors'. Optional. Must be specified if lora_adapter_name is specified.
        - hf_access_key (str, optional): The access key to access HuggingFace to download a LoRA adapter. Specify if your adapter is in a private repo that requires permissions. Optional.
        - output_image_format (str): The format of the generated image. Defaults to "PNG". Options are "PNG" and "JPG". Use PNG for best quality and JPG for best speed. JPG currently only supported for samples=1.

        Returns:
        Image.Image or List[Image.Image]: Generated image or a list of generated images.

        Raises:
        RuntimeError: If there is an error in the image generation process.
        """
        text_prompts = [
            TextPrompt(text=prompt, weight=1.0),
        ]
        if negative_prompt:
            text_prompts.append(TextPrompt(text=negative_prompt, weight=-1.0))
        request_body = TextToImageRequestBody(
            cfg_scale=cfg_scale,
            clip_guidance_preset=clip_guidance_preset,
            height=height,
            width=width,
            sampler=sampler,
            samples=samples,
            steps=steps,
            seed=seed,
            style_preset=style_preset,
            text_prompts=text_prompts,
            safety_check=safety_check,
            lora_adapter_name=lora_adapter_name,
            lora_weight_filename=lora_weight_filename,
        )
        payload_dict = request_body.dict()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if samples == 1:
            if output_image_format in {"JPG", "JPEG"}:
                headers["Accept"] = "image/jpeg"
            elif output_image_format == "PNG":
                headers["Accept"] = "image/png"
            else:
                raise ValueError(
                    f"Unsupported output_image_format: {output_image_format}"
                )
        else:
            if output_image_format == "PNG":
                headers["Accept"] = "application/json"
            else:
                raise ValueError(
                    f"Only PNG output image format is supported when samples != 1"
                )

        if hf_access_key is not None:
            headers["Huggingface-Access-Key"] = hf_access_key

        with httpx.Client(
            headers=headers,
            timeout=self.request_timeout,
            **self.client_kwargs,
        ) as client:
            endpoint_base_uri = f"{self.base_url}/image_generation/accounts/{self.account}/models/{self.model}"
            response = client.post(endpoint_base_uri, json=payload_dict)
            self._error_handling(response)
        if samples == 1:
            finish_reason = response.headers.get("finish-reason", "SUCCESS")
            return Answer(
                image=Image.open(io.BytesIO(response.content)),
                finish_reason=finish_reason,
            )
        else:
            return [
                Answer(
                    Image.open(io.BytesIO(base64.b64decode(artifact["base64"]))),
                    finish_reason=artifact["finishReason"],
                )
                for artifact in response.json()
            ]

    def image_to_image(
        self,
        init_image: Union[Image.Image, str, os.PathLike, bytes],
        prompt: str,
        negative_prompt: Optional[str] = None,
        cfg_scale: int = 7,
        clip_guidance_preset: str = "NONE",
        sampler: Optional[str] = None,
        samples: int = 1,
        steps: int = 50,
        seed: int = 0,
        style_preset: Optional[str] = None,
        init_image_mode: str = "IMAGE_STRENGTH",
        image_strength: Optional[float] = None,
        step_schedule_start: Optional[float] = 0.65,
        step_schedule_end: Optional[float] = None,
        safety_check: bool = False,
        client_account_id_header: Optional[str] = None,
        lora_adapter_name: Optional[str] = None,
        lora_weight_filename: Optional[str] = None,
        hf_access_key: Optional[str] = None,
        output_image_format: str = "PNG",
    ) -> Union[Image.Image, List[Image.Image]]:
        """
        Modify an existing image based on a given text prompt and optional negative prompt.
        See the OpenAPI spec (https://readme.fireworks.ai/reference/post_image-generation-stable-diffusion)
        for the most up-to-date description of the supported parameters

        Parameters:
        - init_image (Union[Image.Image, str, os.PathLike, bytes]): Initial image to be modified. It can be provided as a PIL Image object, path to an image, or raw bytes.
        - prompt (str): The main text prompt based on which the image will be modified.
        - negative_prompt (str, optional): A secondary text prompt which can be used to guide the image modification in a negative way.
        - cfg_scale (int, optional): Configuration scale for the image modification. Defaults to 7.
        - clip_guidance_preset (str, optional): CLIP guidance preset. Defaults to "NONE".
        - sampler (str, optional): Sampler type. Optional.
        - samples (int, optional): Number of images to be generated. Defaults to 1.
        - steps (int, optional): Number of steps for the modification process. Defaults to 50.
        - seed (int, optional): Seed for random number generation. Defaults to 0.
        - style_preset (str, optional): Style preset for the modified image. Optional.
        - init_image_mode (str, optional): Initialization mode for the image modification. Defaults to "IMAGE_STRENGTH".
        - image_strength (float, optional): Strength of the initial image. Required when init_image_mode is "IMAGE_STRENGTH".
        - step_schedule_start (float, optional): Start of the step schedule. Required when init_image_mode is "STEP_SCHEDULE". Defaults to 0.65.
        - step_schedule_end (float, optional): End of the step schedule. Required when init_image_mode is "STEP_SCHEDULE".
        - model (str, optional): which model to use. Defaults to "accounts/fireworks/models/stable-diffusion-xl-1024-v1-0".
        - client_account_id_header (str, optional): Client account ID header. Used for private deployments. Optional.
        - lora_adapter_name (str, optional): LoRA adapter name. This can refer to a fully-qualified HuggingFace repo name, e.g. 'foo/bar'. Optional
        - lora_weight_filename (str, optional): The filename within the LoRA repo to load LoRA weights from. Should be a single filename like 'pytorch_lora_weights.safetensors'. Optional. Must be specified if lora_adapter_name is specified.
        - hf_access_key (str, optional): The access key to access HuggingFace to download a LoRA adapter. Specify if your adapter is in a private repo that requires permissions. Optional.
        - output_image_format (str): The format of the generated image. Defaults to "PNG". Options are "PNG" and "JPG". Use PNG for best quality and JPG for best speed. JPG currently only supported for samples=1.

        Returns:
        Image.Image or List[Image.Image]: Modified image or a list of modified images.

        Raises:
        ValueError: If required parameters are missing based on the given init_image_mode.
        RuntimeError: If there is an error in the image modification process.
        """
        # Argument Validation
        if init_image_mode == "IMAGE_STRENGTH" and image_strength is None:
            raise ValueError(
                "image_strength is required when init_image_mode is IMAGE_STRENGTH"
            )
        if init_image_mode == "STEP_SCHEDULE" and (
            step_schedule_start is None or step_schedule_end is None
        ):
            raise ValueError(
                "Both step_schedule_start and step_schedule_end are required when init_image_mode is STEP_SCHEDULE"
            )

        # Construct and validate request fields.
        # NB: prompt and init_image are not used here. Instead, we construct
        # them specially to be sent as multipart/form-data
        request_body = ImageToImageRequestBody(
            prompt=prompt,
            negative_prompt=negative_prompt,
            cfg_scale=cfg_scale,
            clip_guidance_preset=clip_guidance_preset,
            sampler=sampler,
            samples=samples,
            steps=steps,
            seed=seed,
            style_preset=style_preset,
            init_image_mode=init_image_mode,
            image_strength=image_strength,
            step_schedule_start=step_schedule_start,
            step_schedule_end=step_schedule_end,
            safety_check=safety_check,
            lora_adapter_name=lora_adapter_name,
            lora_weight_filename=lora_weight_filename,
        )
        payload_dict = request_body.dict()

        headers = {"Authorization": f"Bearer {self.api_key}"}
        if samples == 1:
            if output_image_format in {"JPG", "JPEG"}:
                headers["Accept"] = "image/jpeg"
            elif output_image_format == "PNG":
                headers["Accept"] = "image/png"
            else:
                raise ValueError(
                    f"Unsupported output_image_format: {output_image_format}"
                )
        else:
            if output_image_format == "PNG":
                headers["Accept"] = "application/json"
            else:
                raise ValueError(
                    f"Only PNG output image format is supported when samples != 1"
                )

        if client_account_id_header:
            headers["X-Fireworks-Routing-Account-ID"] = client_account_id_header

        if hf_access_key is not None:
            headers["Huggingface-Access-Key"] = hf_access_key

        init_image: bytes = self._img_to_bytes(init_image)

        files = {
            "init_image": init_image,
        }
        with httpx.Client(
            headers=headers,
            timeout=self.request_timeout,
            **self.client_kwargs,
        ) as client:
            endpoint_base_uri = f"{self.base_url}/image_generation/accounts/{self.account}/models/{self.model}"
            response = client.post(
                f"{endpoint_base_uri}/image_to_image",
                data=payload_dict,
                files=files,
            )
            self._error_handling(response)
        if samples == 1:
            finish_reason = response.headers.get("finish-reason", "SUCCESS")
            return Answer(
                image=Image.open(io.BytesIO(response.content)),
                finish_reason=finish_reason,
            )
        else:
            return [
                Answer(
                    Image.open(io.BytesIO(base64.b64decode(artifact["base64"]))),
                    finish_reason=artifact["finishReason"],
                )
                for artifact in response.json()
            ]

    def control_net(
        self,
        control_image: Union[Image.Image, str, os.PathLike, bytes],
        control_net_name: str,
        prompt: str,
        negative_prompt: Optional[str] = None,
        cfg_scale: int = 7,
        clip_guidance_preset: str = "NONE",
        sampler: Optional[str] = None,
        samples: int = 1,
        steps: int = 50,
        seed: int = 0,
        style_preset: Optional[str] = None,
        step_schedule_start: Optional[float] = 0.0,
        step_schedule_end: Optional[float] = 1.0,
        conditioning_scale: Optional[float] = 0.5,
        safety_check: bool = False,
        client_account_id_header: Optional[str] = None,
        lora_adapter_name: Optional[str] = None,
        lora_weight_filename: Optional[str] = None,
        hf_access_key: Optional[str] = None,
        output_image_format: str = "PNG",
    ) -> Union[Image.Image, List[Image.Image]]:
        """
        Modify an existing image based on a given text prompt and optional negative prompt.
        See the OpenAPI spec (https://readme.fireworks.ai/reference/post_image-generation-stable-diffusion)
        for the most up-to-date description of the supported parameters

        Parameters:
        - control_image (Union[Image.Image, str, os.PathLike, bytes]): Initial image to be modified. It can be provided as a PIL Image object, path to an image, or raw bytes.
        - control_net_name (str): Name of HuggingFace repository with control net name or a simple reference like "canny".
        - prompt (str): The main text prompt based on which the image will be modified.
        - negative_prompt (str, optional): A secondary text prompt which can be used to guide the image modification in a negative way.
        - cfg_scale (int, optional): Configuration scale for the image modification. Defaults to 7.
        - clip_guidance_preset (str, optional): CLIP guidance preset. Defaults to "NONE".
        - sampler (str, optional): Sampler type. Optional.
        - samples (int, optional): Number of images to be generated. Defaults to 1.
        - steps (int, optional): Number of steps for the modification process. Defaults to 50.
        - seed (int, optional): Seed for random number generation. Defaults to 0.
        - style_preset (str, optional): Style preset for the modified image. Optional.
        - step_schedule_start (float, optional): The percentage of total steps at which the ControlNet starts applying.
        - step_schedule_end (float, optional): The percentage of total steps at which the ControlNet stops applying.
        - conditioning_scale (float, optional, defaults to 0.5): The outputs of the ControlNet are multiplied by this value before they are added to the residual.
        - model (str, optional): which model to use. Defaults to "accounts/fireworks/models/stable-diffusion-xl-1024-v1-0".
        - client_account_id_header (str, optional): Client account ID header. Used for private deployments. Optional.
        - lora_adapter_name (str, optional): LoRA adapter name. This can refer to a fully-qualified HuggingFace repo name, e.g. 'foo/bar'. Optional
        - lora_weight_filename (str, optional): The filename within the LoRA repo to load LoRA weights from. Should be a single filename like 'pytorch_lora_weights.safetensors'. Optional. Must be specified if lora_adapter_name is specified.
        - hf_access_key (str, optional): The access key to access HuggingFace to download a LoRA adapter. Specify if your adapter is in a private repo that requires permissions. Optional.
        - output_image_format (str): The format of the generated image. Defaults to "PNG". Options are "PNG" and "JPG". Use PNG for best quality and JPG for best speed. JPG currently only supported for samples=1.

        Returns:
        Image.Image or List[Image.Image]: Modified image or a list of modified images.

        Raises:
        RuntimeError: If there is an error in the image generation process.
        """
        # Argument Validation
        # Construct and validate request fields.
        # NB: prompt and control_image are not used here. Instead, we construct
        # them specially to be sent as multipart/form-data
        request_body = ControlNetRequestBody(
            prompt=prompt,
            negative_prompt=negative_prompt,
            cfg_scale=cfg_scale,
            clip_guidance_preset=clip_guidance_preset,
            sampler=sampler,
            samples=samples,
            steps=steps,
            seed=seed,
            style_preset=style_preset,
            control_net_name=control_net_name,
            step_schedule_start=step_schedule_start,
            step_schedule_end=step_schedule_end,
            conditioning_scale=conditioning_scale,
            safety_check=safety_check,
            lora_adapter_name=lora_adapter_name,
            lora_weight_filename=lora_weight_filename,
        )
        payload_dict = request_body.dict()

        headers = {"Authorization": f"Bearer {self.api_key}"}
        if samples == 1:
            headers["Accept"] = "image/png"
        else:
            headers["Accept"] = "application/json"
        if samples == 1:
            if output_image_format in {"JPG", "JPEG"}:
                headers["Accept"] = "image/jpeg"
            elif output_image_format == "PNG":
                headers["Accept"] = "image/png"
            else:
                raise ValueError(
                    f"Unsupported output_image_format: {output_image_format}"
                )
        else:
            if output_image_format == "PNG":
                headers["Accept"] = "application/json"
            else:
                raise ValueError(
                    f"Only PNG output image format is supported when samples != 1"
                )

        if client_account_id_header:
            headers["X-Fireworks-Routing-Account-ID"] = client_account_id_header

        if hf_access_key is not None:
            headers["Huggingface-Access-Key"] = hf_access_key

        control_image: bytes = self._img_to_bytes(control_image)

        files = {
            "control_image": control_image,
        }
        with httpx.Client(
            headers=headers,
            timeout=self.request_timeout,
            **self.client_kwargs,
        ) as client:
            endpoint_base_uri = f"{self.base_url}/image_generation/accounts/{self.account}/models/{self.model}"
            response = client.post(
                f"{endpoint_base_uri}/control_net",
                data=payload_dict,
                files=files,
            )
            self._error_handling(response)
        if samples == 1:
            finish_reason = response.headers.get("finish-reason", "SUCCESS")
            return Answer(
                image=Image.open(io.BytesIO(response.content)),
                finish_reason=finish_reason,
            )
        else:
            return [
                Answer(
                    Image.open(io.BytesIO(base64.b64decode(artifact["base64"]))),
                    finish_reason=artifact["finishReason"],
                )
                for artifact in response.json()
            ]

    def canny_edge_detection(
        self,
        image: Union[Image.Image, str, os.PathLike, bytes],
        min_val: float = 100,
        max_val: float = 200,
    ) -> Image.Image:
        image: bytes = self._img_to_bytes(image)

        headers = {"Authorization": f"Bearer {self.api_key}"}

        files = {
            "image": image,
        }
        with httpx.Client(
            headers=headers,
            timeout=self.request_timeout,
            **self.client_kwargs,
        ) as client:
            endpoint_base_uri = f"{self.base_url}/image_generation/accounts/{self.account}/models/{self.model}"
            response = client.post(
                f"{endpoint_base_uri}/canny_edge_detection",
                files=files,
                data={"min_val": min_val, "max_val": max_val},
            )
            self._error_handling(response)

        return Image.open(io.BytesIO(response.content))
