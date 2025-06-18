import paramiko
import subprocess


def _get_system_md5(file_path):
    try:
        # 调用系统的md5sum命令
        output = subprocess.check_output(["md5sum", file_path], text=True)
        # 解析输出（格式为：MD5哈希值 文件名）
        md5_value = output.split()[0]
        return md5_value
    except subprocess.CalledProcessError as e:
        # print(f"Error calculating MD5: {e}")
        return None
    except FileNotFoundError:
        # print("Error: md5sum command not found (Linux/macOS only).")
        return None


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

        _, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()

        return exit_status, output, error

    def upload_file(self, local_path, remote_path, extra_stat=None, force=False):
        """防止传入pathlib.Path"""
        remote_path = str(remote_path)
        if not self.client:
            raise Exception("Not connected to a server")

        if not force:
            local_checksum = _get_system_md5(local_path)
            if local_checksum is None:
                force = True
            else:
                cmd = f"md5sum {remote_path!r}"
                _, remote_checksum, _ = self.execute_command(cmd)
                if remote_checksum is None:
                    remote_checksum = ""
                remote_checksum = remote_checksum.split(" ")[0]
                if remote_checksum != local_checksum:
                    force = True

        if force:
            print(f"upload file: (local){local_path!r} --> (remote){remote_path!r}")
            self.execute_command(f"rm {remote_path!r}")
            with self.client.open_sftp() as sftp:
                sftp.put(local_path, remote_path)
                if type(extra_stat) == int:
                    current_permissions = sftp.stat(remote_path).st_mode
                    new_persissions = current_permissions | extra_stat
                    sftp.chmod(remote_path, new_persissions)
        else:
            print(f"upload file omitted, checksum match (md5={local_checksum}) (local){local_path!r} --> (remote){remote_path!r}")

        return


# 示例用法
