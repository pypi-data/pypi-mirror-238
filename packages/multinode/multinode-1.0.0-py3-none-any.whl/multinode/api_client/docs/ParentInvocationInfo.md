# ParentInvocationInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function_name** | **str** |  | 
**invocation_id** | **str** |  | 
**cancellation_request_time** | **int** |  | 
**invocation_status** | [**InvocationStatus**](InvocationStatus.md) |  | 
**creation_time** | **int** |  | 
**last_update_time** | **int** |  | 

## Example

```python
from multinode.api_client.models.parent_invocation_info import ParentInvocationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ParentInvocationInfo from a JSON string
parent_invocation_info_instance = ParentInvocationInfo.from_json(json)
# print the JSON string representation of the object
print ParentInvocationInfo.to_json()

# convert the object into a dict
parent_invocation_info_dict = parent_invocation_info_instance.to_dict()
# create an instance of ParentInvocationInfo from a dict
parent_invocation_info_form_dict = parent_invocation_info.from_dict(parent_invocation_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


