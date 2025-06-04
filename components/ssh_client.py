import paramiko
import time

class RemoteServerDeployer:
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.client = None

    def connect(self):
        """建立 SSH 连接"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, self.port, self.username)

    def disconnect(self):
        """断开 SSH 连接"""
        if self.client:
            self.client.close()

    def execute_command(self, command):
        """在远程服务器上执行命令"""
        if not self.client:
            raise Exception("Not connected to a server")

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()

        return exit_status, output, error

    def upload_file(self, local_path, remote_path):
        """上传文件到远程服务器"""
        if not self.client:
            raise Exception("Not connected to a server")

        sftp = self.client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def create_directory(self, directory_path):
        """在远程服务器上创建目录"""
        if not self.client:
            raise Exception("Not connected to a server")

        self.client.exec_command(f"mkdir -p {directory_path}")

# 示例用法
if __name__ == "__main__":
    # 定义服务器列表
    servers = [
        {"hostname": "server1_ip", "port": 22, "username": "username"},
        {"hostname": "server2_ip", "port": 22, "username": "username"}
    ]

    for server_config in servers:
        deployer = RemoteServerDeployer(
            server_config["hostname"],
            server_config["port"],
            server_config["username"]
        )

        try:
            deployer.connect()
            deployer.create_