# ExecutionFinalResultPayload


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**outcome** | [**ExecutionOutcome**](ExecutionOutcome.md) |  | 
**final_output** | **str** |  | [optional] 
**error_message** | **str** |  | [optional] 

## Example

```python
from multinode.api_client.models.execution_final_result_payload import ExecutionFinalResultPayload

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionFinalResultPayload from a JSON string
execution_final_result_payload_instance = ExecutionFinalResultPayload.from_json(json)
# print the JSON string representation of the object
print ExecutionFinalResultPayload.to_json()

# convert the object into a dict
execution_final_result_payload_dict = execution_final_result_payload_instance.to_dict()
# create an instance of ExecutionFinalResultPayload from a dict
execution_final_result_payload_form_dict = execution_final_result_payload.from_dict(execution_final_result_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


