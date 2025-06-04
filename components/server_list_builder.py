import configparser
import os
from string import Template

class ServerSectionError(Exception):
    def __init__(self, missing_section):
        super().__init__(f"ServerSectionError:{missing_section}")
    pass


class ServerFieldError(Exception):
    def __init__(self, missing_field):
        super().__init__(f"ServerFieldError:{missing_field}")
    pass

class ServerTemplateError(Exception):
    def __init__(self, template_filename):
        super().__init__(f"ServerFieldError:{template_filename}")
    pass


class ServerConnectionConfig:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.config = config

        self.parse_required()
        self.parse_optional()

        print("初始化完成")
        pass

    def parse_required(self):
        if not self.config.has_section("required"):
            raise ServerSectionError("required")
        required_items = { k: v for k,v in self.config.items("required") }
        try:
            server_program = required_items.get("server_program")
            if server_program is None:
                raise ServerFieldError("server_program")
            server_id = required_items.get("server_id")
            if server_id is None:
                raise ServerFieldError("server_id")
            server_address = required_items.get("server_address")
            if server_address is None:
                raise ServerFieldError("server_address")
            service_home_dir = required_items.get("service_home_dir")
            if service_home_dir is None or service_home_dir == "":
                raise ServerFieldError("service_home_dir")
            config_template_file = required_items.get("config_template_file")
            if config_template_file is None or config_template_file == "":
                raise ServerFieldError("config_template_file")
            with open(config_template_file, "r", encoding="utf-8") as file:
                template = file.read()

            self.server_program = server_program
            self.server_id = server_id
            self.server_address = server_address
            self.home_dir = service_home_dir
            self.bin_dir = service_home_dir + "/bin"
            self.config_dir = service_home_dir + "/config"
            
            self.local_config_template_file = config_template_file
            self.template = template

            self.template_key_values = {
                "server_program":self.server_program,
                "server_id": self.server_id,
                "server_address": self.server_address,
                "home_dir": self.home_dir,
                "bin_dir": self.bin_dir,
                "config_dir": self.config_dir,
            }

        except Exception as e:
            print(f"处理必须字段异常: {e}")
        pass
    

    def parse_optional(self):
        if not self.config.has_section("optional"):
            return
        optional_items = { k: v for k,v in self.config.items("optional") }
        template_param_dir=optional_items.get("template_param_dir")
        if template_param_dir is not None:
            _template_param_dir = Template(template_param_dir)
            self.template_param_dir = _template_param_dir.substitute(self.template_key_values)
            print(self.template_param_dir)



class ServerListBuilder:

    def __init__(self, directory_path):
        entries = os.listdir(directory_path)
        for entry in entries:
            full_path = os.path.join(directory_path, entry)
            if not os.path.isfile(full_path):
                print(f"忽略非文件项: {full_path}")
                continue
            print(f"处理服务器连接信息: {full_path}")
            server = ServerConnectionConfig(full_path)
            
                

