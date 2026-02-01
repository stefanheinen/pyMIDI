from abc import ABC, abstractmethod

class EventToAppMap(ABC):
    # NAME is used for identifying the EventToAppMap in the status icon menu
    NAME: str

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def shutdown(self, wait=False):
        pass

    @abstractmethod
    def shutdown_join(self, wait=False):
        pass

    @abstractmethod
    def handle_event(self, event: str):
        pass