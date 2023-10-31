# ExecutionTemporaryResultPayload


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**latest_output** | **str** |  | 

## Example

```python
from multinode.api_client.models.execution_temporary_result_payload import ExecutionTemporaryResultPayload

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionTemporaryResultPayload from a JSON string
execution_temporary_result_payload_instance = ExecutionTemporaryResultPayload.from_json(json)
# print the JSON string representation of the object
print ExecutionTemporaryResultPayload.to_json()

# convert the object into a dict
execution_temporary_result_payload_dict = execution_temporary_result_payload_instance.to_dict()
# create an instance of ExecutionTemporaryResultPayload from a dict
execution_temporary_result_payload_form_dict = execution_temporary_result_payload.from_dict(execution_temporary_result_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


