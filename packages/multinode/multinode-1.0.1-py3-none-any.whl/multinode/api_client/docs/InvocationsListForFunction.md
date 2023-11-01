# InvocationsListForFunction


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_name** | **str** |  | 
**version_id** | **str** |  | 
**function_name** | **str** |  | 
**invocations** | [**List[InvocationInfoForFunction]**](InvocationInfoForFunction.md) |  | 
**next_offset** | **str** |  | 

## Example

```python
from multinode.api_client.models.invocations_list_for_function import InvocationsListForFunction

# TODO update the JSON string below
json = "{}"
# create an instance of InvocationsListForFunction from a JSON string
invocations_list_for_function_instance = InvocationsListForFunction.from_json(json)
# print the JSON string representation of the object
print InvocationsListForFunction.to_json()

# convert the object into a dict
invocations_list_for_function_dict = invocations_list_for_function_instance.to_dict()
# create an instance of InvocationsListForFunction from a dict
invocations_list_for_function_form_dict = invocations_list_for_function.from_dict(invocations_list_for_function_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


