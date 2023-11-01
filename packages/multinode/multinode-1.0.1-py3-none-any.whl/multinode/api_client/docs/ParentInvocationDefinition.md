# ParentInvocationDefinition


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function_name** | **str** |  | 
**invocation_id** | **str** |  | 

## Example

```python
from multinode.api_client.models.parent_invocation_definition import ParentInvocationDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of ParentInvocationDefinition from a JSON string
parent_invocation_definition_instance = ParentInvocationDefinition.from_json(json)
# print the JSON string representation of the object
print ParentInvocationDefinition.to_json()

# convert the object into a dict
parent_invocation_definition_dict = parent_invocation_definition_instance.to_dict()
# create an instance of ParentInvocationDefinition from a dict
parent_invocation_definition_form_dict = parent_invocation_definition.from_dict(parent_invocation_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


