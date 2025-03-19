# Azure Container Instance Deployment

This script automates the deployment of an Nginx container on Microsoft Azure using Azure Container Instances (ACI). It creates a new resource group, configures container specifications, and deploys the container with public access.

## Prerequisites

Before running the script, ensure you have the following:

- An active Azure subscription
- Python 3.x installed
- Azure CLI installed and authenticated (`az login`)
- Required Python packages installed:
  ```sh
  pip install azure-identity azure-mgmt-resource azure-mgmt-containerinstance
  ```

## How the Script Works

1. **Authenticate with Azure**:

   - Uses `DefaultAzureCredential()` to authenticate.
   - Requires an Azure CLI login or managed identity.

2. **Define Configuration Parameters**:

   - Generates unique names for the resource group and container group.
   - Sets the Azure region (`eastus`), container image (`nginx`), and port (`80`).

3. **Create a Resource Group**:

   - Calls `resource_groups.create_or_update()` to provision a new resource group in the specified location.

4. **Define and Configure the Container**:

   - Allocates CPU and memory resources.
   - Sets container image and network ports.
   - Configures an optional image registry credential.

5. **Create and Deploy the Container Group**:

   - Assigns a public IP with a DNS label.
   - Deploys the container using `container_groups.begin_create_or_update()`.

6. **Output Deployment Details**:
   - Prints the accessible URL for the deployed Nginx container.

## Running the Script

Execute the script using:

```sh
python deploy-nginx-container
```

After successful execution, you will see an output similar to:

```
Deployment successful! You can access Nginx at: http://container-group-<uuid>.eastus.azurecontainer.io
```

## Security Considerations

- Avoid hardcoding credentials in the script. Instead, use Azure Key Vault or environment variables.
- Ensure the resource group and container instances are properly cleaned up after testing.
- Use managed identities for authentication instead of storing credentials in the script.

## Cleanup

To remove the created resources, run:

```sh
az group delete --name <resource-group-name> --yes --no-wait
```

This script provides an automated way to deploy and manage container instances on Azure efficiently. Modify it as needed to fit your use case.
