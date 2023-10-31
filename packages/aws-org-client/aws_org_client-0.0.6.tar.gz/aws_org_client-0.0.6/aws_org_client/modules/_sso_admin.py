import boto3
from aws_org_client.modules._logger import Logger


logger = Logger(__name__)


class _SSOAdmin:
    def __init__(self, instance_arn):
        logger.info("Init sso-admin client...")
        self.sso_admin_client = boto3.client("sso-admin")
        self.instance_arn = instance_arn

    #   self.permission_sets = self.get_permission_set_details()

    # def get_permission_set_details(self):
    #   permission_set_data = []
    #   permission_set_list = self.list_permission_sets()
    #   for permission_set_arn in permission_set_list:
    #     print(permission_set_arn)
    #     permission_set_detail = self.describe_permission_set(permission_set_arn)
    #     permission_set_name = permission_set_detail['Name']

    #     permission_set = {
    #       "PermissionSetName": permission_set_name,
    #       "PermissionSetArn": permission_set_arn
    #     }
    #     permission_set_list.append(permission_set)

    #   return permission_set_data

    def list_permission_sets(self):
        logger.info("Listing permission sets...")
        permission_sets = []
        next_token = None

        # [TODO: use paginator]
        while True:
            if next_token:
                response = self.sso_admin_client.list_permission_sets(
                    InstanceArn=self.instance_arn, NextToken=next_token
                )
            else:
                response = self.sso_admin_client.list_permission_sets(
                    InstanceArn=self.instance_arn
                )

            permission_sets.extend(response.get("PermissionSets", []))
            next_token = response.get("NextToken")

            if not next_token:
                break

        return permission_sets

    def list_account_permission_sets(self, account_id):
        logger.info(f"Listing permission sets provisioned to {account_id}...")
        response = self.sso_admin_client.list_permission_sets_provisioned_to_account(
            InstanceArn=self.instance_arn, AccountId=account_id
        )

        return response.get("PermissionSets", [])

    def list_account_assignments(self, account_id, permission_set_arn):
        logger.info(f"Listing {account_id} assignee...")
        response = self.sso_admin_client.list_account_assignments(
            InstanceArn=self.instance_arn,
            AccountId=account_id,
            PermissionSetArn=permission_set_arn,
        )

        return response.get("AccountAssignments", [])

    def describe_permission_set(self, permission_set_arn):
        logger.info(f"Describing permission set {permission_set_arn}...")
        response = self.sso_admin_client.describe_permission_set(
            InstanceArn=self.instance_arn, PermissionSetArn=permission_set_arn
        )

        return response.get("PermissionSet")
