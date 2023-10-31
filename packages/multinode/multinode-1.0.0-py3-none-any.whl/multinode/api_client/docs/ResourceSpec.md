# ResourceSpec


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**virtual_cpus** | **float** |  | 
**memory_gbs** | **float** |  | 
**max_concurrency** | **int** |  | 

## Example

```python
from multinode.api_client.models.resource_spec import ResourceSpec

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceSpec from a JSON string
resource_spec_instance = ResourceSpec.from_json(json)
# print the JSON string representation of the object
print ResourceSpec.to_json()

# convert the object into a dict
resource_spec_dict = resource_spec_instance.to_dict()
# create an instance of ResourceSpec from a dict
resource_spec_form_dict = resource_spec.from_dict(resource_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


