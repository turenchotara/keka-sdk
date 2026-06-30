from typing import Any, Dict, Optional

from ..types import EmployeeSearchResponse, TicketPriorityEnum, TicketStatusEnum
from .base import AsyncBaseResource, BaseResource
from .hr import _build_search_body

_SEARCH_PATH = "hris/employees/search"
_CATEGORIES_PATH = "helpdesk/ticket/categories"
_CLOSING_REASONS_PATH = "helpdesk/ticket/closingreasons"


def _build_ticket_params(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to_ids: Optional[str] = None,
    last_modified: Optional[str] = None,
    category_ids: Optional[str] = None,
    employee_ids: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
    **extra_params: Any,
) -> Dict[str, Any]:
    """
    Build the query-parameter mapping for the Get-All-Helpdesk-Tickets endpoint.

    Maps the SDK's snake_case arguments to the camelCase names expected by the
    Keka API. ``None`` values are omitted. Reference:
    https://developers.keka.com/reference/get_helpdesk-tickets
    """
    params: Dict[str, Any] = {
        "status": status,
        "priority": priority,
        "assignedToIds": assigned_to_ids,
        "lastModified": last_modified,
        "categoryIds": category_ids,
        "employeeIds": employee_ids,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    params.update(extra_params)
    return {k: v for k, v in params.items() if v is not None}


def _build_pagination_params(
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build pagination parameters."""
    params: Dict[str, Any] = {
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_create_ticket_body(
    title: str,
    category_id: str,
    description: Optional[str] = None,
    priority: Optional[TicketPriorityEnum] = None,
    employee_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for POST /helpdesk/tickets."""
    body: Dict[str, Any] = {
        "title": title,
        "categoryId": category_id,
    }
    if description is not None:
        body["description"] = description
    if priority is not None:
        body["priority"] = priority
    if employee_id is not None:
        body["employeeId"] = employee_id
    return body


def _build_update_ticket_body(
    status: Optional[TicketStatusEnum] = None,
    priority: Optional[TicketPriorityEnum] = None,
    assigned_to_id: Optional[str] = None,
    closing_reason: Optional[str] = None,
    comments: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for PUT /helpdesk/tickets/{ticketId}."""
    body: Dict[str, Any] = {}
    if status is not None:
        body["status"] = status
    if priority is not None:
        body["priority"] = priority
    if assigned_to_id is not None:
        body["assignedToId"] = assigned_to_id
    if closing_reason is not None:
        body["closingReason"] = closing_reason
    if comments is not None:
        body["comments"] = comments
    return body


class HelpdeskResource(BaseResource):
    """Synchronous helpdesk/ticket operations."""

    endpoint = "helpdesk/tickets"

    def list_tickets(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to_ids: Optional[str] = None,
        last_modified: Optional[str] = None,
        category_ids: Optional[str] = None,
        employee_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        **extra_params: Any,
    ) -> Dict[str, Any]:
        """
        List helpdesk tickets (paginated).

        Args:
            status: Filter by ticket status.
            priority: Filter by ticket priority.
            assigned_to_ids: Comma-separated assignee IDs.
            last_modified: ISO-8601 timestamp; return tickets modified after it.
            category_ids: Comma-separated category IDs.
            employee_ids: Comma-separated employee IDs.
            page_number: 1-based page number.
            page_size: Results per page (Keka default 100, max 200).
            **extra_params: Any additional query parameters to forward as-is.

        Reference: https://developers.keka.com/reference/get_helpdesk-tickets
        """
        params = _build_ticket_params(
            status=status,
            priority=priority,
            assigned_to_ids=assigned_to_ids,
            last_modified=last_modified,
            category_ids=category_ids,
            employee_ids=employee_ids,
            page_number=page_number,
            page_size=page_size,
            **extra_params,
        )
        return self._paginate(self.endpoint, params=params)

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Get a single ticket by ID."""
        return self._get(self._build_path(ticket_id))

    def search_employee_for_ticket(
        self,
        work_email: Optional[str] = None,
        work_phone: Optional[str] = None,
    ) -> EmployeeSearchResponse:
        """Find an employee (by email/phone) to associate with a ticket."""
        body = _build_search_body(work_email, work_phone)
        return self._post(_SEARCH_PATH, json=body)  # type: ignore[return-value]

    def create_ticket(
        self,
        title: str,
        category_id: str,
        description: Optional[str] = None,
        priority: Optional[TicketPriorityEnum] = None,
        employee_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new helpdesk ticket.

        Args:
            title: Ticket title (required).
            category_id: Category ID (required).
            description: Ticket description.
            priority: Priority (0=Low, 1=Medium, 2=High, 3=Critical).
            employee_id: Employee ID raising the ticket.

        Returns:
            Response with created ticket ID.
        """
        body = _build_create_ticket_body(
            title=title,
            category_id=category_id,
            description=description,
            priority=priority,
            employee_id=employee_id,
        )
        return self._post(self.endpoint, json=body)

    def update_ticket(
        self,
        ticket_id: str,
        status: Optional[TicketStatusEnum] = None,
        priority: Optional[TicketPriorityEnum] = None,
        assigned_to_id: Optional[str] = None,
        closing_reason: Optional[str] = None,
        comments: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing helpdesk ticket.

        Args:
            ticket_id: Ticket ID (required).
            status: New status (0=Open, 1=Pending, 2=Resolved, 3=Closed, 4=InProgress, 5=OnHold).
            priority: New priority (0=Low, 1=Medium, 2=High, 3=Critical).
            assigned_to_id: Assignee ID.
            closing_reason: Reason for closing the ticket.
            comments: Update comments.

        Returns:
            Response indicating success/failure.
        """
        body = _build_update_ticket_body(
            status=status,
            priority=priority,
            assigned_to_id=assigned_to_id,
            closing_reason=closing_reason,
            comments=comments,
        )
        path = f"{self.endpoint}/{ticket_id}"
        return self._put(path, json=body)

    def list_categories(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all helpdesk ticket categories (paginated).

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with ticket categories.
        """
        params = _build_pagination_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(_CATEGORIES_PATH, params=params)

    def list_closing_reasons(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all helpdesk ticket closing reasons (paginated).

        Args:
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with ticket closing reasons.
        """
        params = _build_pagination_params(
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(_CLOSING_REASONS_PATH, params=params)


class AsyncHelpdeskResource(AsyncBaseResource):
    """Asynchronous helpdesk/ticket operations."""

    endpoint = "helpdesk/tickets"

    async def list_tickets(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to_ids: Optional[str] = None,
        last_modified: Optional[str] = None,
        category_ids: Optional[str] = None,
        employee_ids: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        **extra_params: Any,
    ) -> Dict[str, Any]:
        """
        List helpdesk tickets (paginated). See
        :meth:`HelpdeskResource.list_tickets` for the parameter reference.
        """
        params = _build_ticket_params(
            status=status,
            priority=priority,
            assigned_to_ids=assigned_to_ids,
            last_modified=last_modified,
            category_ids=category_ids,
            employee_ids=employee_ids,
            page_number=page_number,
            page_size=page_size,
            **extra_params,
        )
        return await self._paginate(self.endpoint, params=params)

    async def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Get a single ticket by ID."""
        return await self._get(self._build_path(ticket_id))

    async def search_employee_for_ticket(
        self,
        work_email: Optional[str] = None,
        work_phone: Optional[str] = None,
    ) -> EmployeeSearchResponse:
        """Find an employee (by email/phone) to associate with a ticket."""
        body = _build_search_body(work_email, work_phone)
        return await self._post(_SEARCH_PATH, json=body)  # type: ignore[return-value]

    async def create_ticket(
        self,
        title: str,
        category_id: str,
        description: Optional[str] = None,
        priority: Optional[TicketPriorityEnum] = None,
        employee_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new helpdesk ticket. See :meth:`HelpdeskResource.create_ticket`."""
        body = _build_create_ticket_body(
            title=title,
            category_id=category_id,
            description=description,
            priority=priority,
            employee_id=employee_id,
        )
        return await self._post(self.endpoint, json=body)

    async def update_ticket(
        self,
        ticket_id: str,
        status: Optional[TicketStatusEnum] = None,
        priority: Optional[TicketPriorityEnum] = None,
        assigned_to_id: Optional[str] = None,
        closing_reason: Optional[str] = None,
        comments: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing helpdesk ticket. See :meth:`HelpdeskResource.update_ticket`."""
        body = _build_update_ticket_body(
            status=status,
            priority=priority,
            assigned_to_id=assigned_to_id,
            closing_reason=closing_reason,
            comments=comments,
        )
        path = f"{self.endpoint}/{ticket_id}"
        return await self._put(path, json=body)

    async def list_categories(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all helpdesk ticket categories. See :meth:`HelpdeskResource.list_categories`."""
        params = _build_pagination_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(_CATEGORIES_PATH, params=params)

    async def list_closing_reasons(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List all helpdesk ticket closing reasons. See :meth:`HelpdeskResource.list_closing_reasons`."""
        params = _build_pagination_params(
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(_CLOSING_REASONS_PATH, params=params)
