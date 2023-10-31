# InvocationInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_name** | **str** |  | 
**version_id** | **str** |  | 
**function_name** | **str** |  | 
**invocation_id** | **str** |  | 
**parent_invocation** | [**ParentInvocationInfo**](ParentInvocationInfo.md) |  | 
**resource_spec** | [**ResourceSpec**](ResourceSpec.md) |  | 
**execution_spec** | [**ExecutionSpec**](ExecutionSpec.md) |  | 
**function_status** | [**FunctionStatus**](FunctionStatus.md) |  | 
**prepared_function_details** | [**PreparedFunctionDetails**](PreparedFunctionDetails.md) |  | 
**input** | **str** |  | 
**cancellation_request_time** | **int** |  | 
**invocation_status** | [**InvocationStatus**](InvocationStatus.md) |  | 
**creation_time** | **int** |  | 
**last_update_time** | **int** |  | 
**executions** | [**List[ExecutionSummary]**](ExecutionSummary.md) |  | 

## Example

```python
from multinode.api_client.models.invocation_info import InvocationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of InvocationInfo from a JSON string
invocation_info_instance = InvocationInfo.from_json(json)
# print the JSON string representation of the object
print InvocationInfo.to_json()

# convert the object into a dict
invocation_info_dict = invocation_info_instance.to_dict()
# create an instance of InvocationInfo from a dict
invocation_info_form_dict = invocation_info.from_dict(invocation_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


