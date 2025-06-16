import components.server_base as sb
import components.server_config as sc
import components.x as x

import test_assets.prepare as prepare
import os
import yaml

from pathlib import Path


def DeployService(config_file):

    with open(config_file) as config_contents:
        yd = yaml.safe_load(config_contents)

        server_info = yd["server"]
        server_address = server_info["address"]
        server_user = server_info["user"]
        server_home_dir = server_info["home_dir"]

        source = yd["source"]
        source_home = Path(os.path.abspath(source["home_dir"]))
        source_binary_dir = source_home / "service.binary"
        source_script_dir = source_home / "service.script"
        source_config_template_dir = source_home / "service.config.template"
        source_config_temp_output_dir = source_home / "service.config.output.temp"

        config = source.get("config", [])
        config_values = source.get("config_values", {})

        for file in config:
            config_file_path = source_config_template_dir / file
            print(config_file_path)
            print(config_values)
            sc.make_config(config_file_path, source_config_temp_output_dir, config_values)

        source_binaries = source["binaries"]
        source_scripts = source["scripts"]
        install_script = source.get("install_script")
        with sb.ServerBase(f"{server_user}@{server_address}") as runner:
            x.p(f"make home dir : {server_home_dir}")
            runner.make_remote_dirs(server_home_dir)

            binaries = []
            for item in source_binaries:
                full_path = str(source_binary_dir / item)
                binaries.append(full_path)
            runner.upload_bin(binaries)

            scripts = []
            for item in source_scripts:
                full_path = str(source_script_dir / item)
                scripts.append(full_path)
            runner.upload_script(scripts)

            _, o, e = runner.run_script(install_script)
            print("<<<<<<<<<<")
            print(o)
            print("----------")
            print(e)
            pass


if __name__ == "__main__":
    DeployService("./test_assets/server/00-server-id.yaml")
