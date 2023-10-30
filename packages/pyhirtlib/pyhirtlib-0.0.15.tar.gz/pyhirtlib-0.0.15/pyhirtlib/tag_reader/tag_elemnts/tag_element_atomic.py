from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_elemnts.tag_element import TagElement


class TagElementAtomic(TagElement):
    def __init__(self,layout: TagLayouts.C) -> None:
        super().__init__(layout)
        self.value = None

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass

