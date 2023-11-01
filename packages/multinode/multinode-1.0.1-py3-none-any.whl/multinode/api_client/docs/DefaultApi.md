# multinode.api_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_invocation**](DefaultApi.md#cancel_invocation) | **PUT** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations/{invocation_id}/cancel | Cancel Invocation
[**create_invocation**](DefaultApi.md#create_invocation) | **POST** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations | Create Invocation
[**create_project**](DefaultApi.md#create_project) | **PUT** /projects/{project_name} | Create Project
[**create_project_version**](DefaultApi.md#create_project_version) | **POST** /projects/{project_name}/versions | Create Project Version
[**delete_project**](DefaultApi.md#delete_project) | **DELETE** /projects/{project_name} | Delete Project
[**finish_execution**](DefaultApi.md#finish_execution) | **PUT** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations/{invocation_id}/executions/{execution_id}/finish | Finish Execution
[**get_container_repository_credentials**](DefaultApi.md#get_container_repository_credentials) | **GET** /container_repository_credentials | Get Container Repository Credentials
[**get_execution**](DefaultApi.md#get_execution) | **GET** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations/{invocation_id}/executions/{execution_id} | Get Execution
[**get_execution_logs**](DefaultApi.md#get_execution_logs) | **GET** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations/{invocation_id}/executions/{execution_id}/logs | Get Execution Logs
[**get_invocation**](DefaultApi.md#get_invocation) | **GET** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations/{invocation_id} | Get Invocation
[**get_project**](DefaultApi.md#get_project) | **GET** /projects/{project_name} | Get Project
[**get_project_version**](DefaultApi.md#get_project_version) | **GET** /projects/{project_name}/versions/{version_ref_str} | Get Project Version
[**health_check**](DefaultApi.md#health_check) | **GET** / | Health Check
[**list_invocations**](DefaultApi.md#list_invocations) | **GET** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations | List Invocations
[**list_project_versions**](DefaultApi.md#list_project_versions) | **GET** /projects/{project_name}/versions | List Project Versions
[**list_projects**](DefaultApi.md#list_projects) | **GET** /projects | List Projects
[**start_execution**](DefaultApi.md#start_execution) | **PUT** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations/{invocation_id}/executions/{execution_id}/start | Start Execution
[**update_execution**](DefaultApi.md#update_execution) | **PUT** /projects/{project_name}/versions/{version_ref_str}/functions/{function_name}/invocations/{invocation_id}/executions/{execution_id}/update | Update Execution


# **cancel_invocation**
> InvocationInfo cancel_invocation(project_name, version_ref_str, function_name, invocation_id)

Cancel Invocation

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.invocation_info import InvocationInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_id = 'invocation_id_example' # str | 

    try:
        # Cancel Invocation
        api_response = api_instance.cancel_invocation(project_name, version_ref_str, function_name, invocation_id)
        print("The response of DefaultApi->cancel_invocation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->cancel_invocation: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_id** | **str**|  | 

### Return type

[**InvocationInfo**](InvocationInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version; An invocation with this ID does not exist for this function |  -  |
**409** | This invocation has already terminated |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_invocation**
> InvocationInfo create_invocation(project_name, version_ref_str, function_name, invocation_definition)

Create Invocation

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.invocation_definition import InvocationDefinition
from multinode.api_client.models.invocation_info import InvocationInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_definition = multinode.api_client.InvocationDefinition() # InvocationDefinition | 

    try:
        # Create Invocation
        api_response = api_instance.create_invocation(project_name, version_ref_str, function_name, invocation_definition)
        print("The response of DefaultApi->create_invocation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_invocation: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_definition** | [**InvocationDefinition**](InvocationDefinition.md)|  | 

### Return type

[**InvocationInfo**](InvocationInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version |  -  |
**400** | The ID of the parent invocation is invalid |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_project**
> ProjectInfo create_project(project_name)

Create Project

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.project_info import ProjectInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 

    try:
        # Create Project
        api_response = api_instance.create_project(project_name)
        print("The response of DefaultApi->create_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_project: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 

### Return type

[**ProjectInfo**](ProjectInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**409** | A project with this name already exists. |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_project_version**
> VersionInfo create_project_version(project_name, version_definition)

Create Project Version

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.version_definition import VersionDefinition
from multinode.api_client.models.version_info import VersionInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_definition = multinode.api_client.VersionDefinition() # VersionDefinition | 

    try:
        # Create Project Version
        api_response = api_instance.create_project_version(project_name, version_definition)
        print("The response of DefaultApi->create_project_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->create_project_version: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_definition** | [**VersionDefinition**](VersionDefinition.md)|  | 

### Return type

[**VersionInfo**](VersionInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist |  -  |
**400** | The project is being deleted |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_project**
> ProjectInfo delete_project(project_name)

Delete Project

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.project_info import ProjectInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 

    try:
        # Delete Project
        api_response = api_instance.delete_project(project_name)
        print("The response of DefaultApi->delete_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->delete_project: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 

### Return type

[**ProjectInfo**](ProjectInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finish_execution**
> ExecutionInfo finish_execution(project_name, version_ref_str, function_name, invocation_id, execution_id, execution_final_result_payload)

Finish Execution

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.execution_final_result_payload import ExecutionFinalResultPayload
from multinode.api_client.models.execution_info import ExecutionInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_id = 'invocation_id_example' # str | 
    execution_id = 'execution_id_example' # str | 
    execution_final_result_payload = multinode.api_client.ExecutionFinalResultPayload() # ExecutionFinalResultPayload | 

    try:
        # Finish Execution
        api_response = api_instance.finish_execution(project_name, version_ref_str, function_name, invocation_id, execution_id, execution_final_result_payload)
        print("The response of DefaultApi->finish_execution:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->finish_execution: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_id** | **str**|  | 
 **execution_id** | **str**|  | 
 **execution_final_result_payload** | [**ExecutionFinalResultPayload**](ExecutionFinalResultPayload.md)|  | 

### Return type

[**ExecutionInfo**](ExecutionInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version; An invocation with this ID does not exist for this function; An execution with this ID does not exist for this invocation |  -  |
**409** | This execution has not yet started; This execution has already finished; This execution has already terminated |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_container_repository_credentials**
> ContainerRepositoryCredentials get_container_repository_credentials()

Get Container Repository Credentials

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.container_repository_credentials import ContainerRepositoryCredentials
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)

    try:
        # Get Container Repository Credentials
        api_response = api_instance.get_container_repository_credentials()
        print("The response of DefaultApi->get_container_repository_credentials:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_container_repository_credentials: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**ContainerRepositoryCredentials**](ContainerRepositoryCredentials.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_execution**
> ExecutionInfo get_execution(project_name, version_ref_str, function_name, invocation_id, execution_id)

Get Execution

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.execution_info import ExecutionInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_id = 'invocation_id_example' # str | 
    execution_id = 'execution_id_example' # str | 

    try:
        # Get Execution
        api_response = api_instance.get_execution(project_name, version_ref_str, function_name, invocation_id, execution_id)
        print("The response of DefaultApi->get_execution:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_execution: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_id** | **str**|  | 
 **execution_id** | **str**|  | 

### Return type

[**ExecutionInfo**](ExecutionInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version; An invocation with this ID does not exist for this function; An execution with this ID does not exist for this invocation |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_execution_logs**
> ExecutionLogs get_execution_logs(project_name, version_ref_str, function_name, invocation_id, execution_id, max_lines=max_lines, initial_offset=initial_offset)

Get Execution Logs

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.execution_logs import ExecutionLogs
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_id = 'invocation_id_example' # str | 
    execution_id = 'execution_id_example' # str | 
    max_lines = 56 # int |  (optional)
    initial_offset = 'initial_offset_example' # str |  (optional)

    try:
        # Get Execution Logs
        api_response = api_instance.get_execution_logs(project_name, version_ref_str, function_name, invocation_id, execution_id, max_lines=max_lines, initial_offset=initial_offset)
        print("The response of DefaultApi->get_execution_logs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_execution_logs: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_id** | **str**|  | 
 **execution_id** | **str**|  | 
 **max_lines** | **int**|  | [optional] 
 **initial_offset** | **str**|  | [optional] 

### Return type

[**ExecutionLogs**](ExecutionLogs.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version; An invocation with this ID does not exist for this function; An execution with this ID does not exist for this invocation |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_invocation**
> InvocationInfo get_invocation(project_name, version_ref_str, function_name, invocation_id)

Get Invocation

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.invocation_info import InvocationInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_id = 'invocation_id_example' # str | 

    try:
        # Get Invocation
        api_response = api_instance.get_invocation(project_name, version_ref_str, function_name, invocation_id)
        print("The response of DefaultApi->get_invocation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_invocation: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_id** | **str**|  | 

### Return type

[**InvocationInfo**](InvocationInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version; An invocation with this ID does not exist for this function |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project**
> ProjectInfo get_project(project_name)

Get Project

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.project_info import ProjectInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 

    try:
        # Get Project
        api_response = api_instance.get_project(project_name)
        print("The response of DefaultApi->get_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_project: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 

### Return type

[**ProjectInfo**](ProjectInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project_version**
> VersionInfo get_project_version(project_name, version_ref_str)

Get Project Version

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.version_info import VersionInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 

    try:
        # Get Project Version
        api_response = api_instance.get_project_version(project_name, version_ref_str)
        print("The response of DefaultApi->get_project_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_project_version: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 

### Return type

[**VersionInfo**](VersionInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health_check**
> HealthStatus health_check()

Health Check

### Example

```python
import time
import os
import multinode.api_client
from multinode.api_client.models.health_status import HealthStatus
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)

    try:
        # Health Check
        api_response = api_instance.health_check()
        print("The response of DefaultApi->health_check:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->health_check: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**HealthStatus**](HealthStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_invocations**
> InvocationsListForFunction list_invocations(project_name, version_ref_str, function_name, max_results=max_results, initial_offset=initial_offset, status=status, parent_function_name=parent_function_name, parent_invocation_id=parent_invocation_id)

List Invocations

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.invocation_status import InvocationStatus
from multinode.api_client.models.invocations_list_for_function import InvocationsListForFunction
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    max_results = 56 # int |  (optional)
    initial_offset = 'initial_offset_example' # str |  (optional)
    status = multinode.api_client.InvocationStatus() # InvocationStatus |  (optional)
    parent_function_name = 'parent_function_name_example' # str |  (optional)
    parent_invocation_id = 'parent_invocation_id_example' # str |  (optional)

    try:
        # List Invocations
        api_response = api_instance.list_invocations(project_name, version_ref_str, function_name, max_results=max_results, initial_offset=initial_offset, status=status, parent_function_name=parent_function_name, parent_invocation_id=parent_invocation_id)
        print("The response of DefaultApi->list_invocations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_invocations: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **max_results** | **int**|  | [optional] 
 **initial_offset** | **str**|  | [optional] 
 **status** | [**InvocationStatus**](.md)|  | [optional] 
 **parent_function_name** | **str**|  | [optional] 
 **parent_invocation_id** | **str**|  | [optional] 

### Return type

[**InvocationsListForFunction**](InvocationsListForFunction.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version |  -  |
**400** | The next offset is in an invalid format; The parent function name is missing; The parent invocation ID is missing |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_project_versions**
> VersionsListForProject list_project_versions(project_name)

List Project Versions

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.versions_list_for_project import VersionsListForProject
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 

    try:
        # List Project Versions
        api_response = api_instance.list_project_versions(project_name)
        print("The response of DefaultApi->list_project_versions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_project_versions: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 

### Return type

[**VersionsListForProject**](VersionsListForProject.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_projects**
> ProjectsList list_projects()

List Projects

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.projects_list import ProjectsList
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)

    try:
        # List Projects
        api_response = api_instance.list_projects()
        print("The response of DefaultApi->list_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->list_projects: %s\n" % e)
```



### Parameters
This endpoint does not need any parameter.

### Return type

[**ProjectsList**](ProjectsList.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**403** | The API key is invalid |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_execution**
> ExecutionInfo start_execution(project_name, version_ref_str, function_name, invocation_id, execution_id)

Start Execution

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.execution_info import ExecutionInfo
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_id = 'invocation_id_example' # str | 
    execution_id = 'execution_id_example' # str | 

    try:
        # Start Execution
        api_response = api_instance.start_execution(project_name, version_ref_str, function_name, invocation_id, execution_id)
        print("The response of DefaultApi->start_execution:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->start_execution: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_id** | **str**|  | 
 **execution_id** | **str**|  | 

### Return type

[**ExecutionInfo**](ExecutionInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version; An invocation with this ID does not exist for this function; An execution with this ID does not exist for this invocation |  -  |
**409** | This execution has already started; This execution has already terminated |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_execution**
> ExecutionInfo update_execution(project_name, version_ref_str, function_name, invocation_id, execution_id, execution_temporary_result_payload)

Update Execution

### Example

* Bearer Authentication (HTTPBearer):
```python
import time
import os
import multinode.api_client
from multinode.api_client.models.execution_info import ExecutionInfo
from multinode.api_client.models.execution_temporary_result_payload import ExecutionTemporaryResultPayload
from multinode.api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = multinode.api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = multinode.api_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with multinode.api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = multinode.api_client.DefaultApi(api_client)
    project_name = 'project_name_example' # str | 
    version_ref_str = 'version_ref_str_example' # str | 
    function_name = 'function_name_example' # str | 
    invocation_id = 'invocation_id_example' # str | 
    execution_id = 'execution_id_example' # str | 
    execution_temporary_result_payload = multinode.api_client.ExecutionTemporaryResultPayload() # ExecutionTemporaryResultPayload | 

    try:
        # Update Execution
        api_response = api_instance.update_execution(project_name, version_ref_str, function_name, invocation_id, execution_id, execution_temporary_result_payload)
        print("The response of DefaultApi->update_execution:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->update_execution: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_name** | **str**|  | 
 **version_ref_str** | **str**|  | 
 **function_name** | **str**|  | 
 **invocation_id** | **str**|  | 
 **execution_id** | **str**|  | 
 **execution_temporary_result_payload** | [**ExecutionTemporaryResultPayload**](ExecutionTemporaryResultPayload.md)|  | 

### Return type

[**ExecutionInfo**](ExecutionInfo.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | A project with this name does not exist; A version with this ID does not exist for this project; A function with this name does not exist for this project version; An invocation with this ID does not exist for this function; An execution with this ID does not exist for this invocation |  -  |
**409** | This execution has not yet started; This execution has already finished; This execution has already terminated |  -  |
**403** | The API key is invalid |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

