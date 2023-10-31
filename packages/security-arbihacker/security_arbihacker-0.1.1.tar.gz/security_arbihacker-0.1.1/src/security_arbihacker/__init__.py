import itertools
import logging

from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, HTTPBearer
from jose import jwt, JWTError

__all__ = [
    "JWTBearer",
    "get_security",
    "CredentialsException",
    "check_token_and_scopes",
]


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> str | None:
        result = await super().__call__(request)
        if result is None:
            return None
        return result.credentials


def get_security(
    token_url: str | None = None,
    auto_error: bool = True,
    scheme_name: str | None = None,
    description: str | None = None,
):
    if token_url is None:
        return JWTBearer(auto_error=auto_error, scheme_name=scheme_name, description=description)
    else:
        return OAuth2PasswordBearer(
            tokenUrl=token_url,
            auto_error=auto_error,
            scheme_name=scheme_name,
            description=description,
        )


class CredentialsException(HTTPException):
    def __init__(self, authenticate_value="bearer") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )


def check_token_and_scopes(
    security_scopes: SecurityScopes,
    token: str,
    key: str | dict,
    algorithms: str | list,
    subject: str | None = None,
    auto_error=True,
) -> dict | None:
    def maybe_raise_credentials_exception(reason=None):
        if reason is not None:
            logging.warning({"message": f"Token invalid: {reason}", "reason": reason, "sub": subject})
        if security_scopes.scopes:
            authenticate_value = f"bearer scope={security_scopes.scope_str}"
        else:
            authenticate_value = "bearer"
        if auto_error:
            raise CredentialsException(authenticate_value)
        return None

    try:
        if subject is not None:
            payload = jwt.decode(token, key, algorithms=algorithms, subject=subject)
        else:
            payload = jwt.decode(token, key, algorithms=algorithms)
    except JWTError as e:
        return maybe_raise_credentials_exception(str(e))
    if "sub" not in payload:
        return maybe_raise_credentials_exception("sub not in payload")
    if not security_scopes.scopes:
        return payload

    security_set = set(security_scopes.scopes)
    payload_set = set(payload["scope"].strip().split(" "))
    for security_scope in security_set:
        security_fragments = security_scope.split(":")

        scope_present = False
        for payload_scope in payload_set:
            payload_fragments = payload_scope.split(":")

            if "superuser" in payload_fragments:
                return payload

            scope_match = True
            for security_f, payload_f in itertools.zip_longest(security_fragments, payload_fragments, fillvalue="*"):
                if not (
                    security_f == "*" or payload_f == {"all", "admin", "superuser", "*"} or security_f == payload_f
                ):
                    scope_match = False
            if scope_match:
                scope_present = True
                break

        if not scope_present:
            return maybe_raise_credentials_exception("scope mismatch")
    return payload
