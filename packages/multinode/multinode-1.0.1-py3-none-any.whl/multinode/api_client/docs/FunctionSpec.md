# FunctionSpec


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function_name** | **str** |  | 
**docker_image_override** | **str** |  | [optional] 
**resource_spec** | [**ResourceSpec**](ResourceSpec.md) |  | 
**execution_spec** | [**ExecutionSpec**](ExecutionSpec.md) |  | 

## Example

```python
from multinode.api_client.models.function_spec import FunctionSpec

# TODO update the JSON string below
json = "{}"
# create an instance of FunctionSpec from a JSON string
function_spec_instance = FunctionSpec.from_json(json)
# print the JSON string representation of the object
print FunctionSpec.to_json()

# convert the object into a dict
function_spec_dict = function_spec_instance.to_dict()
# create an instance of FunctionSpec from a dict
function_spec_form_dict = function_spec.from_dict(function_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


