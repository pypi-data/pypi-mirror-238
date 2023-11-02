# Interface for services which implement the v1 protocol
from abc import ABC, abstractmethod
from typing import Optional, Any
from typing import TypeVar
from .types import CriteriaTree, Metadata, TaskItemValueMap, StreamMatrixResponse

ParametersType = TypeVar("ParametersType")


class IProtocolV1Service(ABC):

    # Specific version of this service, SemVer-formatted
    version: str

    # Get the criteria tree for the given criteria set ID and combination of parameters
    @abstractmethod
    def get_criteria_tree(
            self,
            criteria_set_id: str,
            parameters: ParametersType,
            values: Optional[TaskItemValueMap] = None,
            locale: Optional[str] = None
    ) -> CriteriaTree:
        pass

    # Validate the given parameters for the given criteria set ID
    @abstractmethod
    def validate_parameters(self, criteria_set_id: str, parameters: ParametersType):
        pass

    # Stream the matrix for the given criteria set ID, parameter combination and value map
    @abstractmethod
    def stream_matrix(
            self,
            criteria_set_id: str,
            parameters: ParametersType,
            values: Optional[TaskItemValueMap] = None,
            locale: Optional[str] = None
    ) -> StreamMatrixResponse:
        pass

    # Get the metadata of all criteria sets supported by this service
    @abstractmethod
    def get_criteria_set_metadata_list(self) -> list[Metadata]:
        pass

    # Get the JSON schema for the given criteria set ID
    @abstractmethod
    def get_parameters_json_schema(self, criteria_set_id: str) -> dict[str, Any]:
        pass
