import struct


def readStringInPlace(f, start, inplace=False):
    toBack = f.tell()
    f.seek(start)
    string = []
    while True:
        char = f.read(1)
        if char == b'\x00':
            if inplace:
                f.seek(toBack)
            return "".join(string)
        try:
            string.append(char.decode("utf-8"))
        except:
            try:
                char += f.read(1)
                string.append(char.decode("utf-8"))
            except:
                if inplace:
                    f.seek(toBack)
                return "".join(string)

def readStringOnBytes(bytes):
    string = []
    for i, byte in enumerate(bytes):
        char = (byte).to_bytes(1, byteorder='little')
        #char = bytes[i] 
        if char == b'\x00':
            return "".join(string)
        else:
            string.append(char.decode("utf-8"))
        
    return "".join(string)