import time
import os
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor
from boto3.session import Session

from aws_org_client.modules import identity_store, organizations, sso_admin
from aws_org_client.modules.logger import Logger


logger = Logger(__name__)
PROFILE = os.environ["AWS_PROFILE"]


class Client:
    def __init__(self, identity_store_id: str, instance_arn: str):
        """Initialise client for organisation & identity services.

        Args:
            identity_store_id (str): The globally unique identifier for the identity store.
            instance_arn (str): The ARN of the IAM Identity Center instance under which the operation will be executed.
        """
        # [ TODO: load instance_arn & identity_store_id from local config ]
        # Input parameters
        self.identity_store_id = identity_store_id
        self.instance_arn = instance_arn

        # Clients
        self.session = Session(profile_name=PROFILE, region_name="eu-west-2")
        self.idc_client = identity_store.IdentityStore(
            identity_store_id=self.identity_store_id
        )
        self.org_client = organizations.Organizations()
        self.sso_client = sso_admin.SSOAdmin(instance_arn=self.instance_arn)

        # Data
        self.data = {}

    def _bootstrap(self):
        """Fetch base data for client. Runs _update_data() method in threads."""

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

    def _update_data(self, target: str):
        """Fetch specified data object & update base data dictionary

        Args:
            target (str): AWS object to fetch.
        """
        logger.info(f"Updating {target} data...")
        match target:
            case "Users":
                self.data[target] = self.idc_client.list_users()

            case "Groups":
                self.data[target] = self.idc_client.list_groups()

            case "Accounts":
                self.data[target] = self.org_client.list_accounts()

            case "PermissionSets":
                self.data[target] = self.sso_client.list_permission_sets()

            case _:
                logger.error("Data update requested for unknown target!")
                exit

    def _update_account_permission_sets(self, account_id: str):
        """Fetch permission sets assigned to specified account.

        Args:
            account_id (str): Unique identitied of AWS account.
        """
        # this code is ignored by the black formatter because it unnecessarily
        # formats the "PermissionSets" key as a multi-line object
        # fmt: off
        self.data["Accounts"][account_id]["PermissionSets"] = self.sso_client.list_account_permission_sets(account_id)
        # fmt: on

    def report_accounts_created(self, delta=7):
        """Generate report of accounts created within a timeframe.

        Args:
            delta (int, optional): Number of days from today to include in report. Defaults to 7.

        Returns:
            list: List of account objects that joined within the timeframe.
        """
        account_report = []
        # fmt: off
        timeframe = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(days=delta )
        # fmt: on
        for account in self.data["Accounts"]:
            joined_timestamp = account["JoinedTimestamp"]
            if joined_timestamp > timeframe:
                account_report.append(account)

        return account_report
