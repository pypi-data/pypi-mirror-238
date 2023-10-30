from tag_reader.tag_elemnts.tag_element_dict import ChildTagElement, StructTagElement
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_factory import BaseStructTagFactory


class DefaultStructFactory(BaseStructTagFactory):
   
    def __init__(self) -> None:
        super().__init__()

    def getTagElemnt(self, layout:TagLayouts.C) -> StructTagElement :
        return StructTagElement(layout)
    
    def getChildTagElemnt(self, layout:TagLayouts.C) -> ChildTagElement :
        return ChildTagElement(layout)
    