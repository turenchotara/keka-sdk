"""
Keka HR Module

This module provides HR-related operations for the Keka SDK including
Employee, Job Title, and Department management.
"""

import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

from .client import ApiClient, AsyncApiClient
from .utils.helpers import get_auth_headers

logger = logging.getLogger(__name__)


class EmployeeManager:
    """Manages employee-related operations in Keka HR."""

    def __init__(self, client: Union[ApiClient, AsyncApiClient], base_url: str):
        """
        Initialize the Employee Manager.

        Args:
            client: API client instance (sync or async)
            base_url: Base URL for the API
        """
        self.client = client
        self.base_url = base_url.rstrip('/')
        self.endpoint = '/api/v1/employees'

    def _build_url(self, path: str = '') -> str:
        """Build full URL for employee endpoints."""
        return urljoin(self.base_url + '/', self.endpoint + path)

    def get_employees(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None,
        department_id: Optional[str] = None,
        job_title_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of employees with optional filtering.

        Args:
            page: Page number for pagination
            page_size: Number of items per page
            search: Search term for employee name or email
            department_id: Filter by department ID
            job_title_id: Filter by job title ID
            status: Filter by employee status (active, inactive, etc.)

        Returns:
            Dictionary containing employee data
        """
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if search:
            params['search'] = search
        if department_id:
            params['departmentId'] = department_id
        if job_title_id:
            params['jobTitleId'] = job_title_id
        if status:
            params['status'] = status

        response = self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """
        Get employee details by ID.

        Args:
            employee_id: Unique identifier for the employee

        Returns:
            Dictionary containing employee details
        """
        endpoint = f"{self.endpoint}/{employee_id}"
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new employee.

        Args:
            employee_data: Dictionary containing employee information
                Required fields: firstName, lastName, email
                Optional fields: departmentId, jobTitleId, employeeId, etc.

        Returns:
            Dictionary containing created employee data
        """
        response = self.client.post(self.endpoint, data=employee_data)
        response.raise_for_status()
        return response.json()

    def update_employee(
        self,
        employee_id: str,
        employee_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update employee information.

        Args:
            employee_id: Unique identifier for the employee
            employee_data: Dictionary containing updated employee information

        Returns:
            Dictionary containing updated employee data
        """
        endpoint = f"{self.endpoint}/{employee_id}"
        response = self.client.put(endpoint, data=employee_data)
        response.raise_for_status()
        return response.json()

    def delete_employee(self, employee_id: str) -> bool:
        """
        Delete an employee.

        Args:
            employee_id: Unique identifier for the employee

        Returns:
            True if deletion was successful
        """
        endpoint = f"{self.endpoint}/{employee_id}"
        response = self.client.delete(endpoint)
        response.raise_for_status()
        return True

    def get_employee_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get employee by email address.

        Args:
            email: Employee email address

        Returns:
            Dictionary containing employee details or None if not found
        """
        params = {'search': email}
        response = self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Find employee with exact email match
        employees = data.get('employees', [])
        for employee in employees:
            if employee.get('email', '').lower() == email.lower():
                return employee
        return None


class JobTitleManager:
    """Manages job title-related operations in Keka HR."""

    def __init__(self, client: Union[ApiClient, AsyncApiClient], base_url: str):
        """
        Initialize the Job Title Manager.

        Args:
            client: API client instance (sync or async)
            base_url: Base URL for the API
        """
        self.client = client
        self.base_url = base_url.rstrip('/')
        self.endpoint = '/api/v1/jobtitles'

    def get_job_titles(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of job titles with optional filtering.

        Args:
            page: Page number for pagination
            page_size: Number of items per page
            search: Search term for job title name

        Returns:
            Dictionary containing job title data
        """
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if search:
            params['search'] = search

        response = self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_job_title(self, job_title_id: str) -> Dict[str, Any]:
        """
        Get job title details by ID.

        Args:
            job_title_id: Unique identifier for the job title

        Returns:
            Dictionary containing job title details
        """
        endpoint = f"{self.endpoint}/{job_title_id}"
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    def create_job_title(self, job_title_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new job title.

        Args:
            job_title_data: Dictionary containing job title information
                Required fields: name
                Optional fields: description, departmentId, etc.

        Returns:
            Dictionary containing created job title data
        """
        response = self.client.post(self.endpoint, data=job_title_data)
        response.raise_for_status()
        return response.json()

    def update_job_title(
        self,
        job_title_id: str,
        job_title_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update job title information.

        Args:
            job_title_id: Unique identifier for the job title
            job_title_data: Dictionary containing updated job title information

        Returns:
            Dictionary containing updated job title data
        """
        endpoint = f"{self.endpoint}/{job_title_id}"
        response = self.client.put(endpoint, data=job_title_data)
        response.raise_for_status()
        return response.json()

    def delete_job_title(self, job_title_id: str) -> bool:
        """
        Delete a job title.

        Args:
            job_title_id: Unique identifier for the job title

        Returns:
            True if deletion was successful
        """
        endpoint = f"{self.endpoint}/{job_title_id}"
        response = self.client.delete(endpoint)
        response.raise_for_status()
        return True


class DepartmentManager:
    """Manages department-related operations in Keka HR."""

    def __init__(self, client: Union[ApiClient, AsyncApiClient], base_url: str):
        """
        Initialize the Department Manager.

        Args:
            client: API client instance (sync or async)
            base_url: Base URL for the API
        """
        self.client = client
        self.base_url = base_url.rstrip('/')
        self.endpoint = '/api/v1/departments'

    def get_departments(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of departments with optional filtering.

        Args:
            page: Page number for pagination
            page_size: Number of items per page
            search: Search term for department name

        Returns:
            Dictionary containing department data
        """
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if search:
            params['search'] = search

        response = self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_department(self, department_id: str) -> Dict[str, Any]:
        """
        Get department details by ID.

        Args:
            department_id: Unique identifier for the department

        Returns:
            Dictionary containing department details
        """
        endpoint = f"{self.endpoint}/{department_id}"
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    def create_department(self, department_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new department.

        Args:
            department_data: Dictionary containing department information
                Required fields: name
                Optional fields: description, parentDepartmentId, etc.

        Returns:
            Dictionary containing created department data
        """
        response = self.client.post(self.endpoint, data=department_data)
        response.raise_for_status()
        return response.json()

    def update_department(
        self,
        department_id: str,
        department_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update department information.

        Args:
            department_id: Unique identifier for the department
            department_data: Dictionary containing updated department information

        Returns:
            Dictionary containing updated department data
        """
        endpoint = f"{self.endpoint}/{department_id}"
        response = self.client.put(endpoint, data=department_data)
        response.raise_for_status()
        return response.json()

    def delete_department(self, department_id: str) -> bool:
        """
        Delete a department.

        Args:
            department_id: Unique identifier for the department

        Returns:
            True if deletion was successful
        """
        endpoint = f"{self.endpoint}/{department_id}"
        response = self.client.delete(endpoint)
        response.raise_for_status()
        return True

    def get_department_employees(
        self,
        department_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get employees in a specific department.

        Args:
            department_id: Unique identifier for the department
            page: Page number for pagination
            page_size: Number of items per page

        Returns:
            Dictionary containing employee data for the department
        """
        endpoint = f"{self.endpoint}/{department_id}/employees"
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        response = self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()


class HRClient:
    """
    Main HR client that provides access to all HR-related operations.
    
    This client combines Employee, Job Title, and Department management
    into a single interface for easy access to all HR functionality.
    """

    def __init__(
        self,
        client: Union[ApiClient, AsyncApiClient],
        base_url: str,
        auth_token: Optional[str] = None
    ):
        """
        Initialize the HR Client.

        Args:
            client: API client instance (sync or async)
            base_url: Base URL for the API
            auth_token: Authentication token for API requests
        """
        self.client = client
        self.base_url = base_url
        self.auth_token = auth_token
        
        # Initialize managers
        self.employees = EmployeeManager(client, base_url)
        self.job_titles = JobTitleManager(client, base_url)
        self.departments = DepartmentManager(client, base_url)

    def set_auth_token(self, token: str) -> None:
        """
        Set or update the authentication token.

        Args:
            token: New authentication token
        """
        self.auth_token = token
        # Update client headers with new token
        if hasattr(self.client, 'headers'):
            self.client.headers.update(get_auth_headers(token))

    def get_organization_structure(self) -> Dict[str, Any]:
        """
        Get complete organization structure including departments and job titles.

        Returns:
            Dictionary containing organization structure data
        """
        try:
            departments = self.departments.get_departments()
            job_titles = self.job_titles.get_job_titles()
            
            return {
                'departments': departments,
                'job_titles': job_titles,
                'timestamp': self._get_current_timestamp()
            }
        except Exception as e:
            logger.error(f"Error fetching organization structure: {e}")
            raise

    def get_employee_summary(self, employee_id: str) -> Dict[str, Any]:
        """
        Get comprehensive employee information including department and job title.

        Args:
            employee_id: Unique identifier for the employee

        Returns:
            Dictionary containing comprehensive employee information
        """
        try:
            employee = self.employees.get_employee(employee_id)
            
            # Get additional details if available
            department_info = None
            job_title_info = None
            
            if employee.get('departmentId'):
                try:
                    department_info = self.departments.get_department(
                        employee['departmentId']
                    )
                except Exception as e:
                    logger.warning(f"Could not fetch department info: {e}")
            
            if employee.get('jobTitleId'):
                try:
                    job_title_info = self.job_titles.get_job_title(
                        employee['jobTitleId']
                    )
                except Exception as e:
                    logger.warning(f"Could not fetch job title info: {e}")
            
            return {
                'employee': employee,
                'department': department_info,
                'job_title': job_title_info,
                'timestamp': self._get_current_timestamp()
            }
        except Exception as e:
            logger.error(f"Error fetching employee summary: {e}")
            raise

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


# Async versions of the managers for async operations
class AsyncEmployeeManager(EmployeeManager):
    """Async version of Employee Manager."""

    async def get_employees(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None,
        department_id: Optional[str] = None,
        job_title_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Async version of get_employees."""
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if search:
            params['search'] = search
        if department_id:
            params['departmentId'] = department_id
        if job_title_id:
            params['jobTitleId'] = job_title_id
        if status:
            params['status'] = status

        response = await self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Async version of get_employee."""
        endpoint = f"{self.endpoint}/{employee_id}"
        response = await self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    async def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async version of create_employee."""
        response = await self.client.post(self.endpoint, data=employee_data)
        response.raise_for_status()
        return response.json()

    async def update_employee(
        self,
        employee_id: str,
        employee_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Async version of update_employee."""
        endpoint = f"{self.endpoint}/{employee_id}"
        response = await self.client.put(endpoint, data=employee_data)
        response.raise_for_status()
        return response.json()

    async def delete_employee(self, employee_id: str) -> bool:
        """Async version of delete_employee."""
        endpoint = f"{self.endpoint}/{employee_id}"
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return True

    async def get_employee_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Async version of get_employee_by_email."""
        params = {'search': email}
        response = await self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        
        employees = data.get('employees', [])
        for employee in employees:
            if employee.get('email', '').lower() == email.lower():
                return employee
        return None


class AsyncJobTitleManager(JobTitleManager):
    """Async version of Job Title Manager."""

    async def get_job_titles(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Async version of get_job_titles."""
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if search:
            params['search'] = search

        response = await self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def get_job_title(self, job_title_id: str) -> Dict[str, Any]:
        """Async version of get_job_title."""
        endpoint = f"{self.endpoint}/{job_title_id}"
        response = await self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    async def create_job_title(self, job_title_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async version of create_job_title."""
        response = await self.client.post(self.endpoint, data=job_title_data)
        response.raise_for_status()
        return response.json()

    async def update_job_title(
        self,
        job_title_id: str,
        job_title_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Async version of update_job_title."""
        endpoint = f"{self.endpoint}/{job_title_id}"
        response = await self.client.put(endpoint, data=job_title_data)
        response.raise_for_status()
        return response.json()

    async def delete_job_title(self, job_title_id: str) -> bool:
        """Async version of delete_job_title."""
        endpoint = f"{self.endpoint}/{job_title_id}"
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return True


class AsyncDepartmentManager(DepartmentManager):
    """Async version of Department Manager."""

    async def get_departments(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Async version of get_departments."""
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if search:
            params['search'] = search

        response = await self.client.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def get_department(self, department_id: str) -> Dict[str, Any]:
        """Async version of get_department."""
        endpoint = f"{self.endpoint}/{department_id}"
        response = await self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    async def create_department(self, department_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async version of create_department."""
        response = await self.client.post(self.endpoint, data=department_data)
        response.raise_for_status()
        return response.json()

    async def update_department(
        self,
        department_id: str,
        department_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Async version of update_department."""
        endpoint = f"{self.endpoint}/{department_id}"
        response = await self.client.put(endpoint, data=department_data)
        response.raise_for_status()
        return response.json()

    async def delete_department(self, department_id: str) -> bool:
        """Async version of delete_department."""
        endpoint = f"{self.endpoint}/{department_id}"
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return True

    async def get_department_employees(
        self,
        department_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """Async version of get_department_employees."""
        endpoint = f"{self.endpoint}/{department_id}/employees"
        params = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()


class AsyncHRClient(HRClient):
    """Async version of HR Client."""

    def __init__(
        self,
        client: AsyncApiClient,
        base_url: str,
        auth_token: Optional[str] = None
    ):
        """
        Initialize the Async HR Client.

        Args:
            client: Async API client instance
            base_url: Base URL for the API
            auth_token: Authentication token for API requests
        """
        super().__init__(client, base_url, auth_token)
        
        # Initialize async managers
        self.employees = AsyncEmployeeManager(client, base_url)
        self.job_titles = AsyncJobTitleManager(client, base_url)
        self.departments = AsyncDepartmentManager(client, base_url)

    async def get_organization_structure(self) -> Dict[str, Any]:
        """Async version of get_organization_structure."""
        try:
            departments = await self.departments.get_departments()
            job_titles = await self.job_titles.get_job_titles()
            
            return {
                'departments': departments,
                'job_titles': job_titles,
                'timestamp': self._get_current_timestamp()
            }
        except Exception as e:
            logger.error(f"Error fetching organization structure: {e}")
            raise

    async def get_employee_summary(self, employee_id: str) -> Dict[str, Any]:
        """Async version of get_employee_summary."""
        try:
            employee = await self.employees.get_employee(employee_id)
            
            department_info = None
            job_title_info = None
            
            if employee.get('departmentId'):
                try:
                    department_info = await self.departments.get_department(
                        employee['departmentId']
                    )
                except Exception as e:
                    logger.warning(f"Could not fetch department info: {e}")
            
            if employee.get('jobTitleId'):
                try:
                    job_title_info = await self.job_titles.get_job_title(
                        employee['jobTitleId']
                    )
                except Exception as e:
                    logger.warning(f"Could not fetch job title info: {e}")
            
            return {
                'employee': employee,
                'department': department_info,
                'job_title': job_title_info,
                'timestamp': self._get_current_timestamp()
            }
        except Exception as e:
            logger.error(f"Error fetching employee summary: {e}")
            raise
