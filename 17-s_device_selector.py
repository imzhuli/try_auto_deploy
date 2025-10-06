import test_assets.prepare as prepare
import time
import sys
from datetime import datetime
from deploy import DeployService

prepare.exec(clean=False)

if __name__ == "__main__":
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("当前时间:", formatted_time)
    DeployService("./test_assets/server/17-s_device_selector.yaml", prepare.OverrideFilePath)
