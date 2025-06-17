import components.server_base as sb
import components.server_config as sc
import components.x as x

import os
import yaml

from pathlib import Path

current_script_path = os.path.abspath(__file__)
current_script_dir = os.path.dirname(current_script_path)


def DeployService(config_file):

    print(f">>> start deployment ---> {config_file}")
    with open(config_file) as config_contents:
        yd = yaml.safe_load(config_contents)

        server_info = yd["server"]
        server_address = server_info["address"]
        server_user = server_info["user"]
        server_home_dir = server_info["home_dir"]

        source = yd["source"]
        source_home = Path(os.path.abspath(source["home_dir"]))
        source_binary_dir = source_home / "service.binary"
        source_config_template_dir = source_home / "service.config.template"
        source_config_temp_output_dir = source_home / "service.config.output.temp"
        source_data_dir = source_home / "service.data"
        source_script_dir = source_home / "service.script"

        source_config_files = source.get("config_files", [])
        source_config_values = source.get("config_values", {})
        source_data_files = source.get("data_files", [])

        for file in source_config_files:
            source_config_template_file_path = source_config_template_dir / file
            sc.make_config(source_config_template_file_path, source_config_temp_output_dir, source_config_values)

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

            config_files = []
            for item in source_config_files:
                full_path = str(source_config_temp_output_dir / item)
                config_files.append(full_path)
            runner.upload_config(config_files)

            data_files = []
            for item in source_data_files:
                full_path = str(source_data_dir / item)
                data_files.append(full_path)
            runner.upload_data(data_files)

            scripts = []
            shared_script_dir = os.path.join(current_script_dir, "shared_scripts")
            for item in os.listdir(shared_script_dir):
                full_path = os.path.join(shared_script_dir, item)
                if not os.path.isfile(full_path):
                    continue
                scripts.append(full_path)
            for item in source_scripts:
                full_path = str(source_script_dir / item)
                scripts.append(full_path)
            runner.upload_script(scripts)

            print("stopping privous service processes")
            _, o, e = runner.run_script(install_script, *(["stop"]))
            print(o, end="")
            print(e, end="")
            print("starting service processes")
            _, o, e = runner.run_script(install_script, *(["start"] + source_config_files))
            print(o, end="")
            print(e, end="")
            print("check service process status")
            _, o, e = runner.run_script(install_script, *(["status"]))
            print(o, end="")
            print(e, end="")
            pass
    print(f"<<< finished deployment")
