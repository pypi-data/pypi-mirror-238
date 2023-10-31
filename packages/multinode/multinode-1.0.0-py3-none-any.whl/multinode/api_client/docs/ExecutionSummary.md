# ExecutionSummary


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**execution_id** | **str** |  | 
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

## Example

```python
from multinode.api_client.models.execution_summary import ExecutionSummary

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionSummary from a JSON string
execution_summary_instance = ExecutionSummary.from_json(json)
# print the JSON string representation of the object
print ExecutionSummary.to_json()

# convert the object into a dict
execution_summary_dict = execution_summary_instance.to_dict()
# create an instance of ExecutionSummary from a dict
execution_summary_form_dict = execution_summary.from_dict(execution_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


