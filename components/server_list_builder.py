import configparser
import os

class ServerConfigError(Exception):
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
            raise ServerConfigError("缺少[required]")
        required_items = { k: v for k,v in self.config.items("required") }
        sa = required_items.get("server_address")
        if sa is None:
            print("缺少字段: server_address")
        pass
    

    def parse_optional(self):
        if not self.config.has_section("optional"):
            print("缺少[optional], 忽略")
            return
        optional = self.config["optional"]


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
            
                

