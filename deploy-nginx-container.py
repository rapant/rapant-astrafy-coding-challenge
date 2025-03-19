import uuid
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import ImageRegistryCredential
from azure.mgmt.containerinstance.models import (
    ContainerGroup, Container, ContainerPort, Port, ResourceRequests,
    ResourceRequirements, IpAddress, ContainerGroupNetworkProtocol, OperatingSystemTypes
)

# Replace with your Azure subscription ID
SUBSCRIPTION_ID = "86f92126-bcde-4b48-bea8-afe3d8856f1c"
RESOURCE_GROUP = "rg-" + str(uuid.uuid4())
CONTAINER_GROUP_NAME = "container-group-" + str(uuid.uuid4())
LOCATION = "eastus"
IMAGE = "nginx"
PORT = 80

# Authenticate using DefaultAzureCredential (requires AZ CLI login or managed identity)
credential = DefaultAzureCredential()

# Create Resource Management Client
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

# Create Resource Group
resource_client.resource_groups.create_or_update(
    RESOURCE_GROUP,
    {"location": LOCATION}
)

# Create Container Instance Management Client
client = ContainerInstanceManagementClient(credential, SUBSCRIPTION_ID)

# Define container resource requirements
resources = ResourceRequirements(requests=ResourceRequests(memory_in_gb=1.5, cpu=1.0))

# Add the credentials to the container group
image_registry_credentials = [
    ImageRegistryCredential(
        username="XXX",
        password="XXX",
        server="index.docker.io"
    )
]

# Define container instance
container = Container(
    name="nginx-container",
    image=IMAGE,
    resources=resources,
    ports=[ContainerPort(port=PORT)]
)

# Define IP address settings for public access
ip_address = IpAddress(
    ports=[Port(protocol=ContainerGroupNetworkProtocol.tcp, port=PORT)],
    type="Public",
    dns_name_label=CONTAINER_GROUP_NAME  # Ensures a public FQDN
)

# Create the container group
container_group = ContainerGroup(
    location=LOCATION,
    containers=[container],
    os_type=OperatingSystemTypes.linux,
    ip_address=ip_address,
    image_registry_credentials=image_registry_credentials
)

# Deploy the container instance
deployment = client.container_groups.begin_create_or_update(
    RESOURCE_GROUP, CONTAINER_GROUP_NAME, container_group
)
deployment.result()

print(f"Deployment successful! You can access Nginx at: http://{CONTAINER_GROUP_NAME}.{LOCATION}.azurecontainer.io")
