# WorkerDetails


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**WorkerType**](WorkerType.md) |  | 
**identifier** | **str** |  | 
**logs_identifier** | **str** |  | 

## Example

```python
from multinode.api_client.models.worker_details import WorkerDetails

# TODO update the JSON string below
json = "{}"
# create an instance of WorkerDetails from a JSON string
worker_details_instance = WorkerDetails.from_json(json)
# print the JSON string representation of the object
print WorkerDetails.to_json()

# convert the object into a dict
worker_details_dict = worker_details_instance.to_dict()
# create an instance of WorkerDetails from a dict
worker_details_form_dict = worker_details.from_dict(worker_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


