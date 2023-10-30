from abc import abstractmethod
from unpacker.hi_module_file_entry import HiModuleFileEntry
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_elemnts.tag_element import ComplexTagElement, TagElement


class TagElementDict(ComplexTagElement):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        self.dict : dict= None

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        self.dict = dict()

    @classmethod    
    def hash(cls):
        return ""

class RootTagElement(TagElementDict):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        assert layout.T == TagElemntType.RootTagInstance
        self.tagEntryFile: HiModuleFileEntry= None

    def onFullRead(self):
        pass

class StructTagElement(TagElementDict):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        assert layout.T == TagElemntType.Struct

class ChildTagElement(TagElementDict):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        self.index: int = -1
        assert layout.T in [TagElemntType.Array, TagElemntType.Block, TagElemntType.RootTagInstance, TagElemntType.ResourceHandle]  
            