import struct
from crc16 import *

class packet:
    '''
    Single packet for SIYI XT6

    STY         : 2 Bytes
    ctrl        : 1 Bytes
    data_len    : 2 Bytes
    seq         : 2 Bytes
    cmd_id      : 1 Bytes
    data        : data_len Bytes
    crc16       : 2 Bytes
    
    <H : 2 Bytes
    <B : 1 Byte

    '''

    def __init__(self) -> None:
        self._stx = 0x6655
        self.ctrl = None
        self._data_len = None
        self.seq = None
        self.cmd_id = None
        self.data = None
        self.crc16 = None

    def __str__(self) -> str:
        return str(self._stx)

    def update_dataLen(self):
        self._data_len = len(self.data)

    def update_crc(self, data):
        self.crc16 = crc_check_16bites(data)

    def pack(self):
        '''
        Serialize and return data
        '''
        self.update_dataLen()
        
        data = b''

        data += struct.pack("<H", self._stx)
        print(data.hex())
        data += struct.pack("<B", self.ctrl)
        print(data.hex())
        data += struct.pack("<H", self._data_len)
        print(data.hex())
        data += struct.pack("<H", self.seq)
        print(data.hex())
        data += struct.pack("<B", self.cmd_id)
        print(data.hex())
        for single_data in self.data:
            data += struct.pack("<B", single_data)
            print(data.hex())
        print(data)
        self.update_crc(data)
        
        data += struct.pack("<H", self.crc16)  
        print(data.hex())
        return data
    
    def unpack(self, data):
        byte_data = list(hex(i) for i in data)

        

    
if __name__ == '__main__':
    singlePacket = packet()
    singlePacket.ctrl = 1
    singlePacket.seq = 0
    singlePacket.cmd_id = 0x19
    singlePacket.data = []

    command = singlePacket.pack()
    print(command.hex())