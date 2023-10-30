from typing import List, Optional

from dennis_systems.core.shared_lib.entity.BaseModel import BaseModel


class DefaultService:
    def list(self, limit: int, page: int) -> List[BaseModel]:
        pass

    def save(self, item: BaseModel) -> BaseModel:
        pass

    def delete(self, item: BaseModel) -> BaseModel:
        pass

    def get(self, id: int) -> Optional[BaseModel]:
        pass
