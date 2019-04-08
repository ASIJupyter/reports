import azure
import azure.mgmt.storage.models
from azure.mgmt.compute.models import DiskCreateOption
from azure.common.credentials import ServicePrincipalCredentials
from azure.common.credentials import UserPassCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient

from azure.storage.blob import BlockBlobService, PageBlobService, AppendBlobService
from azure.storage.blob.models import BlobBlock, ContainerPermissions, ContentSettings

class ResourceHelper:
    def __init__(self, resource_client, resource_group):
        self.resource_client = resource_client
        self.resource_group = resource_group

    def create_resource_group(self, resource_group_location):
        resource_group_params = { 'location': resource_group_location }
        create_resource_group_async = self.resource_client.resource_groups.create_or_update(
            self.resource_group, 
            resource_group_params
        )

# end of the class
