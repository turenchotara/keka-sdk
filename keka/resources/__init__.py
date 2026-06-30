from .base import AsyncBaseResource, BaseResource
from .helpdesk import AsyncHelpdeskResource, HelpdeskResource
from .hr import AsyncHRResource, HRResource
from .hris import (
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
from .leave import AsyncLeaveResource, LeaveResource

__all__ = [
    # Base
    "BaseResource",
    "AsyncBaseResource",
    # HR
    "HRResource",
    "AsyncHRResource",
    # Helpdesk
    "HelpdeskResource",
    "AsyncHelpdeskResource",
    # HRIS
    "GroupsResource",
    "AsyncGroupsResource",
    "DepartmentsResource",
    "AsyncDepartmentsResource",
    "LocationsResource",
    "AsyncLocationsResource",
    "JobTitlesResource",
    "AsyncJobTitlesResource",
    "CurrencyResource",
    "AsyncCurrencyResource",
    "NoticePeriodResource",
    "AsyncNoticePeriodResource",
    "ExitReasonsResource",
    "AsyncExitReasonsResource",
    # Leave
    "LeaveResource",
    "AsyncLeaveResource",
]
