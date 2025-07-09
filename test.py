from deploy import DeployService
import test_assets.prepare as prepare

prepare.exec(clean=False)

if __name__ == "__main__":
    # DeployService("./test_assets/server/00-s_server_id_center.yaml")
    # DeployService("./test_assets/server/01-server_config_center.yaml")
    # DeployService("./test_assets/server/02-s_server_list.yaml")
    # DeployService("./test_assets/server/10-server_relay_device.yaml")
    # DeployService("./test_assets/server/11-server_device_state_relay.yaml")
    DeployService("./test_assets/server/12-s_auth_cache.yaml")
    # DeployService("./test_assets/server/15-s_pa.yaml")
    # DeployService("./test_assets/server/21-server_audit_device.yaml")
    # DeployService("./test_assets/server/22-server_audit_account.yaml")
    DeployService("./test_assets/server/99-t_auth_cache_client.yaml")

    pass
