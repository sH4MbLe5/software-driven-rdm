from abc import ABC, abstractclassmethod
from typing import List

class SchemaParser(ABC):

    objs: List
    inherits: List
    compositions: List
    module_name: str = ""

    @abstractclassmethod
    def parse(self, path: str):
        raise NotImplementedError()