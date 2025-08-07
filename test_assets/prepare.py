import os
import shutil
import sys
import components.x as x


def exec(clean=True):
    source_path = "/home/ubuntu/Projects/PPPro/_build/cpp/bin"
    if not os.path.isdir(source_path):
        x.pe("源执行文件目录不存在")
        return False

    server_app_path = "/home/ubuntu/Projects/try_auto_deploy/test_assets/service.binary"
    if not os.path.isdir(server_app_path):
        x.pe("目标执行文件目录不存在")
        return False

    # clean target dir
    if clean:
        for filename in os.listdir(server_app_path):
            file_path = os.path.join(server_app_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Deleted directory: {file_path}")

    for filename in os.listdir(source_path):
        if not filename.startswith("s_") and not filename.startswith("t_") and not filename.startswith("r_") and not filename.startswith("x_"):
            continue

        source_filename = os.path.join(source_path, filename)
        target_filename = os.path.join(server_app_path, filename)
        if os.path.isfile(source_filename):
            shutil.copy(source_filename, target_filename)

    return True
