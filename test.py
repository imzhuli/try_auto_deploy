import test_assets.prepare as prepare
import time
from datetime import datetime
from deploy import DeployService

prepare.exec(clean=False)

if __name__ == "__main__":

    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("当前时间:", formatted_time)

    ##DeployService("./test_assets/server/00-s_server_id_center.yaml")
    ##DeployService("./test_assets/server/01-s_server_list.yaml")
    ##DeployService("./test_assets/server/02-s_config_center.yaml")
    ##DeployService("./test_assets/server/09-s_relay_info_dispatcher.yaml")
    ##DeployService("./test_assets/server/10-s_device_relay.yaml")
    ##DeployService("./test_assets/server/11-s_device_state_relay.yaml")
    ##DeployService("./test_assets/server/12-s_auth_cache.yaml")

    ##DeployService("./test_assets/server/13-s_device_selector.yaml")

    ##DeployService("./test_assets/server/14-s_audit_account.yaml")
    DeployService("./test_assets/server/15-s_pa.yaml")

    ## DeployService("./test_assets/server/80-r_device_audit_to_backend.yaml")

    # DeployService("./test_assets/server/98-t_server_list_downloader.yaml")

    pass
