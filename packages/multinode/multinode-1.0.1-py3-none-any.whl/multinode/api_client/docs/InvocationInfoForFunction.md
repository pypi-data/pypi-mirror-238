# InvocationInfoForFunction


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invocation_id** | **str** |  | 
**parent_invocation** | [**ParentInvocationDefinition**](ParentInvocationDefinition.md) |  | 
**cancellation_request_time** | **int** |  | 
**invocation_status** | [**InvocationStatus**](InvocationStatus.md) |  | 
**creation_time** | **int** |  | 
**last_update_time** | **int** |  | 

## Example

```python
from multinode.api_client.models.invocation_info_for_function import InvocationInfoForFunction

# TODO update the JSON string below
json = "{}"
# create an instance of InvocationInfoForFunction from a JSON string
invocation_info_for_function_instance = InvocationInfoForFunction.from_json(json)
# print the JSON string representation of the object
print InvocationInfoForFunction.to_json()

# convert the object into a dict
invocation_info_for_function_dict = invocation_info_for_function_instance.to_dict()
# create an instance of InvocationInfoForFunction from a dict
invocation_info_for_function_form_dict = invocation_info_for_function.from_dict(invocation_info_for_function_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


