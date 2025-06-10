import os
import shutil
from pathlib import Path

class ServerDirs:
    def __init__(self, home_dir):
        try:
            hp = Path(home_dir)
            self.bin = hp.joinpath("bin")
            self.conf = hp.joinpath("conf")
            self.data = hp.joinpath("data")
            self.local_data = hp.joinpath("local_data")

            os.makedirs(self.bin, exist_ok=True)
            os.makedirs(self.conf, exist_ok=True)
            os.makedirs(self.data, exist_ok=True)
            os.makedirs(self.local_data, exist_ok=True)

        except (TypeError, AttributeError, ValueError):
            return False


if __name__ == "__main__":
    sd = ServerDirs("/home/zhuli/test/")

