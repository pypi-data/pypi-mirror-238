# FunctionInfoForVersion


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function_name** | **str** |  | 
**docker_image** | **str** |  | 
**resource_spec** | [**ResourceSpec**](ResourceSpec.md) |  | 
**execution_spec** | [**ExecutionSpec**](ExecutionSpec.md) |  | 
**function_status** | [**FunctionStatus**](FunctionStatus.md) |  | 
**prepared_function_details** | [**PreparedFunctionDetails**](PreparedFunctionDetails.md) |  | 

## Example

```python
from multinode.api_client.models.function_info_for_version import FunctionInfoForVersion

# TODO update the JSON string below
json = "{}"
# create an instance of FunctionInfoForVersion from a JSON string
function_info_for_version_instance = FunctionInfoForVersion.from_json(json)
# print the JSON string representation of the object
print FunctionInfoForVersion.to_json()

# convert the object into a dict
function_info_for_version_dict = function_info_for_version_instance.to_dict()
# create an instance of FunctionInfoForVersion from a dict
function_info_for_version_form_dict = function_info_for_version.from_dict(function_info_for_version_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


