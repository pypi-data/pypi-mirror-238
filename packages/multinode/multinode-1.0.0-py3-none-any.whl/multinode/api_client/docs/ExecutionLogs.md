# ExecutionLogs


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_name** | **str** |  | 
**version_id** | **str** |  | 
**function_name** | **str** |  | 
**invocation_id** | **str** |  | 
**execution_id** | **str** |  | 
**log_lines** | **List[str]** |  | 
**next_offset** | **str** |  | 

## Example

```python
from multinode.api_client.models.execution_logs import ExecutionLogs

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionLogs from a JSON string
execution_logs_instance = ExecutionLogs.from_json(json)
# print the JSON string representation of the object
print ExecutionLogs.to_json()

# convert the object into a dict
execution_logs_dict = execution_logs_instance.to_dict()
# create an instance of ExecutionLogs from a dict
execution_logs_form_dict = execution_logs.from_dict(execution_logs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


