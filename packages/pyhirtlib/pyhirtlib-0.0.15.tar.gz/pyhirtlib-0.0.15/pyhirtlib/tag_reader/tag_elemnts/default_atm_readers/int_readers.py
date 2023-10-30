import struct
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic


class Qword(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Qword]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('q', f.read(8))[0]

class Dword(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Dword]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('i', f.read(4))[0]


class Word(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Word]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('h', f.read(2))[0]


class Byte(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Byte]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('b', f.read(1))[0]

class Int64(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Int64]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('q', f.read(8))[0]

class Long(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Long]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('i', f.read(4))[0]


class Short(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Short]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('h', f.read(2))[0]


class CharIntiger(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.CharIntiger]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('b', f.read(1))[0]

