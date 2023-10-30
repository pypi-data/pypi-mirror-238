import struct
from events import Event, EventParameter
from tag_reader.tag_elemnts.tag_element_type import TagElemntType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_elemnts.tag_element_atomic import TagElementAtomic


class TagReference(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.TagReference]
        self.value = None
        self.ref_id_center = None
        self.ref_id_sub = None
        self.ref_id = None
        self.ref_id_center_int = None
        self.ref_id_sub_int = None
        self.ref_id_int = None
        self.global_handle = None
        self.local_handle = None
        self.tagGroup = None
        self.tagGroupRev = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('q', f.read(8))[0],struct.unpack('i', f.read(4))[0],struct.unpack('i', f.read(4))[0],
                      struct.unpack('i', f.read(4))[0],struct.unpack('4s', f.read(4))[0]) 
        self.global_handle = self.value[0]
        self.ref_id = f.read(4)
        self.ref_id_int = self.value[1]
        self.ref_id = self.ref_id.hex().upper()
        self.ref_id_sub = f.read(4)
        self.ref_id_sub_int = self.value[2]
        self.ref_id_sub = self.ref_id_sub.hex().upper()
        self.ref_id_center = f.read(4)
        self.ref_id_center_int = self.value[3]
        self.ref_id_center = self.ref_id_center.hex().upper()
        self.tagGroup = self.value[4]
        if self.tagGroup != b'\xff\xff\xff\xff':
            self.tagGroupRev = self.tagGroup[::-1].decode("utf-8")

class Data(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Data]
        self.value = None
        self.funct_address0 = None
        self.funct_address1 = None
        self.byte_offset = None
        self.byte_len = None
        self.onSetReference = Event()
        self.data_reference_info = None
        self.datas_bytes = b''
        pass

    def AddSubscribersForOnSetReference(self, objMethod):
        self.onSetReference += objMethod

    
    def RemoveSubscribersOnSetReference(self, objMethod):
        self.onSetReference -= objMethod

    def setDataReferenceInfo(self, f, data_reference_info):
        self.data_reference_info = data_reference_info
        event_p = EventParameter(False)
        self.onSetReference(event_p)
        if event_p.value is True:
            assert self.byte_len == self.data_reference_info[1]
            to_return = f.tell()
            f.seek(self.data_reference_info[0])
            self.datas_bytes = f.read(self.byte_len)
            f.seek(to_return)
            


    def readTagElemnt(self, f, address, field_offset, entry, parent):
        f.seek(address + field_offset)
        self.value = (struct.unpack('Q', f.read(8))[0],struct.unpack('Q', f.read(8))[0],
                      struct.unpack('i', f.read(4))[0], struct.unpack('i', f.read(4))[0] ) 
        self.funct_address0 = self.value[0]
        self.funct_address1 = self.value[1]
        self.byte_offset = self.value[2]
        self.byte_len = self.value[3]

class Pad(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Pad]
        self.value = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass

class Skip(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Skip]
        self.value = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass

class Explanation(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Explanation]
        self.value = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass

class Custom(TagElementAtomic):
    def __init__(self, layout: TagLayouts.C):
        super().__init__(layout)
        assert layout.T in [TagElemntType.Custom]
        self.value = None
        pass

    def readTagElemnt(self, f, address, field_offset, entry, parent):
        pass
 