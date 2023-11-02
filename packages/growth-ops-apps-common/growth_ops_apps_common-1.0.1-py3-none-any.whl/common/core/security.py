from typing import Union

import jwt
import jwt.algorithms
import requests
from dependency_injector.wiring import inject
from fastapi import HTTPException, status, Header
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidAudienceError

from ..services.metadata import MetadataService

OIDC_ENDPOINT = 'https://accounts.google.com/.well-known/openid-configuration'
GOOGLE_CONFIG = None
CERTS = None


@inject
def verify_google(
    authorization: Union[str, None] = Header(default=None),
):
    metadata_service = MetadataService()
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Please use a valid token from google.com"
        )

    token = authorization.replace('Bearer ', '')
    global GOOGLE_CONFIG
    if GOOGLE_CONFIG is None:
        GOOGLE_CONFIG = requests.get(OIDC_ENDPOINT).json()

    global CERTS
    if CERTS is None:
        CERTS = requests.get(GOOGLE_CONFIG['jwks_uri']).json()
    public_keys = {}
    for jwk in CERTS['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
    kid = jwt.get_unverified_header(token)['kid']
    key = public_keys[kid]

    try:
        payload = jwt.decode(token, key=key, algorithms=['RS256'], audience=metadata_service.public_url)
        print(f"decoded: {payload}")
        if payload['iss'] != 'https://accounts.google.com':
            print(f"Issuer is invalid: {payload['iss']} != https://accounts.google.com")
            print(f"Failed to validate JWT: {token}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized. Please use a valid token from google"
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature has expired. Please use a valid token from google"
        )
    except InvalidSignatureError:
        print(f"Invalid JWT for ({token})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to validate token. Please use a valid token from google"
        )
    except InvalidAudienceError:
        print(f"Invalid audience for ({token})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to validate token. Please use a valid token from google"
        )



