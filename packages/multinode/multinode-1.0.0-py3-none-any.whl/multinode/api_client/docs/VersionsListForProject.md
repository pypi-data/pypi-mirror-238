# VersionsListForProject


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_name** | **str** |  | 
**versions** | [**List[VersionInfoForProject]**](VersionInfoForProject.md) |  | 

## Example

```python
from multinode.api_client.models.versions_list_for_project import VersionsListForProject

# TODO update the JSON string below
json = "{}"
# create an instance of VersionsListForProject from a JSON string
versions_list_for_project_instance = VersionsListForProject.from_json(json)
# print the JSON string representation of the object
print VersionsListForProject.to_json()

# convert the object into a dict
versions_list_for_project_dict = versions_list_for_project_instance.to_dict()
# create an instance of VersionsListForProject from a dict
versions_list_for_project_form_dict = versions_list_for_project.from_dict(versions_list_for_project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


