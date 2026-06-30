from typing import Any, Dict, Optional

from ..types import (
    EmployeeSearchResponse,
    ExitTypeEnum,
    GenderType,
    MaritalStatusType,
)
from .base import AsyncBaseResource, BaseResource

_SEARCH_PATH = "hris/employees/search"
_JOB_DETAILS_PATH = "hris/employees/jobdetails"
_PERSONAL_DETAILS_PATH = "hris/employees/personaldetails"


def _build_search_body(work_email: Optional[str], work_phone: Optional[str]) -> Dict[str, str]:
    if not work_email and not work_phone:
        raise ValueError("At least one of work_email or work_phone must be provided")
    body: Dict[str, str] = {}
    if work_email:
        body["workEmail"] = work_email
    if work_phone:
        body["workPhone"] = work_phone
    return body


def _build_employee_list_params(
    employee_ids: Optional[str] = None,
    employee_numbers: Optional[str] = None,
    employment_status: Optional[str] = None,
    in_probation: Optional[bool] = None,
    in_notice_period: Optional[bool] = None,
    last_modified: Optional[str] = None,
    search_key: Optional[str] = None,
    page_number: Optional[int] = None,
    page_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Build query parameters for GET /hris/employees."""
    params: Dict[str, Any] = {
        "employeeIds": employee_ids,
        "employeeNumbers": employee_numbers,
        "employmentStatus": employment_status,
        "inProbation": in_probation,
        "inNoticePeriod": in_notice_period,
        "lastModified": last_modified,
        "searchKey": search_key,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    return {k: v for k, v in params.items() if v is not None}


def _build_create_employee_body(
    first_name: str,
    last_name: str,
    email: str,
    date_joined: str,
    employee_number: Optional[str] = None,
    display_name: Optional[str] = None,
    middle_name: Optional[str] = None,
    mobile_number: Optional[str] = None,
    gender: Optional[GenderType] = None,
    date_of_birth: Optional[str] = None,
    department: Optional[str] = None,
    business_unit: Optional[str] = None,
    job_title: Optional[str] = None,
    secondary_job_title: Optional[str] = None,
    location: Optional[str] = None,
    legal_entity: Optional[str] = None,
    nationality: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for POST /hris/employees."""
    body: Dict[str, Any] = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "dateJoined": date_joined,
    }
    if employee_number is not None:
        body["employeeNumber"] = employee_number
    if display_name is not None:
        body["displayName"] = display_name
    if middle_name is not None:
        body["middleName"] = middle_name
    if mobile_number is not None:
        body["mobileNumber"] = mobile_number
    if gender is not None:
        body["gender"] = gender
    if date_of_birth is not None:
        body["dateOfBirth"] = date_of_birth
    if department is not None:
        body["department"] = department
    if business_unit is not None:
        body["businessUnit"] = business_unit
    if job_title is not None:
        body["jobTitle"] = job_title
    if secondary_job_title is not None:
        body["secondaryJobTitle"] = secondary_job_title
    if location is not None:
        body["location"] = location
    if legal_entity is not None:
        body["legalEntity"] = legal_entity
    if nationality is not None:
        body["nationality"] = nationality
    return body


def _build_job_details_body(
    employee_id: str,
    job_title_id: Optional[str] = None,
    department_id: Optional[str] = None,
    location_id: Optional[str] = None,
    business_unit_id: Optional[str] = None,
    reports_to_id: Optional[str] = None,
    effective_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for PUT /hris/employees/jobdetails."""
    body: Dict[str, Any] = {"employeeId": employee_id}
    if job_title_id is not None:
        body["jobTitleId"] = job_title_id
    if department_id is not None:
        body["departmentId"] = department_id
    if location_id is not None:
        body["locationId"] = location_id
    if business_unit_id is not None:
        body["businessUnitId"] = business_unit_id
    if reports_to_id is not None:
        body["reportsToId"] = reports_to_id
    if effective_date is not None:
        body["effectiveDate"] = effective_date
    return body


def _build_personal_details_body(
    employee_id: str,
    first_name: Optional[str] = None,
    middle_name: Optional[str] = None,
    last_name: Optional[str] = None,
    display_name: Optional[str] = None,
    date_of_birth: Optional[str] = None,
    gender: Optional[GenderType] = None,
    marital_status: Optional[MaritalStatusType] = None,
    mobile_phone: Optional[str] = None,
    personal_email: Optional[str] = None,
    nationality: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for PUT /hris/employees/personaldetails."""
    body: Dict[str, Any] = {"employeeId": employee_id}
    if first_name is not None:
        body["firstName"] = first_name
    if middle_name is not None:
        body["middleName"] = middle_name
    if last_name is not None:
        body["lastName"] = last_name
    if display_name is not None:
        body["displayName"] = display_name
    if date_of_birth is not None:
        body["dateOfBirth"] = date_of_birth
    if gender is not None:
        body["gender"] = gender
    if marital_status is not None:
        body["maritalStatus"] = marital_status
    if mobile_phone is not None:
        body["mobilePhone"] = mobile_phone
    if personal_email is not None:
        body["personalEmail"] = personal_email
    if nationality is not None:
        body["nationality"] = nationality
    return body


def _build_exit_request_body(
    exit_type: ExitTypeEnum,
    resignation_date: str,
    exit_reason: Optional[str] = None,
    last_working_date: Optional[str] = None,
    is_ok_to_rehire: Optional[bool] = None,
    comments: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request body for POST/PUT /hris/employees/{id}/exitrequest."""
    body: Dict[str, Any] = {
        "exitType": exit_type,
        "resignationDate": resignation_date,
    }
    if exit_reason is not None:
        body["exitReason"] = exit_reason
    if last_working_date is not None:
        body["lastWorkingDate"] = last_working_date
    if is_ok_to_rehire is not None:
        body["isOkToRehire"] = is_ok_to_rehire
    if comments is not None:
        body["comments"] = comments
    return body


class HRResource(BaseResource):
    """Synchronous HR operations."""

    endpoint = "hris/employees"

    def list_employees(
        self,
        employee_ids: Optional[str] = None,
        employee_numbers: Optional[str] = None,
        employment_status: Optional[str] = None,
        in_probation: Optional[bool] = None,
        in_notice_period: Optional[bool] = None,
        last_modified: Optional[str] = None,
        search_key: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List employees (paginated).

        Args:
            employee_ids: Comma-separated list of employee IDs to filter.
            employee_numbers: Comma-separated list of employee numbers to filter.
            employment_status: Filter by status: "Working" or "Relieved".
            in_probation: Filter employees in probation period (True/False).
            in_notice_period: Filter employees in notice period (True/False).
            last_modified: Return records modified after this date (ISO 8601).
            search_key: Search keyword (minimum 3 characters).
            page_number: Page number (1-based).
            page_size: Results per page (default 100, max 200).

        Returns:
            Paginated response with employees data.
        """
        params = _build_employee_list_params(
            employee_ids=employee_ids,
            employee_numbers=employee_numbers,
            employment_status=employment_status,
            in_probation=in_probation,
            in_notice_period=in_notice_period,
            last_modified=last_modified,
            search_key=search_key,
            page_number=page_number,
            page_size=page_size,
        )
        return self._paginate(self.endpoint, params=params)

    def search_employee(
        self,
        work_email: Optional[str] = None,
        work_phone: Optional[str] = None,
    ) -> EmployeeSearchResponse:
        """
        Search for an employee by work email or work phone.

        At least one of ``work_email`` / ``work_phone`` is required.

        Reference: https://developers.keka.com/reference/post_hris-employees-search.md
        """
        body = _build_search_body(work_email, work_phone)
        return self._post(_SEARCH_PATH, json=body)  # type: ignore[return-value]

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get a single employee by ID."""
        return self._get(self._build_path(employee_id))

    def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_joined: str,
        employee_number: Optional[str] = None,
        display_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        mobile_number: Optional[str] = None,
        gender: Optional[GenderType] = None,
        date_of_birth: Optional[str] = None,
        department: Optional[str] = None,
        business_unit: Optional[str] = None,
        job_title: Optional[str] = None,
        secondary_job_title: Optional[str] = None,
        location: Optional[str] = None,
        legal_entity: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new employee.

        Args:
            first_name: Employee's first name (required).
            last_name: Employee's last name (required).
            email: Employee's work email (required).
            date_joined: Joining date in ISO 8601 format (required).
            employee_number: Unique employee number.
            display_name: Display name.
            middle_name: Middle name.
            mobile_number: Mobile phone number.
            gender: Gender (0=Male, 1=Female, 2=Other, 3=Not specified).
            date_of_birth: Date of birth in ISO 8601 format.
            department: Department ID.
            business_unit: Business unit ID.
            job_title: Job title ID.
            secondary_job_title: Secondary job title.
            location: Location ID.
            legal_entity: Legal entity ID.
            nationality: Nationality.

        Returns:
            Response with created employee ID.
        """
        body = _build_create_employee_body(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_joined=date_joined,
            employee_number=employee_number,
            display_name=display_name,
            middle_name=middle_name,
            mobile_number=mobile_number,
            gender=gender,
            date_of_birth=date_of_birth,
            department=department,
            business_unit=business_unit,
            job_title=job_title,
            secondary_job_title=secondary_job_title,
            location=location,
            legal_entity=legal_entity,
            nationality=nationality,
        )
        return self._post(self.endpoint, json=body)

    def update_job_details(
        self,
        employee_id: str,
        job_title_id: Optional[str] = None,
        department_id: Optional[str] = None,
        location_id: Optional[str] = None,
        business_unit_id: Optional[str] = None,
        reports_to_id: Optional[str] = None,
        effective_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update employee job details.

        Args:
            employee_id: Employee ID (required).
            job_title_id: New job title ID.
            department_id: New department ID.
            location_id: New location ID.
            business_unit_id: New business unit ID.
            reports_to_id: New reporting manager ID.
            effective_date: Effective date for changes (ISO 8601).

        Returns:
            Response indicating success/failure.
        """
        body = _build_job_details_body(
            employee_id=employee_id,
            job_title_id=job_title_id,
            department_id=department_id,
            location_id=location_id,
            business_unit_id=business_unit_id,
            reports_to_id=reports_to_id,
            effective_date=effective_date,
        )
        return self._put(_JOB_DETAILS_PATH, json=body)

    def update_personal_details(
        self,
        employee_id: str,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        display_name: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        gender: Optional[GenderType] = None,
        marital_status: Optional[MaritalStatusType] = None,
        mobile_phone: Optional[str] = None,
        personal_email: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update employee personal details.

        Args:
            employee_id: Employee ID (required).
            first_name: First name.
            middle_name: Middle name.
            last_name: Last name.
            display_name: Display name.
            date_of_birth: Date of birth (ISO 8601).
            gender: Gender (0=Male, 1=Female, 2=Other, 3=Not specified).
            marital_status: Marital status (0=Single, 1=Married, 2=Divorced).
            mobile_phone: Mobile phone number.
            personal_email: Personal email address.
            nationality: Nationality.

        Returns:
            Response indicating success/failure.
        """
        body = _build_personal_details_body(
            employee_id=employee_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            display_name=display_name,
            date_of_birth=date_of_birth,
            gender=gender,
            marital_status=marital_status,
            mobile_phone=mobile_phone,
            personal_email=personal_email,
            nationality=nationality,
        )
        return self._put(_PERSONAL_DETAILS_PATH, json=body)

    def deactivate_employee(
        self,
        employee_id: str,
        exit_type: ExitTypeEnum,
        resignation_date: str,
        exit_reason: Optional[str] = None,
        last_working_date: Optional[str] = None,
        is_ok_to_rehire: Optional[bool] = None,
        comments: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Deactivate an employee (initiate exit process).

        Args:
            employee_id: Employee ID (required).
            exit_type: Exit type (0=None, 1=Resignation, 2=Termination, 3=Other).
            resignation_date: Date resignation submitted (ISO 8601).
            exit_reason: Exit reason ID.
            last_working_date: Last working date (ISO 8601).
            is_ok_to_rehire: Whether employee is eligible for rehire.
            comments: Additional comments.

        Returns:
            Response indicating success/failure.
        """
        body = _build_exit_request_body(
            exit_type=exit_type,
            resignation_date=resignation_date,
            exit_reason=exit_reason,
            last_working_date=last_working_date,
            is_ok_to_rehire=is_ok_to_rehire,
            comments=comments,
        )
        path = f"{self.endpoint}/{employee_id}/exitrequest"
        return self._post(path, json=body)

    def update_exit_request(
        self,
        employee_id: str,
        exit_type: ExitTypeEnum,
        resignation_date: str,
        exit_reason: Optional[str] = None,
        last_working_date: Optional[str] = None,
        is_ok_to_rehire: Optional[bool] = None,
        comments: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing employee exit request.

        Args:
            employee_id: Employee ID (required).
            exit_type: Exit type (0=None, 1=Resignation, 2=Termination, 3=Other).
            resignation_date: Date resignation submitted (ISO 8601).
            exit_reason: Exit reason ID.
            last_working_date: Last working date (ISO 8601).
            is_ok_to_rehire: Whether employee is eligible for rehire.
            comments: Additional comments.

        Returns:
            Response indicating success/failure.
        """
        body = _build_exit_request_body(
            exit_type=exit_type,
            resignation_date=resignation_date,
            exit_reason=exit_reason,
            last_working_date=last_working_date,
            is_ok_to_rehire=is_ok_to_rehire,
            comments=comments,
        )
        path = f"{self.endpoint}/{employee_id}/exitrequest"
        return self._put(path, json=body)


class AsyncHRResource(AsyncBaseResource):
    """Asynchronous HR operations."""

    endpoint = "hris/employees"

    async def list_employees(
        self,
        employee_ids: Optional[str] = None,
        employee_numbers: Optional[str] = None,
        employment_status: Optional[str] = None,
        in_probation: Optional[bool] = None,
        in_notice_period: Optional[bool] = None,
        last_modified: Optional[str] = None,
        search_key: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List employees (paginated). See :meth:`HRResource.list_employees`."""
        params = _build_employee_list_params(
            employee_ids=employee_ids,
            employee_numbers=employee_numbers,
            employment_status=employment_status,
            in_probation=in_probation,
            in_notice_period=in_notice_period,
            last_modified=last_modified,
            search_key=search_key,
            page_number=page_number,
            page_size=page_size,
        )
        return await self._paginate(self.endpoint, params=params)

    async def search_employee(
        self,
        work_email: Optional[str] = None,
        work_phone: Optional[str] = None,
    ) -> EmployeeSearchResponse:
        """Search for an employee by work email or work phone."""
        body = _build_search_body(work_email, work_phone)
        return await self._post(_SEARCH_PATH, json=body)  # type: ignore[return-value]

    async def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get a single employee by ID."""
        return await self._get(self._build_path(employee_id))

    async def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_joined: str,
        employee_number: Optional[str] = None,
        display_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        mobile_number: Optional[str] = None,
        gender: Optional[GenderType] = None,
        date_of_birth: Optional[str] = None,
        department: Optional[str] = None,
        business_unit: Optional[str] = None,
        job_title: Optional[str] = None,
        secondary_job_title: Optional[str] = None,
        location: Optional[str] = None,
        legal_entity: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new employee. See :meth:`HRResource.create_employee`."""
        body = _build_create_employee_body(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_joined=date_joined,
            employee_number=employee_number,
            display_name=display_name,
            middle_name=middle_name,
            mobile_number=mobile_number,
            gender=gender,
            date_of_birth=date_of_birth,
            department=department,
            business_unit=business_unit,
            job_title=job_title,
            secondary_job_title=secondary_job_title,
            location=location,
            legal_entity=legal_entity,
            nationality=nationality,
        )
        return await self._post(self.endpoint, json=body)

    async def update_job_details(
        self,
        employee_id: str,
        job_title_id: Optional[str] = None,
        department_id: Optional[str] = None,
        location_id: Optional[str] = None,
        business_unit_id: Optional[str] = None,
        reports_to_id: Optional[str] = None,
        effective_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update employee job details. See :meth:`HRResource.update_job_details`."""
        body = _build_job_details_body(
            employee_id=employee_id,
            job_title_id=job_title_id,
            department_id=department_id,
            location_id=location_id,
            business_unit_id=business_unit_id,
            reports_to_id=reports_to_id,
            effective_date=effective_date,
        )
        return await self._put(_JOB_DETAILS_PATH, json=body)

    async def update_personal_details(
        self,
        employee_id: str,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        display_name: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        gender: Optional[GenderType] = None,
        marital_status: Optional[MaritalStatusType] = None,
        mobile_phone: Optional[str] = None,
        personal_email: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update employee personal details. See :meth:`HRResource.update_personal_details`."""
        body = _build_personal_details_body(
            employee_id=employee_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            display_name=display_name,
            date_of_birth=date_of_birth,
            gender=gender,
            marital_status=marital_status,
            mobile_phone=mobile_phone,
            personal_email=personal_email,
            nationality=nationality,
        )
        return await self._put(_PERSONAL_DETAILS_PATH, json=body)

    async def deactivate_employee(
        self,
        employee_id: str,
        exit_type: ExitTypeEnum,
        resignation_date: str,
        exit_reason: Optional[str] = None,
        last_working_date: Optional[str] = None,
        is_ok_to_rehire: Optional[bool] = None,
        comments: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Deactivate an employee. See :meth:`HRResource.deactivate_employee`."""
        body = _build_exit_request_body(
            exit_type=exit_type,
            resignation_date=resignation_date,
            exit_reason=exit_reason,
            last_working_date=last_working_date,
            is_ok_to_rehire=is_ok_to_rehire,
            comments=comments,
        )
        path = f"{self.endpoint}/{employee_id}/exitrequest"
        return await self._post(path, json=body)

    async def update_exit_request(
        self,
        employee_id: str,
        exit_type: ExitTypeEnum,
        resignation_date: str,
        exit_reason: Optional[str] = None,
        last_working_date: Optional[str] = None,
        is_ok_to_rehire: Optional[bool] = None,
        comments: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing employee exit request. See :meth:`HRResource.update_exit_request`."""
        body = _build_exit_request_body(
            exit_type=exit_type,
            resignation_date=resignation_date,
            exit_reason=exit_reason,
            last_working_date=last_working_date,
            is_ok_to_rehire=is_ok_to_rehire,
            comments=comments,
        )
        path = f"{self.endpoint}/{employee_id}/exitrequest"
        return await self._put(path, json=body)
