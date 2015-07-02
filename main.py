import logging
import os
from sensomatic.rxutils.scheduler import loop
from sensomatic.ui.persistence.observer import configure_persistence
from sensomatic.ui.server import Server


os.environ["EXECJS_RUNTIME"] = "Node"


def main():
    logging.basicConfig(level=logging.DEBUG)
    server = Server()

    configure_persistence(sensors_list=['door'])
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.finalize()
    loop.close()


if __name__ == "__main__":
    main()
