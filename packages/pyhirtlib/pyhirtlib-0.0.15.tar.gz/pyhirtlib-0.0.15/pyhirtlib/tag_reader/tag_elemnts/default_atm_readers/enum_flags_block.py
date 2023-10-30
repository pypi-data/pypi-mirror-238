import math
import struct
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def int_to_binary(number: int, num_digits: int = 8) -> str:
    return str(bin(number))[2:].zfill(num_digits)[::-1]

class Enums(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.LongEnum, TagElemntType.ShortEnum, TagElemntType.CharEnum]
        self.value = -1
        self.selected = None
        pass
    
    def asingSelected(self):
        if not self.L.STR is None and self.value>=0 and self.value<len(self.L.STR):
            self.selected = self.L.STR[self.value]
            pass
        else:
            self.selected = None


class LongEnum(Enums):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.LongEnum]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('i', f.read(4))[0]
        self.asingSelected()


class ShortEnum(Enums):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ShortEnum]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('h', f.read(2))[0]
        self.asingSelected()


class CharEnum(Enums):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.CharEnum]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('b', f.read(1))[0]
        self.asingSelected()


class Flags(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.LongFlags, TagElemntType.WordFlags, TagElemntType.ByteFlags]
        self.value = None
        self.bits = None
        self.options = {}
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value =  int.from_bytes(f.read(self.L.A), 'little', signed=True)
        self.generateBits()
        pass

    def generateBits(self):
        self.bits= (int_to_binary(self.value,8*self.L.A))
        for i in range(len(self.L.STR)):
            self.options[self.L.STR[i]] = self.bits[i] == "1"
        

class LongFlags(Flags):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.LongFlags]
        self.value = -1
        pass

    #self.value = struct.unpack('i', f.read(4))[0]
    


class WordFlags(Flags):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.WordFlags]
        self.value = -1
        pass

    #self.value = struct.unpack('h', f.read(2))[0]


class ByteFlags(Flags):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ByteFlags]
        self.value = -1
        pass

    #self.value = struct.unpack('b', f.read(1))[0]

class DwordBlockFlags(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.DwordBlockFlags]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('i', f.read(4))[0]


class WordBlockFlags(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.WordBlockFlags]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('h', f.read(2))[0]


class ByteBlockFlags(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ByteBlockFlags]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('b', f.read(1))[0]

class LongBlockIndex(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.LongBlockIndex]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('i', f.read(4))[0]


class ShortBlockIndex(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ShortBlockIndex]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('h', f.read(2))[0]


class CharBlockIndex(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.CharBlockIndex]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('b', f.read(1))[0]

class CustomLongBlockIndex(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.CustomLongBlockIndex]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('i', f.read(4))[0]


class CustomShortBlockIndex(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.CustomShortBlockIndex]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('h', f.read(2))[0]


class CustomCharBlockIndex(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.CustomCharBlockIndex]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('b', f.read(1))[0]
