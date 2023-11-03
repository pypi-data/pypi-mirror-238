import asyncio

import click
from rich import print

from kt2 import __version__ as VERSION
from kt2.client import KoppeltaalSDK
from kt2.helpers import font
from kt2.settings import CommandLineArgs, ConfigFile, load_settings, merge_config

# ----------------------------------------------------------------------------
# KoppeltaalAsyncRunner: runs KoppeltaalSDK in aysnc-mode
# ----------------------------------------------------------------------------


class KoppeltaalAsyncRunner:
    def __init__(self, config: ConfigFile, debug: bool):
        self.config: ConfigFile = config

        # build SDK
        self.client = KoppeltaalSDK(
            client_name=self.config.client_name,
            fhir_url=self.config.fhir_url,
            oauth_token_url=self.config.oauth_token_url,
            oauth_authorize_url=self.config.oauth_authorize_url,
            smart_config_url=self.config.smart_config_url,
            domain=self.config.domain,
            client_id=self.config.client_id,
            oauth_introspection_token_url=self.config.oauth_introspection_token_url,
            jwks_keys=self.config.jwks_keys,
            enable_logger=True,
        )

    async def get_patients(self) -> None:
        """Get all Patient resources from Koppeltaal"""
        response = await self.client.get_patients()
        print(response)

    async def get_patient(self, id: str) -> None:
        """Get single Patient resource from Koppeltaal"""
        response = await self.client.get_patient(id=id)
        print(response)

    async def get_practitioners(self) -> None:
        """Get all Practitioner resources from Koppeltaal"""
        response = await self.client.get_practitioners()
        print(response)

    async def get_practitioner(self, id: str) -> None:
        """Get single Practitioner resource from Koppeltaal"""
        response = await self.client.get_practitioner(id=id)
        print(response)

    async def get_careteams(self) -> None:
        """Get all CareTeam resources from Koppeltaal"""
        response = await self.client.get_careteams()
        print(response)

    async def get_careteam(self, id: str) -> None:
        """Get single CareTeam resource from Koppeltaal"""
        response = await self.client.get_careteam(id=id)
        print(response)

    async def get_endpoints(self) -> None:
        """Get all Endpoint resources from Koppeltaal"""
        response = await self.client.get_endpoints()
        print(response)

    async def get_endpoint(self, id: str) -> None:
        """Get single Endpoint resource from Koppeltaal"""
        response = await self.client.get_endpoint(id=id)
        print(response)

    async def get_activitydefinitions(self) -> None:
        """Get all ActivityDefinition resources from Koppeltaal"""
        response = await self.client.get_activitydefinitions()
        print(response)

    async def get_activitydefinition(self, id: str) -> None:
        """Get single ActivityDefinition resource from Koppeltaal"""
        response = await self.client.get_activitydefinition(id=id)
        print(response)

    async def delete_activitydefinition(self, id: str) -> None:
        """Get single ActivityDefinition resource from Koppeltaal"""
        response = await self.client.delete_activitydefinition(id=id)
        print(response)

    async def get_tasks(self) -> None:
        """Get all Task resources from Koppeltaal"""
        response = await self.client.get_tasks()
        print(response)

    async def get_task(self, id: str) -> None:
        """Get single Task resource from Koppeltaal"""
        response = await self.client.get_task(id=id)
        print(response)

    async def get_info(
        self,
    ) -> None:
        """Show information for Koppeltaal Api"""
        info = await self.client.get_info()
        print(info)


class KoppeltaalCli:
    """Koppeltaal Api Cli wrapper"""

    def __init__(self, **kwargs) -> None:
        # Get commandline arguments
        self.args = CommandLineArgs(**kwargs)
        # Get toml file settings
        self.toml_config = load_settings(self.args.config)
        # build config
        self.config = merge_config(self.toml_config, self.args.dict())
        # build runner
        self.runner = KoppeltaalAsyncRunner(self.config, self.args.debug)

    # ----------------------------------------------------------------------------#
    # FHIR Endpoints                                                              #
    # ----------------------------------------------------------------------------#

    def patients(self) -> None:
        asyncio.run(self.runner.get_patients())

    def patient(self, id: str) -> None:
        asyncio.run(self.runner.get_patient(id=id))

    def practitioners(self) -> None:
        asyncio.run(self.runner.get_practitioners())

    def practitioner(self, id: str) -> None:
        asyncio.run(self.runner.get_practitioner(id=id))

    def endpoints(self) -> None:
        asyncio.run(self.runner.get_endpoints())

    def endpoint(self, id: str) -> None:
        asyncio.run(self.runner.get_endpoint(id=id))

    def activitydefinitions(self) -> None:
        asyncio.run(self.runner.get_activitydefinitions())

    def activitydefinition(self, id: str) -> None:
        asyncio.run(self.runner.get_activitydefinition(id=id))

    def delete_activitydefinition(self, id: str) -> None:
        asyncio.run(self.runner.delete_activitydefinition(id=id))

    def tasks(self) -> None:
        asyncio.run(self.runner.get_tasks())

    def task(self, id: str) -> None:
        asyncio.run(self.runner.get_task(id=id))

    # ----------------------------------------------------------------------------#
    # Function for info, version, config, and other usefull insights              #
    # ----------------------------------------------------------------------------#

    def info(self) -> None:
        asyncio.run(self.runner.get_info())

    def show_version(self) -> None:
        click.secho("Koppeltaal CLI tools")
        click.secho(font.renderText("Koppeltaal"), fg="blue")
        click.secho(f"Version {VERSION}")


pass_koppeltaal = click.make_pass_decorator(KoppeltaalCli, ensure=True)
