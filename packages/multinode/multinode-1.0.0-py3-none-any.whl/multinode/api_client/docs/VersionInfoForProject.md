# VersionInfoForProject


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version_id** | **str** |  | 
**creation_time** | **int** |  | 

## Example

```python
from multinode.api_client.models.version_info_for_project import VersionInfoForProject

# TODO update the JSON string below
json = "{}"
# create an instance of VersionInfoForProject from a JSON string
version_info_for_project_instance = VersionInfoForProject.from_json(json)
# print the JSON string representation of the object
print VersionInfoForProject.to_json()

# convert the object into a dict
version_info_for_project_dict = version_info_for_project_instance.to_dict()
# create an instance of VersionInfoForProject from a dict
version_info_for_project_form_dict = version_info_for_project.from_dict(version_info_for_project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


