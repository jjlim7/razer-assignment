from openai import AsyncOpenAI
from flask import current_app


class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance

    def init_app(self, app):
        self.client = AsyncOpenAI(
            api_key=app.config["OPENAI_API_KEY"],
            default_headers={
                "Connection": "close",
            },
        )

    def get_client(self):
        if self.client is None:
            self.client = AsyncOpenAI(
                api_key=current_app.config["OPENAI_API_KEY"],
                default_headers={
                    "Connection": "close",
                },
            )
        return self.client


openai_client = OpenAIClient()
