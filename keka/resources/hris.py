from typing import Any, Dict, Optional

from .base import AsyncBaseResource, BaseResource


def _build_groups_params(
    group_type_ids: Optional[str] = None,
    system_group_types: Optional[str] = None,
    last_modified: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/groups."""
    params: Dict[str, Any] = {
        "groupTypeIds": group_type_ids,
        "systemGroupTypes": system_group_types,
        "lastModified": last_modified,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_group_types_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/grouptypes."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_departments_params(
    department_ids: Optional[str] = None,
    last_modified: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/departments."""
    params: Dict[str, Any] = {
        "departmentIds": department_ids,
        "lastModified": last_modified,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_locations_params(
    last_modified: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/locations."""
    params: Dict[str, Any] = {
        "lastModified": last_modified,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_job_titles_params(
    job_title_ids: Optional[str] = None,
    last_modified: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/jobtitles."""
    params: Dict[str, Any] = {
        "jobTitleIds": job_title_ids,
        "lastModified": last_modified,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_currencies_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/currencies."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_notice_periods_params(
    notice_period_ids: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/noticeperiods."""
    params: Dict[str, Any] = {
        "noticePeriodIds": notice_period_ids,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_exit_reasons_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/exitreasons."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


class GroupsResource(BaseResource):
    """Synchronous Groups resource for organizational group management."""

    endpoint = "hris/groups"

    def list_groups(
        self,
        group_type_ids: Optional[str] = None,
        system_group_types: Optional[str] = None,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all groups (paginated).

        Args:
            group_type_ids: Comma-separated list of group type IDs to filter.
            system_group_types: Comma-separated system group types
                (0=None, 1=BusinessUnit, 2=Department, 3=OrgLocation,
                4=CostCenter, 5=Paygroup, 6=ProjectTeam, 7=Team,
                8=ClientTeam, 9=LegalEntity).
            last_modified: Return records modified after this date (ISO 8601).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with groups data.
        """
        params = _build_groups_params(
            group_type_ids=group_type_ids,
            system_group_types=system_group_types,
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(self.endpoint, params=params)

    def list_group_types(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all group types (paginated).

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with group types data.
        """
        params = _build_group_types_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("hris/grouptypes", params=params)


class AsyncGroupsResource(AsyncBaseResource):
    """Asynchronous Groups resource."""

    endpoint = "hris/groups"

    async def list_groups(
        self,
        group_type_ids: Optional[str] = None,
        system_group_types: Optional[str] = None,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all groups (paginated). See :meth:`GroupsResource.list_groups`."""
        params = _build_groups_params(
            group_type_ids=group_type_ids,
            system_group_types=system_group_types,
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(self.endpoint, params=params)

    async def list_group_types(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all group types (paginated). See :meth:`GroupsResource.list_group_types`."""
        params = _build_group_types_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("hris/grouptypes", params=params)


class DepartmentsResource(BaseResource):
    """Synchronous Departments resource."""

    endpoint = "hris/departments"

    def list_departments(
        self,
        department_ids: Optional[str] = None,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all departments (paginated).

        Args:
            department_ids: Comma-separated list of department IDs to filter.
            last_modified: Return records modified after this date (ISO 8601).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with departments data.
        """
        params = _build_departments_params(
            department_ids=department_ids,
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(self.endpoint, params=params)


class AsyncDepartmentsResource(AsyncBaseResource):
    """Asynchronous Departments resource."""

    endpoint = "hris/departments"

    async def list_departments(
        self,
        department_ids: Optional[str] = None,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all departments (paginated). See :meth:`DepartmentsResource.list_departments`."""
        params = _build_departments_params(
            department_ids=department_ids,
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(self.endpoint, params=params)


class LocationsResource(BaseResource):
    """Synchronous Locations resource."""

    endpoint = "hris/locations"

    def list_locations(
        self,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all locations (paginated).

        Args:
            last_modified: Return records modified after this date (ISO 8601).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with locations data.
        """
        params = _build_locations_params(
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(self.endpoint, params=params)


class AsyncLocationsResource(AsyncBaseResource):
    """Asynchronous Locations resource."""

    endpoint = "hris/locations"

    async def list_locations(
        self,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all locations (paginated). See :meth:`LocationsResource.list_locations`."""
        params = _build_locations_params(
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(self.endpoint, params=params)


class JobTitlesResource(BaseResource):
    """Synchronous Job Titles resource."""

    endpoint = "hris/jobtitles"

    def list_job_titles(
        self,
        job_title_ids: Optional[str] = None,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all job titles (paginated).

        Args:
            job_title_ids: Comma-separated list of job title IDs to filter.
            last_modified: Return records modified after this date (ISO 8601).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with job titles data.
        """
        params = _build_job_titles_params(
            job_title_ids=job_title_ids,
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(self.endpoint, params=params)


class AsyncJobTitlesResource(AsyncBaseResource):
    """Asynchronous Job Titles resource."""

    endpoint = "hris/jobtitles"

    async def list_job_titles(
        self,
        job_title_ids: Optional[str] = None,
        last_modified: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all job titles (paginated). See :meth:`JobTitlesResource.list_job_titles`."""
        params = _build_job_titles_params(
            job_title_ids=job_title_ids,
            last_modified=last_modified,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(self.endpoint, params=params)


class CurrencyResource(BaseResource):
    """Synchronous Currency resource."""

    endpoint = "hris/currencies"

    def list_currencies(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all currencies (paginated).

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with currencies data.
        """
        params = _build_currencies_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(self.endpoint, params=params)


class AsyncCurrencyResource(AsyncBaseResource):
    """Asynchronous Currency resource."""

    endpoint = "hris/currencies"

    async def list_currencies(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all currencies (paginated). See :meth:`CurrencyResource.list_currencies`."""
        params = _build_currencies_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(self.endpoint, params=params)


class NoticePeriodResource(BaseResource):
    """Synchronous Notice Period resource."""

    endpoint = "hris/noticeperiods"

    def list_notice_periods(
        self,
        notice_period_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all notice periods (paginated).

        Args:
            notice_period_ids: Comma-separated list of notice period IDs to filter.
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with notice periods data.
        """
        params = _build_notice_periods_params(
            notice_period_ids=notice_period_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(self.endpoint, params=params)


class AsyncNoticePeriodResource(AsyncBaseResource):
    """Asynchronous Notice Period resource."""

    endpoint = "hris/noticeperiods"

    async def list_notice_periods(
        self,
        notice_period_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all notice periods (paginated). See :meth:`NoticePeriodResource.list_notice_periods`."""
        params = _build_notice_periods_params(
            notice_period_ids=notice_period_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(self.endpoint, params=params)


class ExitReasonsResource(BaseResource):
    """Synchronous Exit Reasons resource."""

    endpoint = "hris/exitreasons"

    def list_exit_reasons(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all exit reasons (paginated).

        Returns both exitReason and terminationReason arrays.

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Response with exitReason and terminationReason arrays.
        """
        params = _build_exit_reasons_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._get(self.endpoint, params=params)


class AsyncExitReasonsResource(AsyncBaseResource):
    """Asynchronous Exit Reasons resource."""

    endpoint = "hris/exitreasons"

    async def list_exit_reasons(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all exit reasons. See :meth:`ExitReasonsResource.list_exit_reasons`."""
        params = _build_exit_reasons_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._get(self.endpoint, params=params)
