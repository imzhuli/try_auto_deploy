from deploy import DeployService
import test_assets.prepare as prepare

prepare.exec(clean=False)

if __name__ == "__main__":
    DeployService("./test_assets/server/00-server_server_id_center.yaml")
    DeployService("./test_assets/server/01-server_config_center.yaml")
    DeployService("./test_assets/server/02-server_server_list.yaml")
    DeployService("./test_assets/server/10-server_relay_device.yaml")
    DeployService("./test_assets/server/11-server_device_state_relay.yaml")
    DeployService("./test_assets/server/12-server_auth_cache.yaml")
    DeployService("./test_assets/server/22-server_stream_usage_audit_reporter.yaml")

    pass
