from typing import Any, Union

from .auth import AsyncAuthManager, AuthManager, KekaAuth
from .config import KekaConfig
from .resources.attendance import AsyncAttendanceResource, AttendanceResource
from .resources.helpdesk import AsyncHelpdeskResource, HelpdeskResource
from .resources.hr import AsyncHRResource, HRResource
from .resources.hris import (
    AsyncCurrencyResource,
    AsyncDepartmentsResource,
    AsyncExitReasonsResource,
    AsyncGroupsResource,
    AsyncJobTitlesResource,
    AsyncLocationsResource,
    AsyncNoticePeriodResource,
    CurrencyResource,
    DepartmentsResource,
    ExitReasonsResource,
    GroupsResource,
    JobTitlesResource,
    LocationsResource,
    NoticePeriodResource,
)
from .resources.leave import AsyncLeaveResource, LeaveResource
from .transport import AsyncTransport, Transport


def _coerce_config(config: Union[str, KekaConfig]) -> KekaConfig:
    if isinstance(config, KekaConfig):
        return config
    if isinstance(config, str):
        return KekaConfig(instance_url=config)
    raise TypeError("config must be a KekaConfig or an instance_url string")


def _validate_auth(auth: KekaAuth) -> KekaAuth:
    if not isinstance(auth, KekaAuth):
        raise TypeError("auth must be a KekaAuth instance")
    return auth


class KekaClient:
    """
    Synchronous Keka client.

    Args:
        auth: Credentials (:class:`KekaAuth`).
        config: A :class:`KekaConfig`, or an ``instance_url`` string.

    Example:
        >>> auth = KekaAuth(client_id="...", client_secret="...", api_key="...")
        >>> with KekaClient(auth, "https://acme.keka.com") as client:
        ...     result = client.hr.search_employee(work_email="a@acme.com")
    """

    def __init__(self, auth: KekaAuth, config: Union[str, KekaConfig]):
        self._auth_credentials = _validate_auth(auth)
        self.config = _coerce_config(config)
        self.transport = Transport(self.config)
        self.auth = AuthManager(self._auth_credentials, self.config, self.transport)

        # Core resources
        self.hr = HRResource(self.transport, self.config, self.auth)
        self.helpdesk = HelpdeskResource(self.transport, self.config, self.auth)

        # HRIS lookup resources
        self.groups = GroupsResource(self.transport, self.config, self.auth)
        self.departments = DepartmentsResource(self.transport, self.config, self.auth)
        self.locations = LocationsResource(self.transport, self.config, self.auth)
        self.job_titles = JobTitlesResource(self.transport, self.config, self.auth)
        self.currencies = CurrencyResource(self.transport, self.config, self.auth)
        self.notice_periods = NoticePeriodResource(self.transport, self.config, self.auth)
        self.exit_reasons = ExitReasonsResource(self.transport, self.config, self.auth)

        # Leave management resource
        self.leave = LeaveResource(self.transport, self.config, self.auth)

        # Attendance management resource
        self.attendance = AttendanceResource(self.transport, self.config, self.auth)

    @property
    def instance_url(self) -> str:
        return self.config.instance_url

    def authenticate(self) -> str:
        """Eagerly acquire an access token and return it."""
        return self.auth.authenticate()

    def close(self) -> None:
        self.transport.close()

    def __enter__(self) -> "KekaClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


class AsyncKekaClient:
    """
    Asynchronous Keka client. See :class:`KekaClient` for usage; use
    ``async with`` and ``await`` on resource methods.
    """

    def __init__(self, auth: KekaAuth, config: Union[str, KekaConfig]):
        self._auth_credentials = _validate_auth(auth)
        self.config = _coerce_config(config)
        self.transport = AsyncTransport(self.config)
        self.auth = AsyncAuthManager(self._auth_credentials, self.config, self.transport)

        # Core resources
        self.hr = AsyncHRResource(self.transport, self.config, self.auth)
        self.helpdesk = AsyncHelpdeskResource(self.transport, self.config, self.auth)

        # HRIS lookup resources
        self.groups = AsyncGroupsResource(self.transport, self.config, self.auth)
        self.departments = AsyncDepartmentsResource(self.transport, self.config, self.auth)
        self.locations = AsyncLocationsResource(self.transport, self.config, self.auth)
        self.job_titles = AsyncJobTitlesResource(self.transport, self.config, self.auth)
        self.currencies = AsyncCurrencyResource(self.transport, self.config, self.auth)
        self.notice_periods = AsyncNoticePeriodResource(self.transport, self.config, self.auth)
        self.exit_reasons = AsyncExitReasonsResource(self.transport, self.config, self.auth)

        # Leave management resource
        self.leave = AsyncLeaveResource(self.transport, self.config, self.auth)

        # Attendance management resource
        self.attendance = AsyncAttendanceResource(self.transport, self.config, self.auth)

    @property
    def instance_url(self) -> str:
        return self.config.instance_url

    async def authenticate(self) -> str:
        """Eagerly acquire an access token and return it."""
        return await self.auth.authenticate()

    async def close(self) -> None:
        await self.transport.close()

    async def __aenter__(self) -> "AsyncKekaClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
