from abc import abstractmethod
from typing import Mapping, Optional

import torch
from torch import nn


class Transform(nn.Module):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name: str = name
        self.fitted: bool = False

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"


class Independent(Transform):
    @abstractmethod
    def _fit(self, data: torch.Tensor, *args, **kwargs) -> Mapping[str, torch.Tensor]:
        raise NotImplementedError

    def fit(self, data: torch.Tensor, *args, **kwargs) -> None:
        for key, value in self._fit(data=data, *args, **kwargs).items():
            self.register_buffer(key, value)
        self.fitted: bool = True

    def forward(self, x: torch.Tensor, *args, **kwargs) -> torch.Tensor:
        raise NotImplementedError

    def reverse(self, x: torch.Tensor, *args, **kwargs) -> torch.Tensor:
        raise NotImplementedError


class Joint(Transform):
    @abstractmethod
    def _fit(self, source_data: torch.Tensor, target_data: torch.Tensor, *args, **kwargs) -> Mapping[str, torch.Tensor]:
        raise NotImplementedError

    def fit(self, source_data: torch.Tensor, target_data: torch.Tensor, *args, **kwargs) -> None:
        for key, value in self._fit(source_data=source_data, target_data=target_data, *args, **kwargs).items():
            self.register_buffer(key, value)
        self.fitted: bool = True

    def forward(
        self, source_x: Optional[torch.Tensor], target_x: Optional[torch.Tensor], *args, **kwargs
    ) -> torch.Tensor:
        raise NotImplementedError

    def reverse(
        self, source_x: Optional[torch.Tensor], target_x: Optional[torch.Tensor], *args, **kwargs
    ) -> torch.Tensor:
        raise NotImplementedError
