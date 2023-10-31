from pathlib import Path
from typing import Any, Union

import toml
from pydantic import BaseModel

config = None


class JWKSKeyPair(BaseModel):
    private_key_path: str
    public_key_path: str
    kid: str


class CommandLineArgs(BaseModel):
    # Base config
    config: str = "koppeltaal.toml"
    debug: bool = False


class ConfigFile(CommandLineArgs):
    client_name: str
    fhir_url: str
    oauth_token_url: str
    oauth_authorize_url: str
    oauth_introspection_token_url: str
    smart_config_url: str
    domain: str
    client_id: str
    jwks_keys: JWKSKeyPair


def load_settings(file_path: str) -> Union[Any, dict[str, Any]]:
    path = Path(file_path)
    if path.is_file():
        with open("koppeltaal.toml", "r") as config_file:
            return toml.loads(config_file.read())


def merge_config(config, custom_args) -> ConfigFile:
    # Merge commandline args with presedent over toml file args, except if there None
    filtered_args = {k: v for k, v in custom_args.items() if v is not None}
    return ConfigFile(**{**config, **filtered_args})
