import components.server_base as sb
import components.server_config as sc

import test_assets.prepare as prepare

prepare.exec(clean=False)
sc.ServerConfig.generate_config("./test_assets/service.config.template", "./test_assets/service.config.output.temp", key_values={"test_key": "hello world!"})

with sb.ServerBase("root@ts_1") as runner:
    home = "/home/test/hw.1"
    runner.make_remote_dirs(home)
    runner.upload_bin("./test_assets/service.binary/hw")
    runner.upload_config(["./test_assets/service.config.output.temp/00-server-config.ini"])
    # r, o = runner.exec(f"ls {home}")
    # print(o)
    pass
