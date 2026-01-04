from typing import Optional, Union
from datetime import datetime

# Import all types from the centralized types module
from keka.src.resources.HR.types import (
    GenderType,
    EmployeeCreateResponse,
    EmployeeSearchResponse
)
from .... import KekaAuth
from ....client import ApiClient
from ....models import RemoveNone


class Employee(ApiClient):
    __endpoint = "hr/employees"

    def __init__(self, base_url: str, auth: KekaAuth):
        super().__init__(base_url)
        self._auth = auth

    def get_all_employees(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_employee_by_filter(
        self,
        id: Optional[str] = None,
        number: Optional[str] = None,
        # status: Optional[str] = None,
        # in_probation: bool = False,
        # in_notice_period: bool = False,
        # search_key: Optional[str] = None
    ):
        request_payload = {
            "id": id,
            "number": number
            # "status": status,
            # "in_probation": in_probation,
            # "in_notice_period": in_notice_period,
            # "search_key": search_key
        }
        payload = RemoveNone(**request_payload).model_dump(exclude_none=True)

        response = self.get(self.__endpoint, self._auth.headers, payload)
        return response.json()

    def search_employee(
        self,
        work_email: Optional[str] = None,
        work_phone: Optional[str] = None,
    ) -> EmployeeSearchResponse:
        """
        Search for an employee by work phone or email.
        
        Based on Keka API specification: https://developers.keka.com/reference/post_hris-employees-search.md
        
        Args:
            work_email (Optional[str]): Work email address to search for
            work_phone (Optional[str]): Work phone number to search for
            
        Note:
            At least one of work_email or work_phone must be provided.
            
        Returns:
            EmployeeSearchResponse: API response containing:
                - succeeded (bool): Whether the operation was successful
                - message (str): Response message
                - errors (List[str]): List of error messages if any
                - data (EmployeeProfile): Complete employee profile if found
                
        Raises:
            ValueError: If neither work_email nor work_phone is provided
            requests.RequestException: If API request fails
            
        Example:
            >>> employee = Employee()
            >>> response = employee.search_employee(work_email="john.doe@company.com")
            >>> if response["succeeded"] and response["data"]:
            ...     profile = response["data"]
            ...     print(f"Found employee: {profile['firstName']} {profile['lastName']}")
            ...     print(f"Employee ID: {profile['id']}")
            ...     print(f"Job Title: {profile['jobTitle']['title']}")
            
        API Response Examples:
            Success Response:
            {
                "succeeded": true,
                "message": "Employee found",
                "errors": null,
                "data": {
                    "id": "emp_12345",
                    "employeeNumber": "EMP001",
                    "firstName": "John",
                    "lastName": "Doe",
                    "displayName": "John Doe",
                    "email": "john.doe@personal.com",
                    "workPhone": "+1234567890",
                    "personalEmail": "john@personal.com",
                    "gender": 0,
                    "maritalStatus": 1,
                    "joiningDate": "2024-01-15T00:00:00Z",
                    "dateOfBirth": "1990-05-20T00:00:00Z",
                    "jobTitle": {
                        "identifier": "jt_001",
                        "title": "Software Engineer"
                    },
                    "reportsTo": {
                        "id": "emp_67890",
                        "firstName": "Jane",
                        "lastName": "Smith",
                        "email": "jane.smith@company.com"
                    },
                    "department": "Engineering",
                    "location": "New York",
                    "employmentStatus": 1,
                    "accountStatus": 1,
                    "isProfileComplete": true,
                    # ... many more fields available
                }
            }
            
            Employee Not Found Response:
            {
                "succeeded": false,
                "message": "Employee not found",
                "errors": ["No employee found with the provided criteria"],
                "data": null
            }
            
            Error Response:
            {
                "succeeded": false,
                "message": "Invalid request",
                "errors": ["Work email or work phone is required"],
                "data": null
            }
        """
        # This is a stub. Actual implementation should call the API endpoint.
        # POST /hris/employees/search
        # Validate input parameters
        if not work_email and not work_phone:
            raise ValueError("At least one of work_email or work_phone must be provided")

        endpoint = f"{self.__endpoint}/search"
        payload = RemoveNone(**{"workPhone": work_phone, "workEmail": work_email}).model_dump(exclude_none=True)
        response = self.post(endpoint, data=payload, headers=self._auth.headers)
        result = response.json()

        return result


    def get_employee_by_id(self, id: str):
        raise NotImplementedError("Subclasses must implement this method")

    def create(
        self,
        employee_number: Optional[str] = None,
        display_name: Optional[str] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        mobile_number: Optional[str] = None,
        gender: Optional[GenderType] = None,
        date_of_birth: Optional[Union[str, datetime]] = None,
        date_joined: Optional[Union[str, datetime]] = None,
        department: Optional[str] = None,
        business_unit: Optional[str] = None,
        job_title: Optional[str] = None,
        secondary_job_title: Optional[str] = None,
        location: Optional[str] = None,
        legal_entity: Optional[str] = None,
        nationality: Optional[str] = None,
    ) -> EmployeeCreateResponse:
        """
        Create a new employee in Keka HR system.
        
        Based on Keka API specification: https://developers.keka.com/reference/post_hris-employees.md

        Args:
            employee_number (Optional[str]): Employee number/ID
            display_name (Optional[str]): Display name for the employee
            first_name (Optional[str]): First name of the employee
            middle_name (Optional[str]): Middle name of the employee
            last_name (Optional[str]): Last name of the employee
            email (Optional[str]): Email address of the employee
            mobile_number (Optional[str]): Mobile phone number
            gender (Optional[GenderType]): Gender of the employee
                - 0: Male
                - 1: Female 
                - 2: Other
                - 3: Not specified
            date_of_birth (Optional[Union[str, datetime]]): Date of birth (ISO format or datetime object)
            date_joined (Optional[Union[str, datetime]]): Date when employee joined (ISO format or datetime object)
            department (Optional[str]): Department name or ID
            business_unit (Optional[str]): Business unit name or ID
            job_title (Optional[str]): Job title/position
            secondary_job_title (Optional[str]): Secondary job title if applicable
            location (Optional[str]): Work location/office
            legal_entity (Optional[str]): Legal entity the employee belongs to
            nationality (Optional[str]): Nationality of the employee
            
        Returns:
            EmployeeCreateResponse: API response containing:
                - succeeded (bool): Whether the operation was successful
                - message (str): Response message
                - errors (List[str]): List of error messages if any
                - data (str): Employee ID if creation was successful
                
        Raises:
            ValueError: If required parameters are missing or invalid
            requests.RequestException: If API request fails
            
        Example:
            >>> employee = Employee()
            >>> response = employee.create(
            ...     first_name="John",
            ...     last_name="Doe", 
            ...     email="john.doe@example.com",
            ...     date_joined="2024-01-15T00:00:00Z",
            ...     department="Engineering"
            ... )
            >>> if response["succeeded"]:
            ...     print(f"Employee created with ID: {response['data']}")
            
        API Response Examples:
            Success Response:
            {
                "succeeded": true,
                "message": "Employee created successfully",
                "errors": null,
                "data": "EMP001234"  # Employee ID
            }
            
            Error Response:
            {
                "succeeded": false,
                "message": "Validation failed",
                "errors": ["First name is required", "Invalid email format"],
                "data": null
            }
        """
        # This is a stub. Actual implementation should call the API endpoint.
        # POST /hris/employees
        raise NotImplementedError("Subclasses must implement this method")
    
    def update_employee(self):
        raise NotImplementedError("Subclasses must implement this method")
    


class Group:

    def __init__(self):
        pass

    def get_all_groups(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_group_by_filter(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_group_types(self):
        raise NotImplementedError("Subclasses must implement this method")



class Department:

    def __init__(self):
        pass

    def get_all_departments(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_department_by_filter(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def create_department(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def update_department(self):
        raise NotImplementedError("Subclasses must implement this method")

class Location:

    def __init__(self):
        pass

    def get_all_locations(self):
        raise NotImplementedError("Subclasses must implement this method")


class JobTitle:

    def __init__(self):
        pass

    def get_all_job_titles(self):
        raise NotImplementedError("Subclasses must implement this method")


class Currency:

    def __init__(self):
        pass

    def get_all_currencies(self):
        raise NotImplementedError("Subclasses must implement this method")


class NoticePeriod:

    def __init__(self):
        pass

    def get_all_notice_periods(self):
        raise NotImplementedError("Subclasses must implement this method")


class ExitReason:

    def __init__(self):
        pass

    def get_all_exit_reasons(self):
        raise NotImplementedError("Subclasses must implement this method")


class EmploymentExit:

    def __init__(self):
        pass

    def get_all_employment_exits(self):
        raise NotImplementedError("Subclasses must implement this method")
