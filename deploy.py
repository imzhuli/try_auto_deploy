from components.server_list_builder import ServerListBuilder


if __name__ != "__main__":
    print("非程序入口, 退出")
    exit(1)

print("尝试自动化产部署开始")
try:
    slb = ServerListBuilder("./test_assets")


except Exception as e:
    print(e)


finally:
    print("自动化部署结束")
