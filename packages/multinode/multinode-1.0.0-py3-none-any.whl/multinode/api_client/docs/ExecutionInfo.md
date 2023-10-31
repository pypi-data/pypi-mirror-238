# ExecutionInfo


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_name** | **str** |  | 
**version_id** | **str** |  | 
**function_name** | **str** |  | 
**invocation_id** | **str** |  | 
**execution_id** | **str** |  | 
**input** | **str** |  | 
**cancellation_request_time** | **int** |  | 
**resource_spec** | [**ResourceSpec**](ResourceSpec.md) |  | 
**execution_spec** | [**ExecutionSpec**](ExecutionSpec.md) |  | 
**function_status** | [**FunctionStatus**](FunctionStatus.md) |  | 
**prepared_function_details** | [**PreparedFunctionDetails**](PreparedFunctionDetails.md) |  | 
**worker_status** | [**WorkerStatus**](WorkerStatus.md) |  | 
**worker_details** | [**WorkerDetails**](WorkerDetails.md) |  | 
**termination_signal_time** | **int** |  | 
**outcome** | [**ExecutionOutcome**](ExecutionOutcome.md) |  | 
**output** | **str** |  | 
**error_message** | **str** |  | 
**creation_time** | **int** |  | 
**last_update_time** | **int** |  | 
**execution_start_time** | **int** |  | 
**execution_finish_time** | **int** |  | 
**invocation_creation_time** | **int** |  | 

## Example

```python
from multinode.api_client.models.execution_info import ExecutionInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionInfo from a JSON string
execution_info_instance = ExecutionInfo.from_json(json)
# print the JSON string representation of the object
print ExecutionInfo.to_json()

# convert the object into a dict
execution_info_dict = execution_info_instance.to_dict()
# create an instance of ExecutionInfo from a dict
execution_info_form_dict = execution_info.from_dict(execution_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


