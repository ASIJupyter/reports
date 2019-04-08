import azure
import azure.cli
import azure.mgmt.storage.models
from azure.mgmt.compute.models import DiskCreateOption
from azure.common.credentials import ServicePrincipalCredentials
from azure.common.credentials import UserPassCredentials
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient

class AADHelper:
    def authenticate(self, auth_method, **kwargs):
        creds = self.get_credentials(auth_method, **kwargs)
        return self.initialize_azure_clients(kwargs['subscription_id'], creds)

    def get_credentials(self, auth_method, **kwargs):
        if auth_method == 'Service Principal':
            credentials = ServicePrincipalCredentials(client_id=kwargs['client_id'], secret=kwargs['secret'], tenant=kwargs['tenant_id'])
        elif auth_method == 'User ID Password':
            credentials = UserPassCredentials(username=kwargs['user_id'], password=kwargs['password'])
        else:
            credentials = None

        return credentials
        
    def initialize_azure_clients(self, subscription_id, credentials):
        if credentials is not None:
            resource_client = ResourceManagementClient(credentials, subscription_id)
            compute_client = ComputeManagementClient(credentials, subscription_id)
            network_client = NetworkManagementClient(credentials, subscription_id)
            storage_client = StorageManagementClient(credentials, subscription_id)
        else:
            resource_client = get_client_from_cli_profile(ResourceManagementClient, subscription_id = subscription_id)
            compute_client = get_client_from_cli_profile(ComputeManagementClient, subscription_id = subscription_id)
            network_client = get_client_from_cli_profile(NetworkManagementClient, subscription_id = subscription_id)
            storage_client = get_client_from_cli_profile(StorageManagementClient, subscription_id = subscription_id)

        return compute_client, network_client, resource_client, storage_client

# end of the class
