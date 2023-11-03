from typing import Any, Awaitable, Dict, Optional

import httpx
from httpx._types import HeaderTypes

from kt2 import __version__
from kt2.jwks import JWKS
from kt2.logging import koppeltaal_logger, noop_koppeltaal_logger
from kt2.models import (
    KT2ActivityDefinition,
    KT2CareTeam,
    KT2Endpoint,
    KT2Patient,
    KT2Practitioner,
    KT2Task,
)
from kt2.oauth import SmartFHIROAuth2
from kt2.settings import JWKSKeyPair
from kt2.types import (
    KT2ActivityDefinitionList,
    KT2CareTeamList,
    KT2EndpointList,
    KT2Id,
    KT2PatientList,
    KT2PracticionerList,
    KT2TaskList,
)
from kt2.utils import Methods, make_request, url


class KoppeltaalSDK(SmartFHIROAuth2[Dict[str, Any]]):
    """
    Example scopes:
    ActivityDefinition.cru
    Task.cru
    Patient.r
    Practitioner.r
    Endpoint.r
    """

    def __init__(
        self,
        client_name: str,
        fhir_url: str,
        oauth_token_url: str,
        oauth_authorize_url: str,
        domain: str,
        client_id: str,
        smart_config_url: str,
        jwks_keys: JWKSKeyPair,
        oauth_introspection_token_url: Optional[str] = None,
        connector_name: str = "kt2-python-sdk",
        enable_logger=False,
    ):
        self.connector_name = connector_name
        self.name: str = client_name
        self.fhir_url: str = fhir_url
        self.smart_config_url: str = smart_config_url
        self.domain: str = domain
        self.logger = koppeltaal_logger if enable_logger else noop_koppeltaal_logger

        # Do not define JWKS on client: instead pass on the object to SmartFHIROAuth2

        jwks = JWKS(jwks_keys)
        jwks.load_key_pair()

        super().__init__(
            client_id=client_id,
            authorize_endpoint=oauth_authorize_url,
            access_token_endpoint=oauth_token_url,
            fhir_url=fhir_url,
            jwks=jwks,
            introspection_token_endpoint=oauth_introspection_token_url,
        )

        self.request_headers = {
            "Accept": "application/fhir+json",
            "User-Agent": f"{self.connector_name}/{__version__}",
        }

    def default_headers(self, headers: HeaderTypes = {}) -> HeaderTypes:
        """Set default headers"""
        return {
            **self.request_headers,
            **{"Authorization": self.token.bearer_token},
            **headers,
        }

    def post_headers(self, id: KT2Id) -> HeaderTypes:
        print("id =", id)
        return self.default_headers(
            headers={
                # "If-None-Exist": id,
                "Prefer": "return=representation",
                "Content-Type": "application/fhir+json",
            }
        )

    def put_headers(self, version_id: KT2Id) -> HeaderTypes:
        return self.default_headers(
            headers={
                "If-Match": f'W/"{version_id}"',
                "Prefer": "return=representation",
                "Content-Type": "application/fhir+json",
            }
        )

    async def get_info(self, *args, **kwargs) -> None:
        """
        Get info from Koppeltaal Api
        """

        # FIXME: add SmartConfig Model so we can view data better
        async with httpx.AsyncClient(headers=self.request_headers) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=self.smart_config_url,
                logger=self.logger,
            )

    @url("/Patient", response_model=KT2Patient, many=True)
    async def get_patients(self, *args, **kwargs) -> Awaitable[KT2PatientList]:
        """
        Get all Patient resources from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=kwargs["url"],
                logger=self.logger,
            )

    @url("/Patient", response_model=KT2Patient)
    async def get_patient(self, id: str, *args, **kwargs) -> Awaitable[KT2Patient]:
        """
        Get single Patient resource by id from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=f'{kwargs["url"]}/{id}',
                logger=self.logger,
            )

    @url("/Practitioner", response_model=KT2Practitioner, many=True)
    async def get_practitioners(
        self, *args, **kwargs
    ) -> Awaitable[KT2PracticionerList]:
        """
        Get all Practitioner resources from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=kwargs["url"],
                logger=self.logger,
            )

    @url("/Practitioner", response_model=KT2Practitioner)
    async def get_practitioner(
        self, id: str, *args, **kwargs
    ) -> Awaitable[KT2Practitioner]:
        """
        Get single Practitioner resource by id from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=f'{kwargs["url"]}/{id}',
                logger=self.logger,
            )

    @url("/Endpoint", response_model=KT2Endpoint, many=True)
    async def get_endpoints(self, *args, **kwargs) -> Awaitable[KT2EndpointList]:
        """
        Get all Endpoint resources from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=kwargs["url"],
                logger=self.logger,
            )

    @url("/Endpoint", response_model=KT2Endpoint)
    async def get_endpoint(self, id: str, *args, **kwargs) -> Awaitable[KT2Endpoint]:
        """
        Get single Endpoint resource by id from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=f'{kwargs["url"]}/{id}',
                logger=self.logger,
            )

    @url("/CareTeam", response_model=KT2CareTeam, many=True)
    async def get_careteams(self, *args, **kwargs) -> Awaitable[KT2CareTeamList]:
        """
        Get all CareTeam resources from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=kwargs["url"],
                logger=self.logger,
            )

    @url("/CareTeam", response_model=KT2CareTeam)
    async def get_careteam(self, id: str, *args, **kwargs) -> Awaitable[KT2CareTeam]:
        """
        Get single CareTeam resource by id from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=f'{kwargs["url"]}/{id}',
                logger=self.logger,
            )

    @url("/ActivityDefinition", response_model=KT2ActivityDefinition, many=True)
    async def get_activitydefinitions(
        self, *args, **kwargs
    ) -> Awaitable[KT2ActivityDefinitionList]:
        """
        Get all ActivityDefinition resources from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=kwargs["url"],
                logger=self.logger,
            )

    @url("/ActivityDefinition", response_model=KT2ActivityDefinition)
    async def get_activitydefinition(
        self, id: str, *args, **kwargs
    ) -> Awaitable[KT2ActivityDefinition]:
        """
        Get single ActivityDefinition resource by id from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=f'{kwargs["url"]}/{id}',
                logger=self.logger,
            )

    @url("/ActivityDefinition", response_model=KT2ActivityDefinition)
    async def create_activitydefinition(
        self, activitydefinition: KT2ActivityDefinition, *args, **kwargs
    ) -> Awaitable[KT2ActivityDefinition]:
        """
        Create ActivityDefinition resource in Koppeltaal Api
        """

        async with httpx.AsyncClient(
            headers=self.post_headers(activitydefinition.id)
        ) as client:
            return await make_request(
                client,
                method=Methods.POST,
                url=kwargs["url"],
                data=activitydefinition.json(exclude_none=True, exclude_comments=True),
                logger=self.logger,
            )

    @url("/ActivityDefinition", response_model=KT2ActivityDefinition)
    async def update_activitydefinition(
        self, activitydefinition: KT2ActivityDefinition, *args, **kwargs
    ) -> Awaitable[KT2ActivityDefinition]:
        """
        Update ActivityDefinition resource in Koppeltaal Api
        """

        async with httpx.AsyncClient(
            headers=self.put_headers(activitydefinition.meta.versionId)
        ) as client:
            return await make_request(
                client,
                method=Methods.PUT,
                url=f'{kwargs["url"]}/{activitydefinition.id}',
                data=activitydefinition.json(exclude_none=True, exclude_comments=True),
                logger=self.logger,
            )

    @url("/ActivityDefinition", response_model=KT2ActivityDefinition)
    async def delete_activitydefinition(
        self, id: str, *args, **kwargs
    ) -> Awaitable[KT2ActivityDefinition]:
        """
        Get delete single ActivityDefinition resource by id from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.DELETE,
                url=f'{kwargs["url"]}/{id}',
                logger=self.logger,
            )

    @url("/Task", response_model=KT2Task, many=True)
    async def get_tasks(self, *args, **kwargs) -> Awaitable[KT2TaskList]:
        """
        Get all Task resources from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=kwargs["url"],
                logger=self.logger,
            )

    @url("/Task", response_model=KT2Task)
    async def get_task(self, id: str, *args, **kwargs) -> Awaitable[KT2Task]:
        """
        Get single Task resource by id from Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.default_headers()) as client:
            return await make_request(
                client,
                method=Methods.GET,
                url=f'{kwargs["url"]}/{id}',
                logger=self.logger,
            )

    @url("/Task", response_model=KT2ActivityDefinition)
    async def create_task(self, task: KT2Task, *args, **kwargs) -> Awaitable[KT2Task]:
        """
        Create Task resource in Koppeltaal Api
        """

        async with httpx.AsyncClient(headers=self.post_headers(task.id)) as client:
            return await make_request(
                client,
                method=Methods.POST,
                url=kwargs["url"],
                data=task.json(exclude_none=True, exclude_comments=True),
                logger=self.logger,
            )

    @url("/Task", response_model=KT2Task)
    async def update_task(self, task: KT2Task, *args, **kwargs) -> Awaitable[KT2Task]:
        """
        Update Task resource in Koppeltaal Api
        """

        async with httpx.AsyncClient(
            headers=self.put_headers(task.meta.versionId)
        ) as client:
            return await make_request(
                client,
                method=Methods.PUT,
                url=f'{kwargs["url"]}/{task.id}',
                data=task.json(exclude_none=True, exclude_comments=True),
                logger=self.logwger,
            )
