import os
from abc import ABC, abstractmethod
import httpx


class AbstractSSAService(ABC):

    @classmethod
    @abstractmethod
    def train(cls, document_path) -> str:
        """
        Starts a session to train a Small Specialist Agent.
        Immediately returns the training session ID, which can be used to
        check the status of the training session, and to retrieve the
        trained agent when the training session is complete.
        """
        pass


class SSAService(AbstractSSAService):
    AISO_API_URL = os.environ.get("AISO_API_URL", "http://149.28.132.159:8000/api")
    AISO_API_KEY = os.environ.get("AISO_API_KEY", "1234567890")

    @classmethod
    def train(cls, document_path):
        """ Call the SSA training service endpoint """

        payload = {
            "name": "document agent",
            "dataset": document_path,
            "indexing_method": {
                "isPromptingFlexibility": True
            },
            "baseMoodel": "llama2",
            "model_size": "7b",
            "compression": "int5",
            "learning_rate": "0.7",
            "api_key": SSAService.AISO_API_URL
        }

        with httpx.Client() as client:
            response = client.post(SSAService.AISO_API_URL + "/train", json=payload)

        return response.json()
    
    @classmethod
    def chat(cls, message, config: dict = {}) -> str:
        """Chat with a Small Specialist Agent."""
        # NOTE: before using chat, the model must be deploy after train

        payload = {
            "user_input": message,
            "endpoint_name":  config.get("endpoint_name"),
        }

        aiso_url = config.get("aiso_url") or SSAService.AISO_API_URL

        with httpx.Client() as client:
            response = client.post(aiso_url + "/api/chat", json=payload)

        return response.json()
