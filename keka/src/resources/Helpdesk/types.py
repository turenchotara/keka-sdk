"""
Keka Helpdesk Module Type Definitions

This module contains type definitions specific to Helpdesk operations that interact
with employee search and other HR-related APIs.

Based on Keka API Documentation:
- https://developers.keka.com/reference/post_hris-employees-search.md
"""

from typing import Optional, Dict, List, Union, Literal, TypedDict


# =============================================================================
# EMPLOYEE SEARCH REQUEST TYPES
# =============================================================================

class EmployeeSearchRequest(TypedDict, total=False):
    """
    Employee search request structure for POST /hris/employees/search
    
    Based on: https://developers.keka.com/reference/post_hris-employees-search.md
    
    This request allows searching for employees by their work contact information.
    At least one of the search criteria should be provided for meaningful results.
    """
    workPhone: Optional[str]  # Work phone number to search for (nullable)
    workEmail: Optional[str]  # Work email address to search for (nullable)


# =============================================================================
# ENUM TYPE DEFINITIONS FOR EMPLOYEE DATA
# =============================================================================

GenderEnum = Literal[0, 1, 2, 3]
"""Gender values: 0=Male, 1=Female, 2=Other, 3=Not specified"""

MaritalStatusEnum = Literal[0, 1, 2]
"""Marital status: 0=Single, 1=Married, 2=Divorced"""

TimeTypeEnum = Literal[0, 1, 2]
"""Time type: 0=Full Time, 1=Part Time, 2=Contract"""

WorkerTypeEnum = Literal[0, 1, 2]
"""Worker type: 0=Employee, 1=Consultant, 2=Intern"""

EmploymentStatusEnum = Literal[0, 1]
"""Employment status: 0=Inactive, 1=Active"""

AccountStatusEnum = Literal[0, 1, 2]
"""Account status: 0=Inactive, 1=Active, 2=Suspended"""

InvitationStatusEnum = Literal[0, 1]
"""Invitation status: 0=Pending, 1=Accepted"""

ExitStatusEnum = Literal[0, 1, 2]
"""Exit status: 0=Active, 1=Notice Period, 2=Exited"""

ExitTypeEnum = Literal[0, 1, 2, 3]
"""Exit type: 0=Resignation, 1=Termination, 2=Retirement, 3=Other"""

RelationTypeEnum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"""Relation types: 0=Father, 1=Mother, 2=Spouse, 3=Child, etc."""

SystemGroupTypeEnum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"""Group types: 0=Department, 1=Location, 2=Business Unit, etc."""


# =============================================================================
# BASIC STRUCTURE TYPES FOR EMPLOYEE DATA
# =============================================================================

class LookupInfo(TypedDict, total=False):
    """Standard lookup info for job titles, departments, etc."""
    identifier: Optional[str]
    title: Optional[str]


class EmployeeLookup(TypedDict, total=False):
    """Employee reference for managers."""
    id: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]


class EmployeeImage(TypedDict, total=False):
    """Employee profile image."""
    fileName: Optional[str]
    thumbs: Optional[Dict[str, Optional[str]]]


class ContingentType(TypedDict, total=False):
    """Contingent worker type."""
    id: Optional[str]
    name: Optional[str]


class EmployeeAddress(TypedDict, total=False):
    """Employee address."""
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip: Optional[str]


class CustomField(TypedDict, total=False):
    """Custom field structure."""
    id: Optional[str]
    title: Optional[str]
    type: Optional[str]
    value: Optional[str]


class EmployeeRelation(TypedDict, total=False):
    """Employee relation/contact."""
    id: Optional[str]
    relationType: Optional[RelationTypeEnum]
    gender: Optional[GenderEnum]
    firstName: Optional[str]
    lastName: Optional[str]
    displayName: Optional[str]
    email: Optional[str]
    dateOfBirth: Optional[str]
    profession: Optional[str]
    mobile: Optional[str]


class EducationDetail(TypedDict, total=False):
    """Education details."""
    id: Optional[str]
    degree: Optional[str]
    branch: Optional[str]
    university: Optional[str]
    cgpa: Optional[float]
    yearOfJoining: Optional[str]
    yearOfCompletion: Optional[str]
    customFields: Optional[List[CustomField]]


class ExperienceDetail(TypedDict, total=False):
    """Work experience details."""
    id: Optional[str]
    companyName: Optional[str]
    jobTitle: Optional[str]
    location: Optional[str]
    description: Optional[str]
    dateOfJoining: Optional[str]
    dateOfRelieving: Optional[str]
    customFields: Optional[List[CustomField]]


class GroupLookup(TypedDict, total=False):
    """Group/team membership."""
    id: Optional[str]
    title: Optional[str]
    groupType: Optional[SystemGroupTypeEnum]


# =============================================================================
# EMPLOYEE PROFILE TYPE
# =============================================================================

class EmployeeProfileData(TypedDict, total=False):
    """
    Complete employee profile structure as returned by POST /hris/employees/search
    
    Matches the exact API response structure for helpdesk operations.
    """
    # Basic Identity
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
    
    # Profile & Job Information
    image: Optional[EmployeeImage]
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
    isPrivate: Optional[bool]
    isProfileComplete: Optional[bool]
    
    # Personal Information
    maritalStatus: Optional[MaritalStatusEnum]
    marriageDate: Optional[str]
    gender: Optional[GenderEnum]
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
    currentAddress: Optional[EmployeeAddress]
    permanentAddress: Optional[EmployeeAddress]
    
    # Related Data Collections
    relations: Optional[List[EmployeeRelation]]
    educationDetails: Optional[List[EducationDetail]]
    experienceDetails: Optional[List[ExperienceDetail]]
    customFields: Optional[List[CustomField]]
    groups: Optional[List[GroupLookup]]
    
    # Policy Assignments
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
# API RESPONSE TYPES
# =============================================================================

class BaseHelpdeskResponse(TypedDict, total=False):
    """Base response structure for Helpdesk API operations."""
    succeeded: bool
    message: Optional[str]
    errors: Optional[List[str]]


class EmployeeSearchResponse(BaseHelpdeskResponse, total=False):
    """
    Employee search API response for POST /hris/employees/search
    
    Based on: https://developers.keka.com/reference/post_hris-employees-search.md
    """
    data: Optional[EmployeeProfileData]


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Request types
    'EmployeeSearchRequest',
    
    # Response types  
    'BaseHelpdeskResponse',
    'EmployeeSearchResponse',
    
    # Data types
    'EmployeeProfileData',
    'LookupInfo',
    'EmployeeLookup',
    'EmployeeImage',
    'ContingentType',
    'EmployeeAddress',
    'CustomField',
    'EmployeeRelation',
    'EducationDetail',
    'ExperienceDetail',
    'GroupLookup',
    
    # Enums
    'GenderEnum',
    'MaritalStatusEnum',
    'TimeTypeEnum',
    'WorkerTypeEnum',
    'EmploymentStatusEnum',
    'AccountStatusEnum',
    'InvitationStatusEnum',
    'ExitStatusEnum',
    'ExitTypeEnum',
    'RelationTypeEnum',
    'SystemGroupTypeEnum'
]
