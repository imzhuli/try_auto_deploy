import configparser
import os
from string import Template
from pathlib import Path

import components.server_deploy as sd

class ServerConnectionConfig:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.config = config

        self.parse_required()
        self.parse_optional()

        print("初始化完成")
        pass

    # def parse_required(self):
    #     if not self.config.has_section("required"):
    #         raise ServerSectionError("required")
    #     required_items = { k: v for k,v in self.config.items("required") }

    #     server_program = required_items.get("server_program")
    #     if server_program is None:
    #         raise ServerFieldError("server_program")
    #     server_program_version = required_items.get("server_program_version")
    #     if server_program_version is None:
    #         raise ServerFieldError("server_program_version")
    #     server_id = required_items.get("server_id")
    #     if server_id is None:
    #         raise ServerFieldError("server_id")
    #     server_address = required_items.get("server_address")
    #     if server_address is None:
    #         raise ServerFieldError("server_address")
    #     service_home_dir = required_items.get("service_home_dir")
    #     if service_home_dir is None or service_home_dir == "":
    #         raise ServerFieldError("service_home_dir")
    #     config_template_file = required_items.get("config_template_file")
    #     if config_template_file is None or config_template_file == "":
    #         raise ServerFieldError("config_template_file")
    #     with open(config_template_file, "r", encoding="utf-8") as file:
    #         template = file.read()

    #     self.server_program = server_program
    #     self.server_program_version = server_program_version
    #     self.server_id = server_id
    #     self.server_address = server_address
    #     self.home_dir = service_home_dir
    #     self.bin_dir = service_home_dir + "/bin"
    #     self.config_dir = service_home_dir + "/config"
        
    #     self.local_config_template_file = config_template_file
    #     self.template = template

    #     self.template_key_values = {
    #         "server_program":self.server_program,
    #         "server_program_version":self.server_program_version,
    #         "server_id": self.server_id,
    #         "server_address": self.server_address,
    #         "home_dir": self.home_dir,
    #         "bin_dir": self.bin_dir,
    #         "config_dir": self.config_dir,
    #     }
    

    # def parse_optional(self):
    #     if not self.config.has_section("optional"):
    #         return
    #     optional_items = { k: v for k,v in self.config.items("optional") }
    #     template_param_dir=optional_items.get("template_param_dir")
    #     if template_param_dir is not None:
    #         _template_param_dir = Template(template_param_dir)
    #         self.template_param_dir = _template_param_dir.substitute(self.template_key_values)
    #         print(self.template_param_dir)


class ServerListBuilder:

    def __init__(self, home_path):
        if not os.path.isdir(home_path):
            raise RuntimeError("home_path is not a valid directory")
        
        self.home_path = Path(home_path)
        self.server_list_path = self.home_path / "server"
        self.build_server_list()

        
    def build_server_list(self):
        self.servers = []

        entries = os.listdir(self.server_list_path)
        for entry in entries:
            full_path = self.server_list_path / entry
            if not os.path.isfile(full_path):
                raise RuntimeError("non file path exists")
                continue            
            server = sd.ServerDeploy(full_path)


            
                

