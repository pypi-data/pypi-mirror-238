from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from abc import ABC, abstractmethod

class TagElement(ABC):
    def __init__(self, layout: TagLayouts.C) -> None:
        self.L : TagLayouts.C = layout
        self.parent: TagElement = None


    @abstractmethod    
    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass

       
    def onStartEnd(self, start):
        pass

class ComplexTagElement(TagElement):
    def __init__(self, layout: TagLayouts.P) -> None:
        super().__init__(layout)