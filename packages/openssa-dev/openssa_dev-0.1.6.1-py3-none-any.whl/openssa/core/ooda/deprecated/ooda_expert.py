import os
from abc import ABC, abstractmethod

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


class AbstractOODAExpert(ABC):
    """Abstract class for an OODA expert."""

    @abstractmethod
    def query(self):
        """Query the OODA model for a response to a given message."""
        pass


class BaseOODAExpert(AbstractOODAExpert):
    """Base class for an OODA expert."""

    def query(self, history):
        """
        Ask the language model that is an expert in planning the problem-solving process to perform
        a chat completion. Update the chat history with the system's response. The new prompt is
        already in the history.
        """
        completions = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=history)
        return completions["choices"][0]["message"]["content"]
