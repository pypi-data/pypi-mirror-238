# ProjectsList


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projects** | [**List[ProjectInfo]**](ProjectInfo.md) |  | 

## Example

```python
from multinode.api_client.models.projects_list import ProjectsList

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectsList from a JSON string
projects_list_instance = ProjectsList.from_json(json)
# print the JSON string representation of the object
print ProjectsList.to_json()

# convert the object into a dict
projects_list_dict = projects_list_instance.to_dict()
# create an instance of ProjectsList from a dict
projects_list_form_dict = projects_list.from_dict(projects_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


