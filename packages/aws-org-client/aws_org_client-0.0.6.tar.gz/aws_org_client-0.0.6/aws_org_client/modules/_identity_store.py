import boto3
from aws_org_client.modules._logger import Logger


logger = Logger(__name__)


class _IdentityStore:
    def __init__(self, identity_store_id):
        logger.info("Init idc client...")
        self.client = boto3.client("identitystore")
        self.identity_store_id = identity_store_id

    def list_users(self):
        logger.info("Listing users...")
        response = self.client.list_users(IdentityStoreId=self.identity_store_id)

        return response.get("Users", [])

    def describe_user(self, user_id):
        logger.info(f"Describing user: {user_id}...")
        response = self.client.describe_user(
            IdentityStoreId=self.identity_store_id, UserId=user_id
        )

        return response

    def list_groups(self):
        logger.info("Listing groups...")
        paginator = self.client.get_paginator("list_groups")
        operation_parameters = {"IdentityStoreId": self.identity_store_id}

        page_iterator = paginator.paginate(**operation_parameters)

        groups = [group for page in page_iterator for group in page["Groups"]]

        return groups

    def describe_group(self, group_id):
        logger.info(f"Describing group: {group_id}...")
        response = self.client.describe_group(
            IdentityStoreId=self.identity_store_id, GroupId=group_id
        )

        return response

    def list_group_memberships(self, group_id):
        logger.info(f"Listing group memberships: {group_id}...")
        response = self.client.list_group_memberships(
            IdentityStoreId=self.identity_store_id, GroupId=group_id
        )

        return response.get("GroupMemberships", [])
