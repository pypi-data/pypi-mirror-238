"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.service_account_servers import (
    NetBoxResourceType,
    ServiceAccountServer,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ServiceAccountServerFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccountServer

        exclude = ("service_account",)

    hostname = factory.Faker("domain_name")
    service_account = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.service_accounts.ServiceAccountFactory",
    )
    netbox_resource_type = factory.fuzzy.FuzzyChoice(NetBoxResourceType)
    netbox_resource_id = 1
    netbox_parent_interface_id = 1
    service_account_id = factory.SelfAttribute("service_account.id")
