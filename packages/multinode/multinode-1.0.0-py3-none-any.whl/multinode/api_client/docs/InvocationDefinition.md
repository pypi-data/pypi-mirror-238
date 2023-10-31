# InvocationDefinition


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parent_invocation** | [**ParentInvocationDefinition**](ParentInvocationDefinition.md) |  | [optional] 
**input** | **str** |  | 

## Example

```python
from multinode.api_client.models.invocation_definition import InvocationDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of InvocationDefinition from a JSON string
invocation_definition_instance = InvocationDefinition.from_json(json)
# print the JSON string representation of the object
print InvocationDefinition.to_json()

# convert the object into a dict
invocation_definition_dict = invocation_definition_instance.to_dict()
# create an instance of InvocationDefinition from a dict
invocation_definition_form_dict = invocation_definition.from_dict(invocation_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


