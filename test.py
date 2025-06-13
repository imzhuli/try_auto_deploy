import components.server_base as sb
import components.server_config as sc

import test_assets.prepare as prepare
import os

prepare.exec(clean=False)
sc.ServerConfig.generate_config("./test_assets/service.config.template", "./test_assets/service.config.output.temp", key_values={"test_key": "hello world!"})

with sb.ServerBase("root@ts_1") as runner:
    home = "/home/test/hw.1"
    runner.make_remote_dirs(home)

    binary_source_dir = "./test_assets/service.binary"
    binaries = []
    for item in os.listdir(binary_source_dir):
        full_path = os.path.join(binary_source_dir, item)
        binaries.append(full_path)
    # runner.upload_bin(binaries)

    runner.upload_config(["./test_assets/service.config.output.temp/00-server-config.ini"])

    script_source_dir = "./test_assets/service.script"
    script_source_files = ["get_pid_by_full_path.sh"]
    scripts = []
    for item in script_source_files:
        full_path = os.path.join(script_source_dir, item)
        scripts.append(full_path)
    runner.upload_script(scripts)

    _, o, _ = runner.run_script("get_pid_by_full_path.sh", "/usr/bin/python3")
    print(o)

    pass
