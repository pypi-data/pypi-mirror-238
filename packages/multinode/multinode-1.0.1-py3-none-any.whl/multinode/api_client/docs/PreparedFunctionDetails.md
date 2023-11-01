# PreparedFunctionDetails


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**WorkerType**](WorkerType.md) |  | 
**identifier** | **str** |  | 

## Example

```python
from multinode.api_client.models.prepared_function_details import PreparedFunctionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PreparedFunctionDetails from a JSON string
prepared_function_details_instance = PreparedFunctionDetails.from_json(json)
# print the JSON string representation of the object
print PreparedFunctionDetails.to_json()

# convert the object into a dict
prepared_function_details_dict = prepared_function_details_instance.to_dict()
# create an instance of PreparedFunctionDetails from a dict
prepared_function_details_form_dict = prepared_function_details.from_dict(prepared_function_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


