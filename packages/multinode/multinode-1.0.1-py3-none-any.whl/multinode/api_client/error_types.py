from multinode.api_client import ApiException
import json


class MultinodeApiException(Exception):
    pass


class ApiKeyIsInvalid(MultinodeApiException):
    pass


class OffsetIsInvalid(MultinodeApiException):
    pass


class ParentFunctionNameIsMissing(MultinodeApiException):
    pass


class ProjectNameIsTooLong(MultinodeApiException):
    pass


class ProjectIsBeingDeleted(MultinodeApiException):
    pass


class ParentInvocationIdIsMissing(MultinodeApiException):
    pass


class ExecutionAlreadyExists(MultinodeApiException):
    pass


class ExecutionDoesNotExist(MultinodeApiException):
    pass


class ExecutionHasAlreadyStarted(MultinodeApiException):
    pass


class ExecutionHasNotStarted(MultinodeApiException):
    pass


class ExecutionHasAlreadyFinished(MultinodeApiException):
    pass


class ExecutionHasNotFinished(MultinodeApiException):
    pass


class ExecutionIsAlreadyTerminated(MultinodeApiException):
    pass


class InvocationAlreadyExists(MultinodeApiException):
    pass


class InvocationDoesNotExist(MultinodeApiException):
    pass


class InvocationIsAlreadyTerminated(MultinodeApiException):
    pass


class ParentInvocationDoesNotExist(MultinodeApiException):
    pass


class FunctionAlreadyExists(MultinodeApiException):
    pass


class FunctionDoesNotExist(MultinodeApiException):
    pass


class VersionAlreadyExists(MultinodeApiException):
    pass


class VersionDoesNotExist(MultinodeApiException):
    pass


class ProjectAlreadyExists(MultinodeApiException):
    pass


class ProjectDoesNotExist(MultinodeApiException):
    pass


def resolve_error(original: ApiException) -> Exception:
    status = original.status
    detail = json.loads(original.body).get('detail')

    if status == 403 and detail == 'The API key is invalid':
        return ApiKeyIsInvalid('The API key is invalid')

    if status == 400 and detail == 'The next offset is in an invalid format':
        return OffsetIsInvalid('The next offset is in an invalid format')

    if status == 400 and detail == 'The parent function name is missing':
        return ParentFunctionNameIsMissing('The parent function name is missing')

    if status == 400 and detail == 'The project name is too long':
        return ProjectNameIsTooLong('The project name is too long')

    if status == 400 and detail == 'The project is being deleted':
        return ProjectIsBeingDeleted('The project is being deleted')

    if status == 400 and detail == 'The parent invocation ID is missing':
        return ParentInvocationIdIsMissing('The parent invocation ID is missing')

    if status == 409 and detail == 'An execution with this ID already exists for this invocation':
        return ExecutionAlreadyExists('An execution with this ID already exists for this invocation')

    if status == 404 and detail == 'An execution with this ID does not exist for this invocation':
        return ExecutionDoesNotExist('An execution with this ID does not exist for this invocation')

    if status == 409 and detail == 'This execution has already started':
        return ExecutionHasAlreadyStarted('This execution has already started')

    if status == 409 and detail == 'This execution has not yet started':
        return ExecutionHasNotStarted('This execution has not yet started')

    if status == 409 and detail == 'This execution has already finished':
        return ExecutionHasAlreadyFinished('This execution has already finished')

    if status == 409 and detail == 'This execution has not yet finished':
        return ExecutionHasNotFinished('This execution has not yet finished')

    if status == 409 and detail == 'This execution has already terminated':
        return ExecutionIsAlreadyTerminated('This execution has already terminated')

    if status == 409 and detail == 'An invocation with this ID already exists for this function':
        return InvocationAlreadyExists('An invocation with this ID already exists for this function')

    if status == 404 and detail == 'An invocation with this ID does not exist for this function':
        return InvocationDoesNotExist('An invocation with this ID does not exist for this function')

    if status == 409 and detail == 'This invocation has already terminated':
        return InvocationIsAlreadyTerminated('This invocation has already terminated')

    if status == 400 and detail == 'The ID of the parent invocation is invalid':
        return ParentInvocationDoesNotExist('The ID of the parent invocation is invalid')

    if status == 409 and detail == 'A function with this name already exists for this project version':
        return FunctionAlreadyExists('A function with this name already exists for this project version')

    if status == 404 and detail == 'A function with this name does not exist for this project version':
        return FunctionDoesNotExist('A function with this name does not exist for this project version')

    if status == 409 and detail == 'A version with this ID already exists for this project':
        return VersionAlreadyExists('A version with this ID already exists for this project')

    if status == 404 and detail == 'A version with this ID does not exist for this project':
        return VersionDoesNotExist('A version with this ID does not exist for this project')

    if status == 409 and detail == 'A project with this name already exists.':
        return ProjectAlreadyExists('A project with this name already exists.')

    if status == 404 and detail == 'A project with this name does not exist':
        return ProjectDoesNotExist('A project with this name does not exist')

    return original
