"""
Interface for versioned services

Services that implement this interface can be managed by the VersionsService
"""
from abc import ABC
from typing import Optional


class IVersionedService(ABC):
    # The SemVer version of the service
    version: str

    # Whether the service supports the given protocol version
    def supports_protocol(self, protocol_version: float) -> bool:
        return self.version.startswith(str(protocol_version))


"""
Service for managing versions of services

The VersionsService class is a utility class for services which implement different versions of the protocol, and different versions of their
own service. For example, say you have a v1service, v11service, v2service and v21service with versions 1.0, 1.1, 2.0 and 2.1 respectively.
The VersionsService class can be used to manage these services:

from openframe_criteria_set_protocol.services import VersionsService


versions_service = new VersionsService([v1_service, v11_service, v2_service, v21_service]);
versions_service.get_latest_version(); // v21_service
versions_service.get_service_versions(1); // [v1_service, v11_service]
versions_service.get_service_versions(2); // [v2_service, v21_service]
versions_service.get('1.1'); // v11service
"""
class VersionsService:
    def __init__(self, versions: list[IVersionedService]):
        """
        :param versions: A list of services implementing IVersionedService
        """
        self.versions = versions

    def get_all(self) -> list[IVersionedService]:
        """
        Get all services
        """
        return self.versions

    def get_service_versions(self, protocol_version: float) -> list[IVersionedService]:
        """
        Retrieve the services which are compatible with the requested protocol version
        """
        return [service for service in self.versions if service.supports_protocol(protocol_version)]

    def get(self, version: str) -> Optional[IVersionedService]:
        """
        Retrieve a service by version
        """
        for service in self.versions:
            if service.version == version:
                return service

        return None

    def get_latest_version(self) -> IVersionedService:
        """
        Retrieve the latest service
        """
        return self.versions[-1]
