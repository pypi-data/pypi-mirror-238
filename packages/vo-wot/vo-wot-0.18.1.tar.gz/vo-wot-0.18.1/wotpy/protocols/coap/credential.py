#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Credential classes that add the proper authorization creds to the outgoing requests.
"""

from base64 import b64encode
from abc import ABCMeta, abstractmethod

from aiocoap.optiontypes import StringOption

from wotpy.wot.enums import SecuritySchemeType


class BaseCredential(metaclass=ABCMeta):
    """This is the base credential class describing
    the credential interface."""

    def __init__(self, security_credentials):
        self._security_credentials = security_credentials

    @abstractmethod
    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()

    @classmethod
    def build(cls, security_scheme_dict, security_credentials):
        """Builds an instance of the appropriate subclass for the given SecurityScheme."""

        klass_map = {
            SecuritySchemeType.NOSEC: NoSecurityCredential,
            SecuritySchemeType.AUTO: AutoSecurityCredential,
            SecuritySchemeType.COMBO: ComboSecurityCredential,
            SecuritySchemeType.BASIC: BasicSecurityCredential,
            SecuritySchemeType.DIGEST: DigestSecurityCredential,
            SecuritySchemeType.APIKEY: APIKeySecurityCredential,
            SecuritySchemeType.BEARER: BearerSecurityCredential,
            SecuritySchemeType.PSK: PSKSecurityCredential,
            SecuritySchemeType.OAUTH2: OAuth2SecurityCredential
        }

        scheme_type = security_scheme_dict.get("scheme")
        klass = klass_map.get(scheme_type)

        if not klass:
            raise ValueError("Unknown scheme: {}".format(scheme_type))

        return klass(security_credentials)


class NoSecurityCredential(BaseCredential):
    """Credential that allows all requests."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        return request


class AutoSecurityCredential(BaseCredential):
    """Auto security credential."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()


class ComboSecurityCredential(BaseCredential):
    """Combinator of security schemes credential."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()


class BasicSecurityCredential(BaseCredential):
    """Basic username and password credential."""

    def __init__(self, security_credentials):
        self._username = security_credentials.get("username", None)
        self._password = security_credentials.get("password", None)

        assert self._username is not None and self._password is not None

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        encoded_creds = b64encode(f"{self._username}:{self._password}".encode("ascii"))
        encoded_creds_str = encoded_creds.decode("ascii")
        auth_header = f"Basic {encoded_creds_str}"
        request.opt.add_option(StringOption(2048, auth_header))

        return request


class DigestSecurityCredential(BaseCredential):
    """Digest credential."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()


class APIKeySecurityCredential(BaseCredential):
    """API Key credential."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()


class BearerSecurityCredential(BaseCredential):
    """Bearer token credential."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()


class PSKSecurityCredential(BaseCredential):
    """Pre shared key credential."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()


class OAuth2SecurityCredential(BaseCredential):
    """OAuth2 credential."""

    def sign(self, request):
        """Adds the appropriate authorization header to the request."""

        raise NotImplementedError()
