import os
import shutil
import components.x as x
from pathlib import Path
from string import Template


class ServerConfig:

    @staticmethod
    def generate_config(template_dir, config_output_dir, key_values={}, clear_config_dir=True):
        if not isinstance(template_dir, Path):
            template_dir = Path(template_dir)
        if not isinstance(config_output_dir, Path):
            config_output_dir = Path(config_output_dir)

        if os.path.exists(config_output_dir):
            if clear_config_dir:
                shutil.rmtree(config_output_dir)
        os.makedirs(config_output_dir)

        entries = os.listdir(template_dir)
        for entry in entries:
            full_path = template_dir / entry
            if not os.path.isfile(full_path):
                raise RuntimeError("non file path exists")
            ServerConfig._make_config(full_path, config_output_dir, key_values)
        pass

    @staticmethod
    def _make_config(template_file, output_dir, key_values):
        x.rt_assert(isinstance(template_file, Path))
        x.rt_assert(isinstance(output_dir, Path))
        output_file = output_dir / template_file.name
        with open(template_file, "r") as template:
            config_content = Template(template.read()).substitute(key_values)
            with open(output_file, "w") as output:
                output.write(config_content)
        return
