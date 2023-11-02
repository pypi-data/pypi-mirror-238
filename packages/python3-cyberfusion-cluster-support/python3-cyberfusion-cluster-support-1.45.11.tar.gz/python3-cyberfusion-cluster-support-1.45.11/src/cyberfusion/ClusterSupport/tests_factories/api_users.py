"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.api_users import APIUser
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class APIUserFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = APIUser

    customer_id = 1
    username = factory.Faker("user_name")
    is_active = factory.Faker("boolean")
    is_superuser = False
    trusted_ip_networks = None
    password = factory.Faker("password", length=24)
