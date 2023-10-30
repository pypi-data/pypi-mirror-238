from tag_reader.tag_elemnts.tag_element_factory import BaseAtomicFactory
from tag_reader.tag_elemnts.default_atm_readers.string_readers import *
from tag_reader.tag_elemnts.default_atm_readers.core_readers import *
from tag_reader.tag_elemnts.default_atm_readers.enum_flags_block import *
from tag_reader.tag_elemnts.default_atm_readers.geom_readers import *
from tag_reader.tag_elemnts.default_atm_readers.int_readers import *


from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic





class TagElementUnk(TagElementAtomic):
    def __init__(self,layout: TagLayouts.C) -> None:
        super().__init__(layout)

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass

class TagElementUnk45(TagElementAtomic):
    def __init__(self,layout: TagLayouts.C) -> None:
        super().__init__(layout)

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass


class DefaultAtomicFactory(BaseAtomicFactory):
    def __init__(self) -> None:
        super().__init__()

    def getTagElemnt(self, layout:TagLayouts.C) -> TagElementAtomic :
        Undefined = -1
        if layout.T == TagElemntType.String:
            return String(layout)
        elif layout.T == TagElemntType.LongString:
            return LongString(layout)
        elif layout.T == TagElemntType.Mmr3Hash:
            return Mmr3Hash(layout)
        elif layout.T == TagElemntType.NotFound03:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.CharIntiger:
            return CharIntiger(layout)
        elif layout.T == TagElemntType.Short:
            return Short(layout)
        elif layout.T == TagElemntType.Long:
            return Long(layout)
        elif layout.T == TagElemntType.Int64:
            return Int64(layout)
        elif layout.T == TagElemntType.Angle:
            return Angle(layout)
        elif layout.T == TagElemntType.StringTag:
            return Mmr3Hash(layout)
        elif layout.T == TagElemntType.CharEnum:
            return CharEnum(layout)
        elif layout.T == TagElemntType.ShortEnum:
            return ShortEnum(layout)
        elif layout.T == TagElemntType.LongEnum:
            return LongEnum(layout)
        elif layout.T == TagElemntType.LongFlags:
            return LongFlags(layout)
        elif layout.T == TagElemntType.WordFlags:
            return WordFlags(layout)
        elif layout.T == TagElemntType.ByteFlags:
            return ByteFlags(layout)
        elif layout.T == TagElemntType.ShortPoint2D:
            return ShortPoint2D(layout)
        elif layout.T == TagElemntType.ShortRectangle2D:
            return ShortRectangle2D(layout)
        elif layout.T == TagElemntType.RgbPixel32:
            return RgbPixel32(layout)
        elif layout.T == TagElemntType.ArgbPixel32:
            return ArgbPixel32(layout)
        elif layout.T == TagElemntType.Real:
            return Real(layout)
        elif layout.T == TagElemntType.Fraction:
            return Fraction(layout)
        elif layout.T == TagElemntType.RealPoint2D:
            return RealPoint2D(layout)
        elif layout.T == TagElemntType.RealPoint3D:
            return RealPoint3D(layout)
        elif layout.T == TagElemntType.RealVector2D:
            return RealVector2D(layout)
        elif layout.T == TagElemntType.RealVector3D:
            return RealVector3D(layout)
        elif layout.T == TagElemntType.RealQuaternion:
            return RealQuaternion(layout)
        elif layout.T == TagElemntType.RealEulerAngles2D:
            return RealEulerAngles2D(layout)
        elif layout.T == TagElemntType.RealEulerAngles3D:
            return RealEulerAngles3D(layout)
        elif layout.T == TagElemntType.Plane2D:
            return Plane2D(layout)
        elif layout.T == TagElemntType.Plane3D:
            return Plane3D(layout)
        elif layout.T == TagElemntType.RealRgbColor:
            return RealRgbColor(layout)
        elif layout.T == TagElemntType.RealARgbColor:
            return RealARgbColor(layout)
        elif layout.T == TagElemntType.RealHsvColor:
            return RealHsvColor(layout)
        elif layout.T == TagElemntType.RealAhsvColor:
            return RealAhsvColor(layout)
        elif layout.T == TagElemntType.ShortBounds:
            return ShortBounds(layout)
        elif layout.T == TagElemntType.AngleBounds:
            return AngleBounds(layout)
        elif layout.T == TagElemntType.RealBounds:
            return RealBounds(layout)
        elif layout.T == TagElemntType.FractionBounds:
            return FractionBounds(layout)
        elif layout.T == TagElemntType.Unmapped27:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.Unmapped28:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.DwordBlockFlags:
            return DwordBlockFlags(layout)
        elif layout.T == TagElemntType.WordBlockFlags:
            return WordBlockFlags(layout)
        elif layout.T == TagElemntType.ByteBlockFlags:
            return ByteBlockFlags(layout)
        elif layout.T == TagElemntType.CharBlockIndex:
            return CharBlockIndex(layout)
        elif layout.T == TagElemntType.CustomCharBlockIndex:
            return CustomCharBlockIndex(layout)
        elif layout.T == TagElemntType.ShortBlockIndex:
            return ShortBlockIndex(layout)
        elif layout.T == TagElemntType.CustomShortBlockIndex:
            return CustomShortBlockIndex(layout)
        elif layout.T == TagElemntType.LongBlockIndex:
            return LongBlockIndex(layout)
        elif layout.T == TagElemntType.CustomLongBlockIndex:
            return CustomLongBlockIndex(layout)
        elif layout.T == TagElemntType.NotFound32:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.NotFound33:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.Pad:
            return Pad(layout)
        elif layout.T == TagElemntType.Skip:
            return Skip(layout)
        elif layout.T == TagElemntType.Explanation:
            return Explanation(layout)
        elif layout.T == TagElemntType.Custom:
            return Custom(layout)
        elif layout.T == TagElemntType.Unmapped3A:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.EndStruct:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.Byte:
            return Byte(layout)
        elif layout.T == TagElemntType.Word:
            return Word(layout)
        elif layout.T == TagElemntType.Dword:
            return Dword(layout)
        elif layout.T == TagElemntType.Qword:
            return Qword(layout)
        elif layout.T == TagElemntType.TagReference:
            return TagReference(layout)
        elif layout.T == TagElemntType.Data:
            return Data(layout)
        elif layout.T == TagElemntType.DataPath:
            return DataPath(layout)
        elif layout.T == TagElemntType.Unmapped45:
            return TagElementAtomic(layout)
        elif layout.T == TagElemntType.NotFound69:
            return TagElementAtomic(layout)
        else:
            return TagElementAtomic(layout)

        