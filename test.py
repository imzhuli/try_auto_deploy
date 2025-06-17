from deploy import DeployService
import test_assets.prepare as prepare

prepare.exec(clean=False)

if __name__ == "__main__":
    # DeployService("./test_assets/server/00-server-server-id.yaml")
    DeployService("./test_assets/server/01-server-config-center.yaml")
