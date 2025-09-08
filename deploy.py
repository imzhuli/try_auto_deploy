import components.server_base as sb
import components.server_config as sc
import components.x as x

import os
import time
import yaml
import shlex

from pathlib import Path

current_script_path = os.path.abspath(__file__)
current_script_dir = os.path.dirname(current_script_path)


def DeepMerge(src, override):
    for key in override:
        if key in src:
            if isinstance(src[key], dict) and isinstance(override[key], dict):
                DeepMerge(src[key], override[key])
            else:
                src[key] = override[key]
        else:
            src[key] = override[key]
    return src


def DeployService(config_file, override_file=None):

    od = {}
    print(f"override_file: {override_file}")
    if override_file is not None:
        with open(override_file) as config_override_contents:
            od = yaml.safe_load(config_override_contents)
    print(f">> config override: ===> {od}")

    print(f">>> start deployment ============> {config_file}")
    with open(config_file) as config_contents:
        yd = yaml.safe_load(config_contents)
        DeepMerge(yd, od)

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

        source_config_files = source.get("config_files")
        source_config_files = source_config_files if source_config_files is not None else []
        source_config_values = source.get("config_values")
        source_config_values = source_config_values if source_config_values is not None else {}
        source_data_files = source.get("data_files")
        source_data_files = source_data_files if source_data_files is not None else []

        pre_defined_config_home_dir = source_config_values.get("home_dir", server_home_dir)
        pre_defined_source_config_values = {
            "HOME_DIR": pre_defined_config_home_dir,
            "BIN_DIR": os.path.join(pre_defined_config_home_dir, "bin"),
            "CACHE_DIR": os.path.join(pre_defined_config_home_dir, "cache"),
            "CONFIG_DIR": os.path.join(pre_defined_config_home_dir, "config"),
            "DATA_DIR": os.path.join(pre_defined_config_home_dir, "data"),
            "SCRIPT_DIR": os.path.join(pre_defined_config_home_dir, "script"),
        }
        source_config_values = {**pre_defined_source_config_values, **source_config_values}
        for file in source_config_files:
            source_config_template_file_path = source_config_template_dir / file
            sc.make_config(source_config_template_file_path, source_config_temp_output_dir, source_config_values)

        source_binaries = source["binaries"]
        source_scripts = source.get("scripts")
        source_scripts = source_scripts if source_scripts is not None else []
        install_script = source.get("install_script", None)

        with sb.ServerBase(f"{server_user}@{server_address}") as runner:
            x.p(f"make home dir : {server_home_dir}")
            runner.make_remote_dirs(server_home_dir)

            binaries = []
            for item in source_binaries:
                full_path = source_binary_dir / item
                binaries.append(shlex.quote(str(full_path)))
            runner.upload_bin(binaries)

            config_files = []
            for item in source_config_files:
                full_path = str(source_config_temp_output_dir / item)
                config_files.append(shlex.quote(str(full_path)))
            runner.upload_config(config_files)

            data_files = []
            for item in source_data_files:
                full_path = str(source_data_dir / item)
                data_files.append(shlex.quote(str(full_path)))
            runner.upload_data(data_files)

            scripts = []
            shared_script_dir = os.path.join(current_script_dir, "shared_scripts")
            for item in os.listdir(shared_script_dir):
                full_path = os.path.join(shared_script_dir, item)
                if not os.path.isfile(full_path):
                    continue
                scripts.append(shlex.quote(str(full_path)))
            for item in source_scripts:
                full_path = source_script_dir / item
                scripts.append(shlex.quote(str(full_path)))
            runner.upload_script(scripts)

            print("install_script =", install_script)
            if install_script is not None:
                print("stopping privous service processes")
                _, o, e = runner.run_script(install_script, *(["stop"]))
                print(o, end="")
                print(e, end="")
                print("starting service processes")
                time.sleep(1)
                _, o, e = runner.run_script(install_script, *(["start"] + source_config_files))
                print(o, end="")
                print(e, end="")
                print("check service process status")
                time.sleep(1)
                _, o, e = runner.run_script(install_script, *(["status"]))
                print(o, end="")
                print(e, end="")
            else:
                remote_home_full_path = shlex.quote(str(runner.dirs.home))
                remote_service_controller_full_path = shlex.quote(str(runner.dirs.script / "service_control.sh"))
                for item in source_binaries:
                    stop_cmd = f"cd {remote_home_full_path}; {remote_service_controller_full_path} stop {item}"
                    start_cmd = f"cd {remote_home_full_path}; {remote_service_controller_full_path} start {item} { " ".join(source_config_files)}"
                    check_cmd = f"cd {remote_home_full_path}; {remote_service_controller_full_path} status {item}"
                    print("stopping privous service processes")
                    _, o, e = runner.execute_command(stop_cmd)
                    print(o, end="")
                    print(e, end="")
                    print("starting service processes")
                    time.sleep(1)
                    _, o, e = runner.execute_command(start_cmd)
                    print(o, end="")
                    print(e, end="")
                    print("check service process status")
                    time.sleep(1)
                    _, o, e = runner.execute_command(check_cmd)
                    print(o, end="")
                    print(e, end="")
            pass
    print(f"<<< finished deployment ==================================================")
