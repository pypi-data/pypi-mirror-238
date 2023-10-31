from abc import ABC, abstractmethod


class AbstractNotifier(ABC):
    @abstractmethod
    def send_update(self, message: str):
        pass


class SimpleNotifier(AbstractNotifier):
    def send_update(self, message_type: str, message: str):
        print(f"{message_type}: {message}\n")


class MessageType:
    NOTIFICATION = "notification"
    SUBTASKS = "subtasks"
    EXECUTING = "executing"
    TASK_RESULT = "task_result"
    OODA = "ooda"
