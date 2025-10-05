"""
Keka SDK Type Definitions

This module contains all type definitions for the Keka API responses and request structures.
It provides comprehensive type safety and IntelliSense support for all Keka API endpoints.

Based on Keka API Documentation:
- https://developers.keka.com/reference/post_hris-employees.md
- https://developers.keka.com/reference/post_hris-employees-search.md
"""

from typing import Optional, Dict, List, Union, Literal, TypedDict
from datetime import datetime


# =============================================================================
# ENUM TYPE DEFINITIONS
# =============================================================================

GenderType = Literal[0, 1, 2, 3]
"""
Gender enumeration values:
- 0: Male
- 1: Female 
- 2: Other
- 3: Not specified
"""

MaritalStatusType = Literal[0, 1, 2]
"""
Marital status enumeration values:
- 0: Single
- 1: Married
- 2: Divorced
"""

TimeTypeEnum = Literal[0, 1, 2]
"""
Time type enumeration values:
- 0: Full Time
- 1: Part Time
- 2: Contract
"""

WorkerTypeEnum = Literal[0, 1, 2]
"""
Worker type enumeration values:
- 0: Employee
- 1: Consultant
- 2: Intern
"""

EmploymentStatusEnum = Literal[0, 1]
"""
Employment status enumeration values:
- 0: Inactive
- 1: Active
"""

AccountStatusEnum = Literal[0, 1, 2]
"""
Account status enumeration values:
- 0: Inactive
- 1: Active
- 2: Suspended
"""

InvitationStatusEnum = Literal[0, 1]
"""
Invitation status enumeration values:
- 0: Pending
- 1: Accepted
"""

ExitStatusEnum = Literal[0, 1, 2]
"""
Exit status enumeration values:
- 0: Active
- 1: Notice Period
- 2: Exited
"""

ExitTypeEnum = Literal[0, 1, 2, 3]
"""
Exit type enumeration values:
- 0: Resignation
- 1: Termination
- 2: Retirement
- 3: Other
"""

RelationTypeEnum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"""
Relation type enumeration values:
- 0: Father
- 1: Mother
- 2: Spouse
- 3: Child
- 4: Sibling
- 5: Father-in-law
- 6: Mother-in-law
- 7: Grandparent
- 8: Guardian
- 9: Other
"""

SystemGroupTypeEnum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"""
System group type enumeration values:
- 0: Department
- 1: Location
- 2: Business Unit
- 3: Cost Center
- 4: Team
- 5: Project
- 6: Band
- 7: Grade
- 8: Level
- 9: Custom
"""


# =============================================================================
# BASIC STRUCTURE TYPE DEFINITIONS
# =============================================================================

class LookupInfo(TypedDict, total=False):
    """
    Standard lookup information structure used throughout Keka API.
    
    Used for: Job titles, departments, locations, policies, etc.
    """
    identifier: Optional[str]
    title: Optional[str]


class EmployeeLookup(TypedDict, total=False):
    """
    Employee lookup structure for references (managers, colleagues, etc.).
    """
    id: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]


class Image(TypedDict, total=False):
    """
    Employee profile image structure.
    """
    fileName: Optional[str]
    thumbs: Optional[Dict[str, Optional[str]]]


class ContingentType(TypedDict, total=False):
    """
    Contingent worker type information.
    """
    id: Optional[str]
    name: Optional[str]


class Address(TypedDict, total=False):
    """
    Address structure for current and permanent addresses.
    """
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip: Optional[str]


class CustomField(TypedDict, total=False):
    """
    Custom field structure for extensible employee data.
    """
    id: Optional[str]
    title: Optional[str]
    type: Optional[str]
    value: Optional[str]


# =============================================================================
# COMPLEX NESTED TYPE DEFINITIONS
# =============================================================================

class Relation(TypedDict, total=False):
    """
    Employee family/emergency contact relation structure.
    """
    id: Optional[str]
    relationType: Optional[RelationTypeEnum]
    gender: Optional[GenderType]
    firstName: Optional[str]
    lastName: Optional[str]
    displayName: Optional[str]
    email: Optional[str]
    dateOfBirth: Optional[str]
    profession: Optional[str]
    mobile: Optional[str]


class Education(TypedDict, total=False):
    """
    Education qualification details structure.
    """
    id: Optional[str]
    degree: Optional[str]
    branch: Optional[str]
    university: Optional[str]
    cgpa: Optional[float]
    yearOfJoining: Optional[str]
    yearOfCompletion: Optional[str]
    customFields: Optional[List[CustomField]]


class Experience(TypedDict, total=False):
    """
    Previous work experience details structure.
    """
    id: Optional[str]
    companyName: Optional[str]
    jobTitle: Optional[str]
    location: Optional[str]
    description: Optional[str]
    dateOfJoining: Optional[str]
    dateOfRelieving: Optional[str]
    customFields: Optional[List[CustomField]]


class GroupLookup(TypedDict, total=False):
    """
    Group/team membership lookup structure.
    """
    id: Optional[str]
    title: Optional[str]
    groupType: Optional[SystemGroupTypeEnum]


# =============================================================================
# EMPLOYEE PROFILE TYPE DEFINITIONS
# =============================================================================

class EmployeeProfile(TypedDict, total=False):
    """
    Complete employee profile structure as returned by Keka API.
    
    This comprehensive structure includes all possible fields that can be
    returned by employee-related API endpoints like search, get by ID, etc.
    
    Used by:
    - Employee search API
    - Get employee by ID API
    - Employee profile updates
    """
    # Basic Identity Information
    id: Optional[str]
    employeeNumber: Optional[str]
    firstName: Optional[str]
    middleName: Optional[str]
    lastName: Optional[str]
    displayName: Optional[str]
    
    # Contact Information
    email: Optional[str]
    personalEmail: Optional[str]
    workPhone: Optional[str]
    homePhone: Optional[str]
    mobilePhone: Optional[str]
    emergencyContactName: Optional[str]
    emergencyContactPhone: Optional[str]
    
    # Location & Demographics
    city: Optional[str]
    countryCode: Optional[str]
    nationality: Optional[str]
    
    # Profile & Media
    image: Optional[Image]
    
    # Job Information
    jobTitle: Optional[LookupInfo]
    secondaryJobTitle: Optional[str]
    
    # Management Hierarchy
    reportsTo: Optional[EmployeeLookup]
    l2Manager: Optional[EmployeeLookup]
    dottedLineManager: Optional[EmployeeLookup]
    
    # Employment Details
    contingentType: Optional[ContingentType]
    timeType: Optional[TimeTypeEnum]
    workerType: Optional[WorkerTypeEnum]
    
    # Profile Status
    isPrivate: Optional[bool]
    isProfileComplete: Optional[bool]
    
    # Personal Information
    maritalStatus: Optional[MaritalStatusType]
    marriageDate: Optional[str]
    gender: Optional[GenderType]
    dateOfBirth: Optional[str]
    professionalSummary: Optional[str]
    
    # Employment Timeline
    joiningDate: Optional[str]
    totalExperienceInDays: Optional[int]
    resignationSubmittedDate: Optional[str]
    exitDate: Optional[str]
    
    # Status Information
    employmentStatus: Optional[EmploymentStatusEnum]
    accountStatus: Optional[AccountStatusEnum]
    invitationStatus: Optional[InvitationStatusEnum]
    exitStatus: Optional[ExitStatusEnum]
    exitType: Optional[ExitTypeEnum]
    exitReason: Optional[str]
    
    # Address Information
    currentAddress: Optional[Address]
    permanentAddress: Optional[Address]
    
    # Related Data Arrays
    relations: Optional[List[Relation]]
    educationDetails: Optional[List[Education]]
    experienceDetails: Optional[List[Experience]]
    customFields: Optional[List[CustomField]]
    groups: Optional[List[GroupLookup]]
    
    # Policy & Configuration Information
    leavePlanInfo: Optional[LookupInfo]
    holidayCalendarId: Optional[str]
    bandInfo: Optional[LookupInfo]
    payGradeInfo: Optional[LookupInfo]
    shiftPolicyInfo: Optional[LookupInfo]
    weeklyOffPolicyInfo: Optional[LookupInfo]
    captureSchemeInfo: Optional[LookupInfo]
    trackingPolicyInfo: Optional[LookupInfo]
    expensePolicyInfo: Optional[LookupInfo]
    overtimePolicyInfo: Optional[LookupInfo]


# =============================================================================
# API REQUEST TYPE DEFINITIONS
# =============================================================================

class EmployeeCreateRequest(TypedDict, total=False):
    """
    Employee creation request structure for POST /hris/employees
    """
    employeeNumber: Optional[str]
    displayName: Optional[str]
    firstName: Optional[str]
    middleName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    mobileNumber: Optional[str]
    gender: Optional[GenderType]
    dateOfBirth: Optional[str]
    dateJoined: Optional[str]
    department: Optional[str]
    businessUnit: Optional[str]
    jobTitle: Optional[str]
    secondaryJobTitle: Optional[str]
    location: Optional[str]
    legalEntity: Optional[str]
    nationality: Optional[str]


class EmployeeSearchRequest(TypedDict, total=False):
    """
    Employee search request structure for POST /hris/employees/search
    """
    workEmail: Optional[str]
    workPhone: Optional[str]


# =============================================================================
# API RESPONSE TYPE DEFINITIONS
# =============================================================================

class BaseKekaResponse(TypedDict, total=False):
    """
    Base Keka API response structure used by all endpoints.
    """
    succeeded: bool
    message: Optional[str]
    errors: Optional[List[str]]


class EmployeeCreateResponse(BaseKekaResponse, total=False):
    """
    Employee creation API response structure.
    
    Used by: POST /hris/employees
    """
    data: Optional[str]  # Employee ID when successful


class EmployeeSearchResponse(BaseKekaResponse, total=False):
    """
    Employee search API response structure.
    
    Used by: POST /hris/employees/search
    """
    data: Optional[EmployeeProfile]


class EmployeeListResponse(BaseKekaResponse, total=False):
    """
    Employee list API response structure.
    
    Used by: GET /hris/employees
    """
    data: Optional[List[EmployeeProfile]]


class EmployeeDetailResponse(BaseKekaResponse, total=False):
    """
    Single employee detail API response structure.
    
    Used by: GET /hris/employees/{id}
    """
    data: Optional[EmployeeProfile]


# =============================================================================
# LEGACY COMPATIBILITY
# =============================================================================

# Legacy alias for backward compatibility
KekaResponse = Dict[str, Union[bool, str, List[str], None]]
"""
Legacy type definition for Keka API response structure.
Use BaseKekaResponse or specific response types for better type safety.
"""


# =============================================================================
# TYPE EXPORT GROUPS
# =============================================================================

# Enum types
__enum_types__ = [
    'GenderType', 'MaritalStatusType', 'TimeTypeEnum', 'WorkerTypeEnum',
    'EmploymentStatusEnum', 'AccountStatusEnum', 'InvitationStatusEnum',
    'ExitStatusEnum', 'ExitTypeEnum', 'RelationTypeEnum', 'SystemGroupTypeEnum'
]

# Basic structure types
__structure_types__ = [
    'LookupInfo', 'EmployeeLookup', 'Image', 'ContingentType', 'Address',
    'CustomField', 'Relation', 'Education', 'Experience', 'GroupLookup'
]

# Request types
__request_types__ = [
    'EmployeeCreateRequest', 'EmployeeSearchRequest'
]

# Response types
__response_types__ = [
    'BaseKekaResponse', 'EmployeeCreateResponse', 'EmployeeSearchResponse',
    'EmployeeListResponse', 'EmployeeDetailResponse', 'KekaResponse'
]

# Main entity types
__entity_types__ = [
    'EmployeeProfile'
]

# All exported types
__all__ = __enum_types__ + __structure_types__ + __request_types__ + __response_types__ + __entity_types__
