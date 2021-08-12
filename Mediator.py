from abc import abstractmethod



class Mediator:
    @abstractmethod
    def notify(self, component: object) -> None:
        pass
