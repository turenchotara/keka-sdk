from typing import Any, Dict, Optional

from ..types import ApprovalStatusEnum, SessionType
from .base import AsyncBaseResource, BaseResource


def _build_attendance_records_params(
    employee_ids: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/attendance."""
    params: Dict[str, Any] = {
        "employeeIds": employee_ids,
        "from": from_date,
        "to": to_date,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_capture_scheme_params(
    capturescheme_ids: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/capturescheme."""
    params: Dict[str, Any] = {
        "captureschemeIds": capturescheme_ids,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_shift_policies_params(
    shift_policy_ids: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/shiftpolicies."""
    params: Dict[str, Any] = {
        "shiftPolicyIds": shift_policy_ids,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_tracking_policies_params(
    tracking_policy_ids: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/penalisationpolicies."""
    params: Dict[str, Any] = {
        "trackingPolicyIds": tracking_policy_ids,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_weekly_off_policies_params(
    weekly_off_policy_ids: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/weeklyoffpolicies."""
    params: Dict[str, Any] = {
        "weeklyOffPolicyIds": weekly_off_policy_ids,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_holiday_calendars_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/holidayscalendar."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_holidays_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/holidayscalendar/{calendarId}/holidays."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_on_duty_params(
    employee_ids: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/od."""
    params: Dict[str, Any] = {
        "employeeIds": employee_ids,
        "from": from_date,
        "to": to_date,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_wfh_params(
    employee_ids: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/wfh."""
    params: Dict[str, Any] = {
        "employeeIds": employee_ids,
        "from": from_date,
        "to": to_date,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_time_entry_body(
    employee_id: str,
    timestamp: str,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for POST /attendance/employee/timeentry."""
    body: Dict[str, Any] = {
        "employeeId": employee_id,
        "timestamp": timestamp,
    }
    if note is not None:
        body["note"] = note
    return body


def _build_on_duty_body(
    employee_id: str,
    from_date: str,
    to_date: str,
    from_session: Optional[SessionType] = None,
    to_session: Optional[SessionType] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for POST /time/od."""
    body: Dict[str, Any] = {
        "employeeId": employee_id,
        "fromDate": from_date,
        "toDate": to_date,
    }
    if from_session is not None:
        body["fromSession"] = from_session
    if to_session is not None:
        body["toSession"] = to_session
    if note is not None:
        body["note"] = note
    return body


def _build_wfh_body(
    employee_id: str,
    from_date: str,
    to_date: str,
    from_session: Optional[SessionType] = None,
    to_session: Optional[SessionType] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for POST /time/wfh."""
    body: Dict[str, Any] = {
        "employeeId": employee_id,
        "fromDate": from_date,
        "toDate": to_date,
    }
    if from_session is not None:
        body["fromSession"] = from_session
    if to_session is not None:
        body["toSession"] = to_session
    if note is not None:
        body["note"] = note
    return body


def _build_approval_status_body(
    status: ApprovalStatusEnum,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for PUT /time/{od|wfh}/{requestId}/status."""
    body: Dict[str, Any] = {
        "status": status,
    }
    if note is not None:
        body["note"] = note
    return body


class AttendanceResource(BaseResource):
    """Synchronous Attendance resource for attendance management operations."""

    endpoint = "time"

    def list_records(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all attendance records (paginated).

        Gets all attendance records between date range ``from`` and ``to``.
        If both are not specified, last 30 days records are returned.
        The difference between from and to date cannot be more than 90 days.

        Args:
            employee_ids: Comma-separated list of employee IDs to filter.
            from_date: Start date (ISO 8601 format).
            to_date: End date (ISO 8601 format, max 90 days from from_date).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with attendance records.
        """
        params = _build_attendance_records_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/attendance", params=params)

    def list_capture_schemes(
        self,
        capturescheme_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all capture schemes (paginated).

        Args:
            capturescheme_ids: Comma-separated capture scheme IDs to filter.
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with capture schemes.
        """
        params = _build_capture_scheme_params(
            capturescheme_ids=capturescheme_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/capturescheme", params=params)

    def list_shift_policies(
        self,
        shift_policy_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all shift policies (paginated).

        Args:
            shift_policy_ids: Comma-separated shift policy IDs to filter.
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with shift policies.
        """
        params = _build_shift_policies_params(
            shift_policy_ids=shift_policy_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/shiftpolicies", params=params)

    def list_tracking_policies(
        self,
        tracking_policy_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all tracking/penalisation policies (paginated).

        Args:
            tracking_policy_ids: Comma-separated tracking policy IDs to filter.
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with tracking policies.
        """
        params = _build_tracking_policies_params(
            tracking_policy_ids=tracking_policy_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/penalisationpolicies", params=params)

    def list_weekly_off_policies(
        self,
        weekly_off_policy_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all weekly off policies (paginated).

        Args:
            weekly_off_policy_ids: Comma-separated weekly off policy IDs to filter.
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with weekly off policies.
        """
        params = _build_weekly_off_policies_params(
            weekly_off_policy_ids=weekly_off_policy_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/weeklyoffpolicies", params=params)

    def list_holiday_calendars(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all holiday calendars (paginated).

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with holiday calendars.
        """
        params = _build_holiday_calendars_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/holidayscalendar", params=params)

    def list_holidays(
        self,
        calendar_id: str,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all holidays for a specific holiday calendar (paginated).

        Args:
            calendar_id: The holiday calendar ID.
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with holidays.
        """
        params = _build_holidays_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(
            f"time/holidayscalendar/{calendar_id}/holidays", params=params
        )

    def create_time_entry_for_employee(
        self,
        employee_id: str,
        timestamp: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a time entry for a specific employee (employee ID in URL path).

        Args:
            employee_id: The employee ID (used in URL path).
            timestamp: Clock-in/out timestamp (ISO 8601 format).
            note: Optional note for the time entry.

        Returns:
            Response with created time entry details.
        """
        body = _build_time_entry_body(
            employee_id=employee_id,
            timestamp=timestamp,
            note=note,
        )
        return self._post(
            f"attendance/employee/{employee_id}/timeentry", json=body
        )

    def create_time_entry(
        self,
        employee_id: str,
        timestamp: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a time entry (employee ID in request body).

        Args:
            employee_id: The employee ID.
            timestamp: Clock-in/out timestamp (ISO 8601 format).
            note: Optional note for the time entry.

        Returns:
            Response with created time entry details.
        """
        body = _build_time_entry_body(
            employee_id=employee_id,
            timestamp=timestamp,
            note=note,
        )
        return self._post("attendance/employee/timeentry", json=body)

    def list_on_duty_requests(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all on-duty requests (paginated).

        Args:
            employee_ids: Comma-separated list of employee IDs to filter.
            from_date: Start date (ISO 8601 format).
            to_date: End date (ISO 8601 format).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with on-duty requests.
        """
        params = _build_on_duty_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/od", params=params)

    def create_on_duty_request(
        self,
        employee_id: str,
        from_date: str,
        to_date: str,
        from_session: Optional[SessionType] = None,
        to_session: Optional[SessionType] = None,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create an on-duty request.

        Args:
            employee_id: Employee ID for whom on-duty is being requested.
            from_date: On-duty start date (ISO 8601 format).
            to_date: On-duty end date (ISO 8601 format).
            from_session: Start session (0=FirstHalf, 1=SecondHalf).
            to_session: End session (0=FirstHalf, 1=SecondHalf).
            note: Optional note/reason for on-duty.

        Returns:
            Response with created on-duty request details.
        """
        body = _build_on_duty_body(
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
            from_session=from_session,
            to_session=to_session,
            note=note,
        )
        return self._post("time/od", json=body)

    def list_wfh_requests(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all work-from-home requests (paginated).

        Args:
            employee_ids: Comma-separated list of employee IDs to filter.
            from_date: Start date (ISO 8601 format).
            to_date: End date (ISO 8601 format).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with WFH requests.
        """
        params = _build_wfh_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate("time/wfh", params=params)

    def create_wfh_request(
        self,
        employee_id: str,
        from_date: str,
        to_date: str,
        from_session: Optional[SessionType] = None,
        to_session: Optional[SessionType] = None,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a work-from-home request.

        Args:
            employee_id: Employee ID for whom WFH is being requested.
            from_date: WFH start date (ISO 8601 format).
            to_date: WFH end date (ISO 8601 format).
            from_session: Start session (0=FirstHalf, 1=SecondHalf).
            to_session: End session (0=FirstHalf, 1=SecondHalf).
            note: Optional note/reason for WFH.

        Returns:
            Response with created WFH request details.
        """
        body = _build_wfh_body(
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
            from_session=from_session,
            to_session=to_session,
            note=note,
        )
        return self._post("time/wfh", json=body)

    def update_approval_status(
        self,
        request_id: str,
        request_type: str,
        status: ApprovalStatusEnum,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update the approval status of an on-duty or WFH request.

        Args:
            request_id: The request ID to update.
            request_type: Type of request — ``"od"`` or ``"wfh"``.
            status: New approval status (0=Pending, 1=Approved, 2=Rejected, 3=Cancelled).
            note: Optional note for the status update.

        Returns:
            Response confirming the status update.

        Raises:
            ValueError: If ``request_type`` is not ``"od"`` or ``"wfh"``.
        """
        if request_type not in ("od", "wfh"):
            raise ValueError(
                f"request_type must be 'od' or 'wfh', got {request_type!r}"
            )
        body = _build_approval_status_body(status=status, note=note)
        return self._put(f"time/{request_type}/{request_id}/status", json=body)


class AsyncAttendanceResource(AsyncBaseResource):
    """Asynchronous Attendance resource for attendance management operations."""

    endpoint = "time"

    async def list_records(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all attendance records (paginated). See :meth:`AttendanceResource.list_records`."""
        params = _build_attendance_records_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/attendance", params=params)

    async def list_capture_schemes(
        self,
        capturescheme_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all capture schemes (paginated). See :meth:`AttendanceResource.list_capture_schemes`."""
        params = _build_capture_scheme_params(
            capturescheme_ids=capturescheme_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/capturescheme", params=params)

    async def list_shift_policies(
        self,
        shift_policy_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all shift policies (paginated). See :meth:`AttendanceResource.list_shift_policies`."""
        params = _build_shift_policies_params(
            shift_policy_ids=shift_policy_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/shiftpolicies", params=params)

    async def list_tracking_policies(
        self,
        tracking_policy_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all tracking policies (paginated). See :meth:`AttendanceResource.list_tracking_policies`."""
        params = _build_tracking_policies_params(
            tracking_policy_ids=tracking_policy_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/penalisationpolicies", params=params)

    async def list_weekly_off_policies(
        self,
        weekly_off_policy_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all weekly off policies (paginated). See :meth:`AttendanceResource.list_weekly_off_policies`."""
        params = _build_weekly_off_policies_params(
            weekly_off_policy_ids=weekly_off_policy_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/weeklyoffpolicies", params=params)

    async def list_holiday_calendars(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all holiday calendars (paginated). See :meth:`AttendanceResource.list_holiday_calendars`."""
        params = _build_holiday_calendars_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/holidayscalendar", params=params)

    async def list_holidays(
        self,
        calendar_id: str,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all holidays for a calendar (paginated). See :meth:`AttendanceResource.list_holidays`."""
        params = _build_holidays_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(
            f"time/holidayscalendar/{calendar_id}/holidays", params=params
        )

    async def create_time_entry_for_employee(
        self,
        employee_id: str,
        timestamp: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a time entry for a specific employee. See :meth:`AttendanceResource.create_time_entry_for_employee`."""
        body = _build_time_entry_body(
            employee_id=employee_id,
            timestamp=timestamp,
            note=note,
        )
        return await self._post(
            f"attendance/employee/{employee_id}/timeentry", json=body
        )

    async def create_time_entry(
        self,
        employee_id: str,
        timestamp: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a time entry (employee ID in body). See :meth:`AttendanceResource.create_time_entry`."""
        body = _build_time_entry_body(
            employee_id=employee_id,
            timestamp=timestamp,
            note=note,
        )
        return await self._post("attendance/employee/timeentry", json=body)

    async def list_on_duty_requests(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all on-duty requests (paginated). See :meth:`AttendanceResource.list_on_duty_requests`."""
        params = _build_on_duty_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/od", params=params)

    async def create_on_duty_request(
        self,
        employee_id: str,
        from_date: str,
        to_date: str,
        from_session: Optional[SessionType] = None,
        to_session: Optional[SessionType] = None,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an on-duty request. See :meth:`AttendanceResource.create_on_duty_request`."""
        body = _build_on_duty_body(
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
            from_session=from_session,
            to_session=to_session,
            note=note,
        )
        return await self._post("time/od", json=body)

    async def list_wfh_requests(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all WFH requests (paginated). See :meth:`AttendanceResource.list_wfh_requests`."""
        params = _build_wfh_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate("time/wfh", params=params)

    async def create_wfh_request(
        self,
        employee_id: str,
        from_date: str,
        to_date: str,
        from_session: Optional[SessionType] = None,
        to_session: Optional[SessionType] = None,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a WFH request. See :meth:`AttendanceResource.create_wfh_request`."""
        body = _build_wfh_body(
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
            from_session=from_session,
            to_session=to_session,
            note=note,
        )
        return await self._post("time/wfh", json=body)

    async def update_approval_status(
        self,
        request_id: str,
        request_type: str,
        status: ApprovalStatusEnum,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update approval status. See :meth:`AttendanceResource.update_approval_status`."""
        if request_type not in ("od", "wfh"):
            raise ValueError(
                f"request_type must be 'od' or 'wfh', got {request_type!r}"
            )
        body = _build_approval_status_body(status=status, note=note)
        return await self._put(
            f"time/{request_type}/{request_id}/status", json=body
        )
