from abc import ABC, abstractmethod
from typing import Optional


class OriginProtobufGetterBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_origin_protobuf(link_to) -> Optional[str]:
        pass