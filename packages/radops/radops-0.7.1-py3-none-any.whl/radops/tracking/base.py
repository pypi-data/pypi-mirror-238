from abc import ABC, abstractmethod


class Run(ABC):
    @abstractmethod
    def __init__(self, experiment_name: str, name: str = None) -> None:
        pass

    @abstractmethod
    def log_param(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def log_params(self, params: dict) -> None:
        pass

    @abstractmethod
    def log_metric(self, key: str, value: float) -> None:
        pass

    @abstractmethod
    def log_metrics(self, metrics: dict) -> None:
        pass

    @abstractmethod
    def end(self) -> None:
        pass

    @abstractmethod
    def get_params(self) -> dict:
        pass

    @abstractmethod
    def get_metrics(self) -> dict:
        pass
