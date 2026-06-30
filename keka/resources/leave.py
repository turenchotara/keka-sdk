from typing import Any, Dict, Optional

from ..types import SessionType
from .base import AsyncBaseResource, BaseResource


# =============================================================================
# PARAMETER BUILDERS
# =============================================================================

def _build_leave_balance_params(
    employee_ids: Optional[str] = None,
    leave_type_ids: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/leavebalance."""
    params: Dict[str, Any] = {
        "employeeIds": employee_ids,
        "leaveTypeIds": leave_type_ids,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_leave_plans_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/leaveplans."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_leave_requests_params(
    employee_ids: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/leaverequests."""
    params: Dict[str, Any] = {
        "employeeIds": employee_ids,
        "from": from_date,
        "to": to_date,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_leave_types_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /time/leavetypes."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_leave_request_body(
    employee_id: str,
    leave_type_id: str,
    from_date: str,
    to_date: str,
    from_session: Optional[SessionType] = None,
    to_session: Optional[SessionType] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for POST /time/leaverequests."""
    body: Dict[str, Any] = {
        "employeeId": employee_id,
        "leaveTypeId": leave_type_id,
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


# =============================================================================
# LEAVE RESOURCE
# =============================================================================

class LeaveResource(BaseResource):
    """Synchronous Leave resource for leave management operations."""

    endpoint = "time"

    def list_balances(
        self,
        employee_ids: Optional[str] = None,
        leave_type_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all leave balances (paginated).

        Args:
            employee_ids: Comma-separated list of employee IDs to filter.
            leave_type_ids: Comma-separated list of leave type IDs to filter.
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with employee leave balances.
        """
        params = _build_leave_balance_params(
            employee_ids=employee_ids,
            leave_type_ids=leave_type_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(f"{self.endpoint}/leavebalance", params=params)

    def list_plans(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all leave plans (paginated).

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with leave plans.
        """
        params = _build_leave_plans_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(f"{self.endpoint}/leaveplans", params=params)

    def list_requests(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all leave requests (paginated).

        Gets all leaves in the organization between from and to date.
        If both from and to are not specified, last 30 days records are returned.
        The difference between from and to date cannot be more than 90 days.

        Args:
            employee_ids: Comma-separated list of employee IDs to filter.
            from_date: Start date (ISO 8601 format).
            to_date: End date (ISO 8601 format, max 90 days from from_date).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with leave requests.
        """
        params = _build_leave_requests_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(f"{self.endpoint}/leaverequests", params=params)

    def create_request(
        self,
        employee_id: str,
        leave_type_id: str,
        from_date: str,
        to_date: str,
        from_session: Optional[SessionType] = None,
        to_session: Optional[SessionType] = None,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new leave request.

        Args:
            employee_id: Employee ID for whom leave is being requested.
            leave_type_id: Leave type ID.
            from_date: Leave start date (ISO 8601 format).
            to_date: Leave end date (ISO 8601 format).
            from_session: Start session (0=FirstHalf, 1=SecondHalf).
            to_session: End session (0=FirstHalf, 1=SecondHalf).
            note: Optional note/reason for leave.

        Returns:
            Response with created leave request ID.
        """
        body = _build_leave_request_body(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            from_date=from_date,
            to_date=to_date,
            from_session=from_session,
            to_session=to_session,
            note=note,
        )
        return self._post(f"{self.endpoint}/leaverequests", json=body)

    def list_types(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all leave types (paginated).

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with leave types.
        """
        params = _build_leave_types_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(f"{self.endpoint}/leavetypes", params=params)


class AsyncLeaveResource(AsyncBaseResource):
    """Asynchronous Leave resource for leave management operations."""

    endpoint = "time"

    async def list_balances(
        self,
        employee_ids: Optional[str] = None,
        leave_type_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all leave balances (paginated). See :meth:`LeaveResource.list_balances`."""
        params = _build_leave_balance_params(
            employee_ids=employee_ids,
            leave_type_ids=leave_type_ids,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(f"{self.endpoint}/leavebalance", params=params)

    async def list_plans(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all leave plans (paginated). See :meth:`LeaveResource.list_plans`."""
        params = _build_leave_plans_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(f"{self.endpoint}/leaveplans", params=params)

    async def list_requests(
        self,
        employee_ids: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all leave requests (paginated). See :meth:`LeaveResource.list_requests`."""
        params = _build_leave_requests_params(
            employee_ids=employee_ids,
            from_date=from_date,
            to_date=to_date,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(f"{self.endpoint}/leaverequests", params=params)

    async def create_request(
        self,
        employee_id: str,
        leave_type_id: str,
        from_date: str,
        to_date: str,
        from_session: Optional[SessionType] = None,
        to_session: Optional[SessionType] = None,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new leave request. See :meth:`LeaveResource.create_request`."""
        body = _build_leave_request_body(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            from_date=from_date,
            to_date=to_date,
            from_session=from_session,
            to_session=to_session,
            note=note,
        )
        return await self._post(f"{self.endpoint}/leaverequests", json=body)

    async def list_types(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all leave types (paginated). See :meth:`LeaveResource.list_types`."""
        params = _build_leave_types_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(f"{self.endpoint}/leavetypes", params=params)
