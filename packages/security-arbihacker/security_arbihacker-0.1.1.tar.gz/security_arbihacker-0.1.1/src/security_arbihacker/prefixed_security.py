from typing import Callable, Any, Sequence

from fastapi import params


class PrefixedSecurity(params.Security):
    def __init__(
        self,
        dependency: Callable[..., Any] | None,
        scopes: Sequence[str],
        prefix: str,
        sep: str = ":",
        use_cache: bool = True
    ):
        super().__init__(dependency, scopes=[f"{prefix}{sep}{scope}" for scope in scopes], use_cache=use_cache)


class RoleSecurity(PrefixedSecurity):
    def __init__(
        self, dependency: Callable[..., Any] | None, scopes: Sequence[str], sep: str = ":", use_cache: bool = True
    ):
        super().__init__(dependency, scopes=scopes, prefix="role", sep=sep, use_cache=use_cache)


class SubscriptionSecurity(PrefixedSecurity):
    def __init__(
        self, dependency: Callable[..., Any] | None, scopes: Sequence[str], sep: str = ":", use_cache: bool = True
    ):
        super().__init__(dependency, scopes=scopes, prefix="subscription", sep=sep, use_cache=use_cache)
