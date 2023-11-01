# VersionDefinition


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_docker_image** | **str** |  | 
**functions** | [**List[FunctionSpec]**](FunctionSpec.md) |  | 

## Example

```python
from multinode.api_client.models.version_definition import VersionDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of VersionDefinition from a JSON string
version_definition_instance = VersionDefinition.from_json(json)
# print the JSON string representation of the object
print VersionDefinition.to_json()

# convert the object into a dict
version_definition_dict = version_definition_instance.to_dict()
# create an instance of VersionDefinition from a dict
version_definition_form_dict = version_definition.from_dict(version_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


