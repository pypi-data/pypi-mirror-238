from abc import ABC, abstractmethod
from pyhirtlib.tag_reader.tag_elemnts.tag_element_dict import ChildTagElement
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic

from tag_reader.tag_layouts import TagLayouts


class BaseAtomicFactory(ABC):
    def __init__(self,) -> None:
        super().__init__()

    @abstractmethod
    def getTagElemnt(self, layout:TagLayouts.C) -> TagElementAtomic :
        pass

class BaseStructTagFactory(ABC):
    def __init__(self,) -> None:
        super().__init__()

    @abstractmethod
    def getTagElemnt(self, layout:TagLayouts.C) -> TagElementAtomic :
        pass
    
    @abstractmethod
    def getChildTagElemnt(self, layout:TagLayouts.C) -> ChildTagElement :
        pass





    
