import struct
from tag_reader.tag_elemnts.tag_element_dict import ChildTagElement
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_elemnts.tag_element import ComplexTagElement, TagElement


class TagElementList(ComplexTagElement):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        self.array : [ChildTagElement]= None
        self.count: int = -1

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        self.array = []
        # self.count
        pass
   

class ResourceHandleTagElement(TagElementList):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)
        assert layout.T == TagElemntType.ResourceHandle
        self.addres_dir_1 = -1
        self.value_hex = ""
        self.str_value = ""
        self.value_int = -1


    def readTagElemnt(self, f, address, field_offset, entry, parent):
        super().readTagElemnt(f, address, field_offset, entry, parent)
        f.seek(address + field_offset)
        self.addres_dir_1 = struct.unpack('Q', f.read(8))[0]
        bin_data = f.read(4)
        self.value = bin_data.hex().upper()
        # self.str_value = getStrInMmr3Hash(self.value)
        self.int_value = int.from_bytes(bin_data, byteorder="little", signed=True)
        self.count = struct.unpack('i', f.read(4))[0]
        pass

class BlockTagElement(TagElementList):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__(layout)  
        assert layout.T == TagElemntType.Block
    
    def readTagElemnt(self, f, address, field_offset, entry, parent):
        super().readTagElemnt(f, address, field_offset, entry, parent)
        f.seek(address + field_offset)
        self.newAddress = struct.unpack('Q', f.read(8))[0]
        self.stringAddress = struct.unpack('Q', f.read(8))[0]
        self.count = struct.unpack('i', f.read(4))[0]
        pass

class ArrayTagElement(TagElementList):
    def __init__(self, layout: TagLayouts.C) -> None:
        super().__init__( layout)    
        assert layout.T == TagElemntType.Array


            
