import json
from dataclasses import dataclass
from typing import List
import os

@dataclass
class ModelConfig:
    authorization: str
    tokenKey: str
    llmApiName: str
    tokenId: str


class AppConfig:
    def __init__(self, json_path: str):
        self.models: List[ModelConfig] = []
        self.load(json_path)

    def load(self, json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)   # data là list

        for item in data:
            self.models.append(ModelConfig(**item))

    def get_by_api_name(self, api_name: str) -> ModelConfig | None:
        for m in self.models:
            if m.llmApiName == api_name:
                return m
        return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "api-keys.json")

config  = AppConfig(CONFIG_PATH)