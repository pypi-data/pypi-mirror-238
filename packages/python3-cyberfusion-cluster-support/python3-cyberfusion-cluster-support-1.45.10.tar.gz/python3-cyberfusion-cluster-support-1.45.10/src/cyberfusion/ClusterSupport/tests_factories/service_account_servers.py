"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.service_account_servers import (
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
    service_account_id = factory.SelfAttribute("service_account.id")
