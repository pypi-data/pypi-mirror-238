# Moved from: koppeltaal.jwks

import json
from pathlib import Path

from jwt import PyJWK, PyJWKClient
from jwt.algorithms import RSAAlgorithm
from jwt.types import JWKDict

from kt2.settings import JWKSKeyPair


def get_signing_key_from_jwks(self, kid: str, url: str) -> PyJWK:
    """
    Get signing from .well-known endpoint and generate validation key

    Returns:
        PyJWK: key for decoding JWT tokens
    """
    jwks_client = PyJWKClient(url)
    return jwks_client.get_signing_key(kid=kid)


class JWKS:
    def __init__(self, keys: JWKSKeyPair) -> None:
        self.keys = keys
        self.kid = keys.kid
        self.private_key = None
        self.public_key = None
        self.algorithm = RSAAlgorithm(RSAAlgorithm.SHA384)

    def json(self) -> JWKDict:
        """
        Expose public key in jwks format

        Returns:
            JWKDict: JSON Web Key format
        """
        jwk = json.loads(self.algorithm.to_jwk(self.public_key))
        jwk['kid'] = self.kid
        return jwk

    def load_key_pair(self) -> None:
        private_key_path = Path(self.keys.private_key_path)
        public_key_path = Path(self.keys.public_key_path)

        try:
            private_key_path.resolve(strict=True)
            public_key_path.resolve(strict=True)
        except FileNotFoundError:
            raise FileNotFoundError("Keypair incomplete or not enabled on server")
        else:
            with open(private_key_path) as keyfile:
                self.private_key = self.algorithm.prepare_key(keyfile.read())

            with open(public_key_path) as keyfile:
                self.public_key = self.algorithm.prepare_key(keyfile.read())
