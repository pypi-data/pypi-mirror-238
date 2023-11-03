import requests
from pydantic import BaseModel
from modelhub.common.types import (
    TextGenerationOutput,
    BaseMessage,
    convert_dicts_to_messages,
    convert_messages_to_dicts,
)
from typing import Optional, Dict, List, Any
import json


class ModelhubClient(BaseModel):
    """
    ModelhubClient: A Python client for the Modelhub API
    """

    user_name: str
    """user name for authentication"""
    user_password: str
    """user password for authentication"""
    host: str
    model: str = ""
    """host URL of the Modelhub API"""
    supported_models: List[str] = []
    """list of supported models"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.host = self.host.rstrip("/")
        try:
            self.supported_models = self._get_supported_models()
        except:
            raise ValueError(f"Failed to connect to {self.host}")

    def _get_supported_models(self) -> List[str]:
        """Get a list of supported models from the Modelhub API"""
        response = requests.get(
            self.host + "/models",
        )
        return response.json()["models"]

    def get_supported_params(self, model: str) -> List[str]:
        """
        Get a list of supported parameters for a given model from the Modelhub API
        params:
            model: the model name
        """
        response = requests.get(
            self.host + "/models/" + model,
        )
        return response.json()["params"]

    def chat(
        self,
        prompt: str,
        model: str = "",
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
    ):
        """
        Chat with a model
        params:
            prompt: the prompt to start the chat
            model: the model name
            parameters: the parameters for the model
        """
        model = model or self.model
        if model not in self.supported_models:
            raise ValueError(f"Model {model} not supported")
        parameters["history"] = convert_messages_to_dicts(history)
        response = requests.post(
            self.host + "/chat",
            json={
                "prompt": prompt,
                "model": model or self.model,
                "parameters": parameters,
                "auth": {
                    "user_name": self.user_name,
                    "user_password": self.user_password,
                },
            },
        ).json()
        response["history"] = convert_dicts_to_messages(response["history"])
        return response

    def stream_chat(
        self, prompt: str, model: str, parameters: Dict[str, Any] = {}
    ) -> Any:
        """
        Stream chat with a model
        params:
            prompt: the prompt to start the chat
            model: the model name
            parameters: the parameters for the model
        """
        for token in requests.post(
            self.host + "/chat",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
                "auth": {
                    "user_name": self.user_name,
                    "user_password": self.user_password,
                },
                "stream": True,
            },
            stream=True,
        ).iter_lines(delimiter=b"\r\n\r\n"):
            if token:
                yield json.loads(token[5:])

    def get_embeddings(
        self, prompt: str, model: str, parameters: Dict[str, Any] = {}
    ) -> Any:
        """
        Get embeddings from a model
        params:
            prompt: the prompt to start the chat
            model: the model name
            parameters: the parameters for the model
        """
        response = requests.post(
            self.host + "/embedding",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
                "auth": {
                    "user_name": self.user_name,
                    "user_password": self.user_password,
                },
            },
        )
        return response.json()


class VLMClient(ModelhubClient):
    """Visual Language Model Client"""

    def chat(self, prompt, image_path, model="cogvlm", parameters={}):
        """
        Chat with a model
        params:
            prompt: the prompt to start the chat
            image_path: the path to the image
            model: the model name
            parameters: the parameters for the model
        """
        image_path = requests.post(
            self.host + "/upload",
            files={"file": open(image_path, "rb")},
            params={
                "user_name": self.user_name,
                "user_password": self.user_password,
            },
        ).json()["file_path"]
        parameters["image_path"] = image_path
        return super().chat(prompt, model, parameters)
