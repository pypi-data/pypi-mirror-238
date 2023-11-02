from dataclasses import dataclass
from typing import Optional

from .errors import (
    APIEngineMissingError,
    APIKeyMissingError,
    APITypeMissingError,
    APIVersionMissingError,
)


@dataclass
class OpenAIConfig:
    api_key: str
    api_base: Optional[str]

    def __init__(self,
        api_key: str,
        api_base: Optional[str] = None,
    ) -> None:
        self.api_key = api_key
        self.api_base = api_base

    def validate(self) -> None:
        if not self.api_key or not self.api_key.strip():
            raise APIKeyMissingError("OpenAI API key not set. It must be set to make calls to the service.")

@dataclass
class AzureConfig(OpenAIConfig):
    engine: Optional[str]
    api_version: Optional[str]

    def __init__(self,
        api_key: str,
        api_base: Optional[str] = None,
        engine: Optional[str] = None,
        api_version: Optional[str] = None
    ):
        super().__init__(api_key, api_base)
        self.api_version = api_version
        self.engine = engine

    def validate(self) -> None:
        super().validate()

        if self.api_version is None:
            raise APIVersionMissingError(
                "OpenAI API version not set. It must be set to make calls to the service.")

        if self.engine is None:
            raise APIEngineMissingError("Azure engine is not set. It must be set to make calls to the service.")


@dataclass
class AnthropicConfig:
    api_key: str


@dataclass
class ProviderConfig:
    anthropic: Optional[AnthropicConfig] = None
    openai: Optional[OpenAIConfig] = None
    azure: Optional[AzureConfig] = None

    def validate(self) -> None:
        if self.anthropic is None and self.openai is None:
            APIKeyMissingError("At least one provider key must be set in ProviderConfig.")

        if self.openai is not None:
            self.openai.validate()
