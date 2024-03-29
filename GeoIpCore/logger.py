import logging
import sys

from colorama import Fore


def GetStdoutLogger(name: str = "GeoIP-logger", type: str = "simple"):
    """Factory function for creating  stdout logger """
    if type == "simple":
        formatter = logging.Formatter(
            f"\n{Fore.YELLOW}[{name}" + "-LOGGER" + f"]{Fore.RESET}" + " <%(levelname)s> %(asctime)s]\n" + f"{Fore.GREEN}" + "%(message)s\n" + f"{Fore.RESET}")
    else:
        formatter = logging.Formatter(
            f"\n{Fore.YELLOW}[{name}" + "-LOGGER" + f"]{Fore.WHITE}" + " <%(levelname)s> %(asctime)s]\n" + f"{Fore.GREEN}" + "\t%(message)s\n" + f"{Fore.RESET}" + "module:%(module)s\n\tat line %(lineno)d in %(pathname)s\n"
        )

    logLevel = logging.INFO
    logger = logging.getLogger(name)
    logger.setLevel(logLevel)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
