import components.ssh_client as sc
import components.x as x
import stat
import shlex
from pathlib import Path


class ServerBase:

    def __init__(self, server_schema):
        host, port, username = x.parse_url(server_schema)
        print(host, port, username)
        self.runner = sc.RemoteRunner(host, port, username)

    def __enter__(self):
        self.runner.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"exception: {exc_type.__name__}, msg: {exc_val}, call_stack: {exc_tb}")
        self.runner.disconnect()
        return True  # 抑制异常

    def exec(self, command):
        r, output, _ = self.runner.execute_command(command)
        return r, output

    def create_remote_directory(self, directory_path):
        r, _, _ = self.runner.execute_command(f"mkdir -p {directory_path}")
        return r

    def make_remote_dirs(self, remote_home_dir):
        if not hasattr(self, "dirs"):
            print("build dirs")
        home_path = Path(remote_home_dir)

        self.dirs = x.Object()
        self.dirs.home = home_path
        self.dirs.bin = home_path / "bin"
        self.dirs.config = home_path / "config"
        self.dirs.data = home_path / "data"
        self.dirs.cache = home_path / "cache"
        self.dirs.script = home_path / "script"

        sum = 0
        sum = sum | self.create_remote_directory(self.dirs.home)
        sum = sum | self.create_remote_directory(self.dirs.bin)
        sum = sum | self.create_remote_directory(self.dirs.config)
        sum = sum | self.create_remote_directory(self.dirs.data)
        sum = sum | self.create_remote_directory(self.dirs.cache)
        sum = sum | self.create_remote_directory(self.dirs.script)
        if sum != 0:
            del self.dirs
            return False
        return True

    def upload_bin(self, local_filename, force=False):
        if type(local_filename) == str:
            self.runner.upload_file(local_filename, self.dirs.bin / Path(local_filename).name, extra_stat=stat.S_IXUSR, force=force)
            return
        if type(local_filename) == list or type(local_filename) == tuple:
            for item in local_filename:
                if type(item) != str:
                    raise RuntimeError("invalid param type")
                self.runner.upload_file(item, self.dirs.bin / Path(item).name, extra_stat=stat.S_IXUSR, force=force)
        return

    def upload_config(self, local_filename, force=False):
        if type(local_filename) == str:
            self.runner.upload_file(local_filename, self.dirs.config / Path(local_filename).name, force=force)
            return
        if type(local_filename) == list or type(local_filename) == tuple:
            for item in local_filename:
                if type(item) != str:
                    raise RuntimeError("invalid param type")
                self.runner.upload_file(item, self.dirs.config / Path(item).name, force=force)
        return

    def upload_data(self, local_filename, force=False):
        if type(local_filename) == str:
            self.runner.upload_file(local_filename, self.dirs.data / Path(local_filename).name, force=force)
            return
        if type(local_filename) == list or type(local_filename) == tuple:
            for item in local_filename:
                if type(item) != str:
                    raise RuntimeError("invalid param type")
                self.runner.upload_file(item, self.dirs.data / Path(item).name, force=force)
        return

    def upload_script(self, local_filename, force=False):
        if type(local_filename) == str:
            self.runner.upload_file(local_filename, self.dirs.script / Path(local_filename).name, extra_stat=stat.S_IXUSR, force=force)
            return
        if type(local_filename) == list or type(local_filename) == tuple:
            for item in local_filename:
                if type(item) != str:
                    raise RuntimeError("invalid param type")
                self.runner.upload_file(item, self.dirs.script / Path(item).name, extra_stat=stat.S_IXUSR, force=force)
        return

    def run_script(self, script_filename, *args, cwd=None):
        if cwd is None:
            cwd = shlex.quote(str(self.dirs.home))
        full_scirpt_path = shlex.quote(str(self.dirs.script / script_filename))
        quoted = []
        for arg in args:
            quoted.append(shlex.quote(str(arg)))

        cmd = f"cd {cwd}; {full_scirpt_path} {' '.join(quoted)}"
        print(cmd)

        return self.runner.execute_command(cmd)
