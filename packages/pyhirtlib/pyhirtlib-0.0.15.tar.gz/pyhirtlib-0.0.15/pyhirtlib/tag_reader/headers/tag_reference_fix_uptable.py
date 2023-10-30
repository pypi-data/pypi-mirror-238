"""
class StringTableEntry:
    local
    int
    init_offset = FTell();
    int
    unknown_0x0;
    int
    tag_ref;
    FSeek(init_offset + 0x8);
    int
    string_offset;
    int
    string_index;
    const
    int
    temp_offset = (header.string_offset + (header.string_count * 0x10)) + string_offset;
    const
    string
    str = ReadString(temp_offset);
"""
import struct

from events import Event
from tag_reader.headers.table_entry import TableEntry

from tag_reader.headers.tag_ref_table import TagDependency
from tag_reader.headers.tag_struct_table import TagStruct
from commons.binary_reader_extension import readStringInPlace


class TagReferenceFixup(TableEntry):

    def __init__(self):
        super().__init__()
        self.field_block = -1
        self.field_offset = -1
        self.name_offset = -1
        self.dependency_index = -1
        self.tag_dependency: TagDependency = None
        self.parent_struct: TagStruct = None
        self.str_path = ""
        pass

    def readIn(self, f, header=None):
        self.field_block = struct.unpack('i', f.read(4))[0]
        self.field_offset = struct.unpack('i', f.read(4))[0]
        self.name_offset = struct.unpack('i', f.read(4))[0]
        self.dependency_index = struct.unpack('i', f.read(4))[0]
        if False and (header.string_table_size!=0):
            temp_offset = (header.tag_reference_offset + (header.tag_reference_count * 0x10)) + self.name_offset
            self.str_path = readStringInPlace(f, temp_offset, True)
            pass


class TagReferenceFixupTable:

    def __init__(self):
        self.entries = []
        self.strings = []
        self.onTagReferenceRead = Event()
        pass

        """
        while True:
            char = f.read(1)
            if char == b'\x00':
                return "".join(string)
            string.append(char.decode("utf-8"))
        """

    def AddSubscribersForOnTagReferenceRead(self, objMethod):
        self.onTagReferenceRead += objMethod

    
    def RemoveSubscribersOnTagReferenceRead(self, objMethod):
        self.onTagReferenceRead -= objMethod

    def readStrings(self, f, header, data_block_table, tag_struct_table, tag_dependency_table, verbose=False):
        # f.readline()
        f.seek(header.tag_reference_offset)
        for x in range(header.tag_reference_count):
            entry = TagReferenceFixup()
            self.entries.append(entry)
            entry.entry_index = len(self.entries)-1
            entry.readIn(f, header)
            if entry.field_block >= len(data_block_table.entries):
                debug = True
                assert False
            db = data_block_table.entries[entry.field_block]
            for tag_i in tag_struct_table.entries:
                if tag_i.field_data_block == db:
                    entry.parent_struct = tag_i
                    break
            if entry.parent_struct is None:
                debug =True
            if entry.dependency_index != -1:
                entry.tag_dependency = tag_dependency_table.entries[self.entries[x].dependency_index]
                assert entry.name_offset == entry.tag_dependency.name_offset
            else:
                debug = True
            entry.parent_struct.l_tag_ref.append(entry)
            entry.p_entry_index = len(entry.parent_struct.l_tag_ref)-1
            self.onTagReferenceRead(f, entry)

        if False and (header.string_table_size!=0):
            offset_1 = f.tell()
            lastPos = offset_1 + header.string_table_size
            while offset_1 < lastPos:
                self.strings.append(readStringInPlace(f, offset_1))
                offset_1 = f.tell()
