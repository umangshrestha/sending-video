from struct import pack, unpack
from pickle import dumps, loads
from struct import calcsize
from settings import Fmt
from collections import namedtuple


__all__ = [
    "cv_pack",
    "cv_unpack",
]

unpacked = namedtuple("unpacked", [
    "data" ,
    "end_pos"
])


_payload_size: int = calcsize(Fmt)


def cv_pack(in_data)->bytes:
    '''
    This module pickles the incomming data 
    [input] message
    [output] |packed(size of message)| pickles(message)|
    '''
    data = dumps(in_data)
    message_size = pack(Fmt, len(data))
    output = message_size + data
    return output


def cv_unpack(in_data: bytes) -> namedtuple:
    '''
    The data is unpacked using this module
    [input] |packed(size of message)| pickled(message)|
    [output] message
    unpack the payload to get aactual size of message
    unpick the message to that size
    [return] (data, end_pos)        
    '''
    if len(in_data) < _payload_size:
        return unpacked("", -1)
    msg_size, = unpack(Fmt, in_data[:_payload_size])
    start_pos = _payload_size
    end_pos = start_pos+msg_size
    if len(in_data) < end_pos:
        return unpacked("", -1)
    unpacked_output = in_data[start_pos: end_pos]
    output = loads(unpacked_output)
    return unpacked(output, end_pos)

