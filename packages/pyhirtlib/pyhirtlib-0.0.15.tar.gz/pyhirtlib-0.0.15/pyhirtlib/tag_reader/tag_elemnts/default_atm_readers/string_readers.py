import struct
from commons.binary_reader_extension import readStringOnBytes
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic


class String(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.String]
        self.value = ""
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = readStringOnBytes(f.read(32))
        # self.value = struct.unpack('32s', f.read(32))[0].decode("utf-8")
        pass

class LongString(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.LongString]
        self.value = ""
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = readStringOnBytes(f.read(256))
        # self.value = struct.unpack('256s', f.read(256))[0].decode("utf-8")     
        pass

class Mmr3Hash(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Mmr3Hash]
        self.value = ""
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = f.read(4).hex().upper()
        pass


class StringTag(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.StringTag]
        self.value = ""
        self.value_rev = ""
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('4s', f.read(4))[0]
        self.value_rev = self.value[::-1].decode("utf-8")
        pass

class DataPath(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.DataPath]
        self.value = ""
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('4s', f.read(256))[0].decode("utf-8")  
        