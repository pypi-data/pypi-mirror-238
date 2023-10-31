"""Helper classes for scripts for cluster support packages."""

from cyberfusion.ClusterSupport._interfaces import (
    APIObjectInterface,
    sort_lists,
)
from cyberfusion.ClusterSupport.task_collections import TaskCollection

ENDPOINT_CUSTOMERS = "customers"
MODEL_CUSTOMERS = "customers"


class Customer(APIObjectInterface):
    """Represents object."""

    @sort_lists  # type: ignore[misc]
    def _set_attributes_from_model(
        self,
        obj: dict,
    ) -> None:
        """Set class attributes from API output."""
        self.id = obj["id"]
        self.team_code = obj["team_code"]
        self.identifier = obj["identifier"]
        self.dns_subdomain = obj["dns_subdomain"]
        self.netbox_default_prefix_ipv4_id = obj[
            "netbox_default_prefix_ipv4_id"
        ]
        self.netbox_default_prefix_ipv6_id = obj[
            "netbox_default_prefix_ipv6_id"
        ]
        self.netbox_default_vlan_id = obj["netbox_default_vlan_id"]
        self.netbox_vlan_ids = obj["netbox_vlan_ids"]
        self.created_at = obj["created_at"]
        self.updated_at = obj["updated_at"]

    def create(self, *, team_code: str) -> TaskCollection:
        """Create object."""
        url = f"/api/v1/{ENDPOINT_CUSTOMERS}"
        data = {"team_code": team_code}

        self.support.request.POST(url, data)
        response = self.support.request.execute()

        obj = TaskCollection(self.support)
        obj._set_attributes_from_model(response)

        return obj
