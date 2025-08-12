import test_assets.prepare as prepare
import time
from datetime import datetime
from deploy import DeployService

prepare.exec(clean=False)

if __name__ == "__main__":

    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("当前时间:", formatted_time)

    DeployService("./test_assets/server/00-s_server_id_center.yaml")

    ## DeployService("./test_assets/server/01-s_config_center.yaml")
    ## DeployService("./test_assets/server/02-s_server_list.yaml")

    ## DeployService("./test_assets/server/09-s_relay_info_dispatcher.yaml")

    ## DeployService("./test_assets/server/10-s_device_relay.yaml")
    ## DeployService("./test_assets/server/10-s_device_relay.yaml.1")

    ## DeployService("./test_assets/server/11-s_device_state_relay.yaml")
    ## DeployService("./test_assets/server/11-s_device_state_relay.yaml.1")

    ## DeployService("./test_assets/server/12-s_auth_cache.yaml")
    ## DeployService("./test_assets/server/12-s_auth_cache.yaml.1")

    # DeployService("./test_assets/server/16-s_device_selector_dispatcher.yaml")
    # DeployService("./test_assets/server/16-s_device_selector_dispatcher.yaml.1")

    ## DeployService("./test_assets/server/17-s_device_selector.yaml")
    ## DeployService("./test_assets/server/17-s_device_selector.yaml.1")

    ## DeployService("./test_assets/server/14-s_audit_account.yaml")

    ## DeployService("./test_assets/server/15-s_pa.yaml")

    ## DeployService("./test_assets/server/80-r_device_audit_to_backend.yaml")

    ## DeployService("./test_assets/server/99-s_address_test.yaml")
    ## DeployService("./test_assets/server/a0-x_device.yaml")

    ## time.sleep(15)
    ##DeployService("./test_assets/server/98-t_server_list_downloader.yaml")

    pass
