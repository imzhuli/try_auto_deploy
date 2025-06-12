import paramiko

class RemoteRunner:
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

    def upload_file(self, local_path, remote_path, extra_stat = None):
        """防止传入pathlib.Path"""
        remote_path = str(remote_path) 
        if not self.client:
            raise Exception("Not connected to a server")
        with self.client.open_sftp() as sftp:
            sftp.put(local_path, remote_path)
            if type(extra_stat) == int:
                current_permissions = sftp.stat(remote_path).st_mode
                new_persissions = current_permissions | extra_stat
                sftp.chmod(remote_path, new_persissions)
        return
    




# 示例用法
