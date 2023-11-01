# -*- coding: utf-8 -*-
"""
    pip_services4_config.auth.ICredentialStore
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Credential store interface
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional

from pip_services4_components.context import IContext

from .CredentialParams import CredentialParams


class ICredentialStore(ABC):
    """
    Interface for credential stores which are used to store
    and lookup credentials to authenticate against external services.
    """

    def store(self, context: Optional[IContext], key: str, credential: CredentialParams):
        """
        Stores credential parameters into the store.

        :param context: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the credential.

        :param credential: a credential to be stored.
        """
        raise NotImplementedError('Method from interface definition')

    def lookup(self, context: Optional[IContext], key: str) -> CredentialParams:
        """
        Lookups credential parameters by its key.

        :param context: (optional) transaction id to trace execution through call chain.

        :param key: a key to uniquely identify the credential.

        :return: found credential parameters or None if nothing was found
        """
        raise NotImplementedError('Method from interface definition')
