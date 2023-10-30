import struct
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic


class Angle(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Angle]
        self.value = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('f', f.read(4))[0]

class ShortPoint2D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ShortPoint2D]
        self.value = None
        self.x = None
        self.y = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('h', f.read(2))[0], struct.unpack('h', f.read(2))[0])
        self.x = self.value[0]
        self.y = self.value[1]

class ShortRectangle2D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ShortRectangle2D]
        self.value = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('h', f.read(2))[0], struct.unpack('h', f.read(2))[0],
                      struct.unpack('h', f.read(2))[0], struct.unpack('h', f.read(2))[0])
        self.x0 = self.value[0]
        self.y0 = self.value[1]
        self.x1 = self.value[2]
        self.y1 = self.value[3]

class RgbPixel32(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RgbPixel32]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('b', f.read(1))[0], struct.unpack('b', f.read(1))[0],
                      struct.unpack('b', f.read(1))[0], struct.unpack('b', f.read(1))[0])
        self.r = self.value[0]
        self.g = self.value[1]
        self.b = self.value[2]
        
class ArgbPixel32(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ArgbPixel32]
        self.value = -1
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('b', f.read(1))[0], struct.unpack('b', f.read(1))[0],
                      struct.unpack('b', f.read(1))[0], struct.unpack('b', f.read(1))[0])
        self.a = self.value[0]
        self.r = self.value[1]
        self.g = self.value[2]
        self.b = self.value[3]

class Real(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Real]
        self.value = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('f', f.read(4))[0]

class Fraction(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Fraction]
        self.value = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = struct.unpack('f', f.read(4))[0]

class RealPoint2D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealPoint2D]
        self.value = None
        self.x = None
        self.y = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]

class RealPoint3D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealPoint3D]
        self.value = None
        self.x = None
        self.y = None
        self.z = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]
        self.z = self.value[2]


class RealVector2D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealVector2D]
        self.value = None
        self.x = None
        self.y = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]

class RealVector3D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealVector3D]
        self.value = None
        self.x = None
        self.y = None
        self.z = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]
        self.z = self.value[2]
    
class RealQuaternion(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealQuaternion]
        self.value = None
        self.x = None
        self.y = None
        self.z = None
        self.w = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0],
                      struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]
        self.z = self.value[2]
        self.w = self.value[3]
    
    
class RealEulerAngles2D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealEulerAngles2D]
        self.value = None
        self.x = None
        self.y = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]

class RealEulerAngles3D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealEulerAngles3D]
        self.value = None
        self.x = None
        self.y = None
        self.z = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]
        self.z = self.value[2]

class Plane2D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Plane2D]
        self.value = None
        self.x = None
        self.y = None
        self.z = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]
        self.z = self.value[2]
    
class Plane3D(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Plane3D]
        self.value = None
        self.x = None
        self.y = None
        self.z = None
        self.w = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0],
                      struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.x = self.value[0]
        self.y = self.value[1]
        self.z = self.value[2]
        self.w = self.value[3]
    
class RealRgbColor(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealRgbColor]
        self.value = None
        self.r = None
        self.g = None
        self.b = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.r = self.value[0]
        self.g = self.value[1]
        self.b = self.value[2]

    
class RealARgbColor(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealARgbColor]
        self.value = None
        self.a = None
        self.r = None
        self.g = None
        self.b = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0],
                      struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.a = self.value[0]
        self.r = self.value[1]
        self.g = self.value[2]
        self.b = self.value[3]

class RealHsvColor(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealRgbColor]
        self.value = None
        self.h = None
        self.s = None
        self.v = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.h = self.value[0]
        self.s = self.value[1]
        self.v = self.value[2]

    
class RealAhsvColor(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealARgbColor]
        self.value = None
        self.a = None
        self.h = None
        self.s = None
        self.v = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0],
                      struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.a = self.value[0]
        self.h = self.value[1]
        self.s = self.value[2]
        self.v = self.value[3]

class ShortBounds(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.ShortBounds]
        self.value = None
        self.min = None
        self.max = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('h', f.read(2))[0], struct.unpack('h', f.read(2))[0])
        self.min = self.value[0]
        self.max = self.value[1]

class AngleBounds(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.AngleBounds]
        self.value = None
        self.min = None
        self.max = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('i', f.read(4))[0], struct.unpack('i', f.read(4))[0])
        self.min = self.value[0]
        self.max = self.value[1]

class RealBounds(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.RealBounds]
        self.value = None
        self.min = None
        self.max = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.min = self.value[0]
        self.max = self.value[1]

class FractionBounds(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.FractionBounds]
        self.value = None
        self.min = None
        self.max = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('f', f.read(4))[0], struct.unpack('f', f.read(4))[0])
        self.min = self.value[0]
        self.max = self.value[1]
    
    