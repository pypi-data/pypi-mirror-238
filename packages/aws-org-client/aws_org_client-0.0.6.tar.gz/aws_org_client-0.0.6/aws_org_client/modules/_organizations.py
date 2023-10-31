import boto3
from aws_org_client.modules._logger import Logger


logger = Logger(__name__)


class _Organizations:
    def __init__(self):
        logger.info("Init organizations client...")
        self.org_client = boto3.client("organizations")

    def list_accounts(self):
        logger.info("Listing accounts...")
        accounts = []
        next_token = None

        # [TODO: use paginator]
        while True:
            if next_token:
                response = self.org_client.list_accounts(NextToken=next_token)
            else:
                response = self.org_client.list_accounts()

            accounts.extend(response.get("Accounts", []))
            next_token = response.get("NextToken")

            if not next_token:
                break

        return accounts
