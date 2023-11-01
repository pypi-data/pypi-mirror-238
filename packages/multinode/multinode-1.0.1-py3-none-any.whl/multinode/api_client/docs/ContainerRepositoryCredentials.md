# ContainerRepositoryCredentials


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repository_name** | **str** |  | 
**username** | **str** |  | 
**password** | **str** |  | 
**endpoint_url** | **str** |  | 

## Example

```python
from multinode.api_client.models.container_repository_credentials import ContainerRepositoryCredentials

# TODO update the JSON string below
json = "{}"
# create an instance of ContainerRepositoryCredentials from a JSON string
container_repository_credentials_instance = ContainerRepositoryCredentials.from_json(json)
# print the JSON string representation of the object
print ContainerRepositoryCredentials.to_json()

# convert the object into a dict
container_repository_credentials_dict = container_repository_credentials_instance.to_dict()
# create an instance of ContainerRepositoryCredentials from a dict
container_repository_credentials_form_dict = container_repository_credentials.from_dict(container_repository_credentials_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


