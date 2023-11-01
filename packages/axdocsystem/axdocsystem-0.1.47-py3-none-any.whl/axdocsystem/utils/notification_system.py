from abc import ABC, abstractmethod

class NotificationSystem(ABC):
    @abstractmethod
    async def send(self, receiver: str, content: str, title: str = '', parse_mode: str = 'html'):
        raise NotImplementedError

