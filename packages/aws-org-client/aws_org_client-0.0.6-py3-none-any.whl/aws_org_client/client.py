import time
from concurrent.futures import ThreadPoolExecutor
from boto3.session import Session

from aws_org_client.modules import _identity_store, _organizations, _sso_admin
from aws_org_client.modules._logger import Logger


logger = Logger(__name__)


class Client:
    def __init__(self, identity_store_id, instance_arn):
        # [ TODO: load instance_arn & identity_store_id from local config]
        # Input parameters
        self.identity_store_id = identity_store_id
        self.instance_arn = instance_arn

        # Clients
        self.session = Session(profile_name="di-audit", region_name="eu-west-2")
        self.idc_client = _identity_store._IdentityStore(
            identity_store_id=self.identity_store_id
        )
        self.org_client = _organizations._Organizations()
        self.sso_client = _sso_admin._SSOAdmin(instance_arn=self.instance_arn)

        # Data
        self.data = {}

    def _bootstrap(self):
        logger.info(f"Bootstrapping...")
        threads = ["Users", "Groups", "Accounts"]
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(threads)) as executor:
            executor.map(self._update_data, threads)
        execution_time = time.time() - start_time
        logger.info(f"Base data fetched in: {execution_time}")

        # start_time = time.time()
        # account_ids = []
        # for account in self.data['Accounts']:
        #     account_ids.append(account['Id'])
        # with ThreadPoolExecutor(max_workers=len(account_ids)) as executor:
        #     executor.map(self._update_account_permission_sets, account_ids)
        # execution_time = time.time() - start_time
        # print(f"--- permission set assignments fetched in: {execution_time} ---")

    def _update_data(self, target):
        logger.info(f"Updating {target} data...")
        match target:
            case "Users":
                self.data[target] = self.idc_client.list_users()
                return True
            case "Groups":
                self.data[target] = self.idc_client.list_groups()
                return True
            case "Accounts":
                self.data[target] = self.org_client.list_accounts()
                return True
            case "PermissionSets":
                self.data[target] = self.sso_client.list_permission_sets()
                return True
            case _:
                logger.error("Data update requested for unknown target!")
                exit

    def _update_account_permission_sets(self, account_id):
        self.data["Accounts"][account_id][
            "PermissionSets"
        ] = self.sso_client.list_account_permission_sets(account_id)
