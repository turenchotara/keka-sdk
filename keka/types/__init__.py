from typing import Dict, List, Literal, Optional, TypedDict, Union

# =============================================================================
# ENUM TYPE DEFINITIONS
# =============================================================================

GenderType = Literal[0, 1, 2, 3]
"""0: Male, 1: Female, 2: Other, 3: Not specified."""

MaritalStatusType = Literal[0, 1, 2]
"""0: Single, 1: Married, 2: Divorced."""

TimeTypeEnum = Literal[0, 1, 2]
"""0: Full Time, 1: Part Time, 2: Contract."""

WorkerTypeEnum = Literal[0, 1, 2]
"""0: Employee, 1: Consultant, 2: Intern."""

EmploymentStatusEnum = Literal[0, 1]
"""0: Inactive, 1: Active."""

AccountStatusEnum = Literal[0, 1, 2]
"""0: Inactive, 1: Active, 2: Suspended."""

InvitationStatusEnum = Literal[0, 1]
"""0: Pending, 1: Accepted."""

ExitStatusEnum = Literal[0, 1, 2]
"""0: Active, 1: Notice Period, 2: Exited."""

ExitTypeEnum = Literal[0, 1, 2, 3]
"""0: Resignation, 1: Termination, 2: Retirement, 3: Other."""

RelationTypeEnum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"""Family/emergency-contact relation type."""

SystemGroupTypeEnum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"""System group type (Department, Location, Business Unit, ...)."""


# =============================================================================
# BASIC STRUCTURE TYPE DEFINITIONS
# =============================================================================

class LookupInfo(TypedDict, total=False):
    """Standard lookup info (job titles, departments, locations, policies)."""

    identifier: Optional[str]
    title: Optional[str]


class EmployeeLookup(TypedDict, total=False):
    """Employee reference (managers, colleagues, etc.)."""

    id: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]


class Image(TypedDict, total=False):
    """Employee profile image."""

    fileName: Optional[str]
    thumbs: Optional[Dict[str, Optional[str]]]


class ContingentType(TypedDict, total=False):
    """Contingent worker type information."""

    id: Optional[str]
    name: Optional[str]


class Address(TypedDict, total=False):
    """Current or permanent address."""

    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip: Optional[str]


class CustomField(TypedDict, total=False):
    """Custom field for extensible employee data."""

    id: Optional[str]
    title: Optional[str]
    type: Optional[str]
    value: Optional[str]


# =============================================================================
# COMPLEX NESTED TYPE DEFINITIONS
# =============================================================================

class Relation(TypedDict, total=False):
    """Family/emergency contact relation."""

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
    """Education qualification details."""

    id: Optional[str]
    degree: Optional[str]
    branch: Optional[str]
    university: Optional[str]
    cgpa: Optional[float]
    yearOfJoining: Optional[str]
    yearOfCompletion: Optional[str]
    customFields: Optional[List[CustomField]]


class Experience(TypedDict, total=False):
    """Previous work experience details."""

    id: Optional[str]
    companyName: Optional[str]
    jobTitle: Optional[str]
    location: Optional[str]
    description: Optional[str]
    dateOfJoining: Optional[str]
    dateOfRelieving: Optional[str]
    customFields: Optional[List[CustomField]]


class GroupLookup(TypedDict, total=False):
    """Group/team membership lookup."""

    id: Optional[str]
    title: Optional[str]
    groupType: Optional[SystemGroupTypeEnum]


# =============================================================================
# EMPLOYEE PROFILE TYPE DEFINITIONS
# =============================================================================

class EmployeeProfile(TypedDict, total=False):
    """Complete employee profile as returned by Keka employee endpoints."""

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


# Backwards-compatible alias (the Helpdesk module previously used this name).
EmployeeProfileData = EmployeeProfile


# =============================================================================
# HRIS ENTITY TYPE DEFINITIONS
# =============================================================================

class Department(TypedDict, total=False):
    """Department entity from GET /hris/departments."""

    id: Optional[str]
    parentId: Optional[str]
    name: Optional[str]
    description: Optional[str]
    isArchived: Optional[bool]
    departmentHeads: Optional[List[EmployeeLookup]]


class LocationAddress(TypedDict, total=False):
    """Address component for Location entity."""

    addressLine1: Optional[str]
    addressLine2: Optional[str]
    countryCode: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]


class Location(TypedDict, total=False):
    """Location entity from GET /hris/locations."""

    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    address: Optional[LocationAddress]


class Group(TypedDict, total=False):
    """Group entity from GET /hris/groups."""

    id: Optional[str]
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    groupTypeId: Optional[str]


class GroupType(TypedDict, total=False):
    """Group type entity from GET /hris/grouptypes."""

    id: Optional[str]
    name: Optional[str]
    systemGroupType: Optional[SystemGroupTypeEnum]


class JobTitle(TypedDict, total=False):
    """Job title entity from GET /hris/jobtitles."""

    id: Optional[str]
    name: Optional[str]


class Currency(TypedDict, total=False):
    """Currency entity from GET /hris/currencies."""

    id: Optional[str]
    code: Optional[str]
    name: Optional[str]


class NoticePeriod(TypedDict, total=False):
    """Notice period entity from GET /hris/noticeperiods."""

    id: Optional[str]
    name: Optional[str]


class ExitReasonItem(TypedDict, total=False):
    """Individual exit/termination reason item."""

    id: Optional[str]
    name: Optional[str]


class ExitReasons(TypedDict, total=False):
    """Exit reasons response from GET /hris/exitreasons."""

    exitReason: Optional[List[ExitReasonItem]]
    terminationReason: Optional[List[ExitReasonItem]]


# =============================================================================
# LEAVE TYPE DEFINITIONS
# =============================================================================

SessionType = Literal[0, 1]
"""0: FirstHalf, 1: SecondHalf."""

LeaveRequestStatusEnum = Literal[0, 1, 2, 3, 4]
"""0: Pending, 1: Approved, 2: Rejected, 3: Cancelled, 4: InApprovalProcess."""

TimeDurationEnum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
"""Time duration unit enum."""


class TimePeriod(TypedDict, total=False):
    """Time period with unit and duration."""

    unit: Optional[TimeDurationEnum]
    duration: Optional[float]
    durationString: Optional[str]


class LeaveTypeSelection(TypedDict, total=False):
    """Leave type selection within a leave request."""

    leaveTypeIdentifier: Optional[str]
    leaveTypeName: Optional[str]
    count: Optional[float]
    duration: Optional[TimePeriod]


class LeaveRequest(TypedDict, total=False):
    """Leave request entity from GET /time/leaverequests."""

    id: Optional[str]
    employeeIdentifier: Optional[str]
    employeeNumber: Optional[str]
    fromDate: Optional[str]
    toDate: Optional[str]
    fromSession: Optional[SessionType]
    toSession: Optional[SessionType]
    requestedOn: Optional[str]
    note: Optional[str]
    cancelRejectReason: Optional[str]
    status: Optional[LeaveRequestStatusEnum]
    selection: Optional[List[LeaveTypeSelection]]
    lastActionTakenOn: Optional[str]


class LeaveBalanceItem(TypedDict, total=False):
    """Individual leave balance for a leave type."""

    leaveTypeId: Optional[str]
    leaveTypeName: Optional[str]
    accruedAmount: Optional[float]
    consumedAmount: Optional[float]
    availableBalance: Optional[float]
    annualQuota: Optional[float]


class EmployeeLeaveBalance(TypedDict, total=False):
    """Employee leave balance from GET /time/leavebalance."""

    employeeIdentifier: Optional[str]
    employeeNumber: Optional[str]
    employeeName: Optional[str]
    leaveBalance: Optional[List[LeaveBalanceItem]]


class LeaveType(TypedDict, total=False):
    """Leave type entity from GET /time/leavetypes."""

    id: Optional[str]
    name: Optional[str]
    code: Optional[str]


class LeavePlan(TypedDict, total=False):
    """Leave plan entity from GET /time/leaveplans."""

    id: Optional[str]
    name: Optional[str]


# =============================================================================
# HELPDESK TYPE DEFINITIONS
# =============================================================================

TicketStatusEnum = Literal[0, 1, 2, 3, 4, 5]
"""0: Open, 1: Pending, 2: Resolved, 3: Closed, 4: InProgress, 5: OnHold."""

TicketPriorityEnum = Literal[0, 1, 2, 3]
"""0: Low, 1: Medium, 2: High, 3: Critical."""


class APILookup(TypedDict, total=False):
    """API lookup for ticket references."""

    id: Optional[str]
    name: Optional[str]


class Ticket(TypedDict, total=False):
    """Helpdesk ticket entity from GET /helpdesk/tickets."""

    id: Optional[str]
    ticketNumber: Optional[int]
    title: Optional[str]
    categoryId: Optional[str]
    status: Optional[TicketStatusEnum]
    raisedBy: Optional[APILookup]
    assignedTo: Optional[APILookup]
    requestedOn: Optional[str]
    priority: Optional[TicketPriorityEnum]
    lastModified: Optional[str]
    closingReason: Optional[str]
    closedOn: Optional[str]
    closedBy: Optional[APILookup]
    csatScore: Optional[int]
    csatResponse: Optional[str]


class TicketCategory(TypedDict, total=False):
    """Helpdesk ticket category from GET /helpdesk/ticket/categories."""

    id: Optional[str]
    name: Optional[str]


class TicketClosingReason(TypedDict, total=False):
    """Helpdesk ticket closing reason from GET /helpdesk/ticket/closingreasons."""

    id: Optional[str]
    name: Optional[str]


# =============================================================================
# API REQUEST TYPE DEFINITIONS
# =============================================================================

class EmployeeCreateRequest(TypedDict, total=False):
    """Employee creation request body for POST /hris/employees."""

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
    """Employee search request body for POST /hris/employees/search."""

    workEmail: Optional[str]
    workPhone: Optional[str]


class EmployeeExitRequest(TypedDict, total=False):
    """Employee exit request body for POST /hris/employees/{id}/exitrequest."""

    exitType: Optional[ExitTypeEnum]
    exitReason: Optional[str]
    resignationDate: Optional[str]
    lastWorkingDate: Optional[str]
    isOkToRehire: Optional[bool]
    comments: Optional[str]


class EmployeeJobDetailsUpdateRequest(TypedDict, total=False):
    """Request body for PUT /hris/employees/jobdetails."""

    employeeId: Optional[str]
    jobTitleId: Optional[str]
    departmentId: Optional[str]
    locationId: Optional[str]
    businessUnitId: Optional[str]
    reportsToId: Optional[str]
    effectiveDate: Optional[str]


class EmployeePersonalDetailsUpdateRequest(TypedDict, total=False):
    """Request body for PUT /hris/employees/personaldetails."""

    employeeId: Optional[str]
    firstName: Optional[str]
    middleName: Optional[str]
    lastName: Optional[str]
    displayName: Optional[str]
    dateOfBirth: Optional[str]
    gender: Optional[GenderType]
    maritalStatus: Optional[MaritalStatusType]
    mobilePhone: Optional[str]
    personalEmail: Optional[str]
    nationality: Optional[str]


class LeaveRequestCreateRequest(TypedDict, total=False):
    """Request body for POST /time/leaverequests."""

    employeeId: Optional[str]
    leaveTypeId: Optional[str]
    fromDate: Optional[str]
    toDate: Optional[str]
    fromSession: Optional[SessionType]
    toSession: Optional[SessionType]
    note: Optional[str]


class TicketCreateRequest(TypedDict, total=False):
    """Request body for POST /helpdesk/tickets."""

    title: Optional[str]
    description: Optional[str]
    categoryId: Optional[str]
    priority: Optional[TicketPriorityEnum]
    employeeId: Optional[str]


class TicketUpdateRequest(TypedDict, total=False):
    """Request body for PUT /helpdesk/tickets/{ticketId}."""

    status: Optional[TicketStatusEnum]
    priority: Optional[TicketPriorityEnum]
    assignedToId: Optional[str]
    closingReason: Optional[str]
    comments: Optional[str]


# =============================================================================
# API RESPONSE TYPE DEFINITIONS
# =============================================================================

class BaseKekaResponse(TypedDict, total=False):
    """Base response envelope used by all Keka endpoints."""

    succeeded: bool
    message: Optional[str]
    errors: Optional[List[str]]


class EmployeeCreateResponse(BaseKekaResponse, total=False):
    """Response for POST /hris/employees (data is the new employee ID)."""

    data: Optional[str]


class EmployeeSearchResponse(BaseKekaResponse, total=False):
    """Response for POST /hris/employees/search."""

    data: Optional[EmployeeProfile]


class EmployeeListResponse(BaseKekaResponse, total=False):
    """Response for GET /hris/employees."""

    data: Optional[List[EmployeeProfile]]


class EmployeeDetailResponse(BaseKekaResponse, total=False):
    """Response for GET /hris/employees/{id}."""

    data: Optional[EmployeeProfile]


class PaginatedResponse(BaseKekaResponse, total=False):
    """A single page of a paginated list response."""

    data: Optional[List[object]]
    pageNumber: Optional[int]
    pageSize: Optional[int]
    totalPages: Optional[int]
    totalRecords: Optional[int]


class BasePaginatedResponse(TypedDict, total=False):
    """Base paginated response with common fields."""

    succeeded: bool
    message: Optional[str]
    errors: Optional[List[str]]
    pageNumber: Optional[int]
    pageSize: Optional[int]
    firstPage: Optional[str]
    lastPage: Optional[str]
    totalPages: Optional[int]
    totalRecords: Optional[int]
    nextPage: Optional[str]
    previousPage: Optional[str]


class DepartmentPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /hris/departments."""

    data: Optional[List[Department]]


class LocationPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /hris/locations."""

    data: Optional[List[Location]]


class GroupPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /hris/groups."""

    data: Optional[List[Group]]


class GroupTypePagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /hris/grouptypes."""

    data: Optional[List[GroupType]]


class JobTitlePagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /hris/jobtitles."""

    data: Optional[List[JobTitle]]


class CurrencyPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /hris/currencies."""

    data: Optional[List[Currency]]


class NoticePeriodPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /hris/noticeperiods."""

    data: Optional[List[NoticePeriod]]


class BooleanResponse(BaseKekaResponse, total=False):
    """Boolean response for operations like deactivate employee."""

    data: Optional[bool]


class LeaveRequestPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /time/leaverequests."""

    data: Optional[List[LeaveRequest]]


class LeaveBalancePagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /time/leavebalance."""

    data: Optional[List[EmployeeLeaveBalance]]


class LeaveTypePagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /time/leavetypes."""

    data: Optional[List[LeaveType]]


class LeavePlanPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /time/leaveplans."""

    data: Optional[List[LeavePlan]]


class LeaveRequestCreateResponse(BaseKekaResponse, total=False):
    """Response for POST /time/leaverequests."""

    data: Optional[str]


class TicketPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /helpdesk/tickets."""

    data: Optional[List[Ticket]]


class TicketCategoryPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /helpdesk/ticket/categories."""

    data: Optional[List[TicketCategory]]


class TicketClosingReasonPagedResponse(BasePaginatedResponse, total=False):
    """Paginated response for GET /helpdesk/ticket/closingreasons."""

    data: Optional[List[TicketClosingReason]]


class TicketCreateResponse(BaseKekaResponse, total=False):
    """Response for POST /helpdesk/tickets."""

    data: Optional[str]


class TicketUpdateResponse(BaseKekaResponse, total=False):
    """Response for PUT /helpdesk/tickets/{ticketId}."""

    data: Optional[bool]


# =============================================================================
# LEGACY COMPATIBILITY
# =============================================================================

KekaResponse = Dict[str, Union[bool, str, List[str], None]]
"""Legacy loose response type. Prefer the typed responses above."""


__all__ = [
    # Enums
    "GenderType", "MaritalStatusType", "TimeTypeEnum", "WorkerTypeEnum",
    "EmploymentStatusEnum", "AccountStatusEnum", "InvitationStatusEnum",
    "ExitStatusEnum", "ExitTypeEnum", "RelationTypeEnum", "SystemGroupTypeEnum",
    "SessionType", "LeaveRequestStatusEnum", "TimeDurationEnum",
    "TicketStatusEnum", "TicketPriorityEnum",
    # Basic Structures
    "LookupInfo", "EmployeeLookup", "Image", "ContingentType", "Address",
    "CustomField", "Relation", "Education", "Experience", "GroupLookup",
    "TimePeriod", "APILookup",
    # Employee Profile
    "EmployeeProfile", "EmployeeProfileData",
    # HRIS Entities
    "Department", "Location", "LocationAddress", "Group", "GroupType",
    "JobTitle", "Currency", "NoticePeriod", "ExitReasonItem", "ExitReasons",
    # Leave Entities
    "LeaveTypeSelection", "LeaveRequest", "LeaveBalanceItem",
    "EmployeeLeaveBalance", "LeaveType", "LeavePlan",
    # Helpdesk Entities
    "Ticket", "TicketCategory", "TicketClosingReason",
    # Employee Requests
    "EmployeeCreateRequest", "EmployeeSearchRequest", "EmployeeExitRequest",
    "EmployeeJobDetailsUpdateRequest", "EmployeePersonalDetailsUpdateRequest",
    # Leave Requests
    "LeaveRequestCreateRequest",
    # Helpdesk Requests
    "TicketCreateRequest", "TicketUpdateRequest",
    # Base Responses
    "BaseKekaResponse", "BasePaginatedResponse", "BooleanResponse",
    # Employee Responses
    "EmployeeCreateResponse", "EmployeeSearchResponse",
    "EmployeeListResponse", "EmployeeDetailResponse", "PaginatedResponse",
    # HRIS Paged Responses
    "DepartmentPagedResponse", "LocationPagedResponse", "GroupPagedResponse",
    "GroupTypePagedResponse", "JobTitlePagedResponse", "CurrencyPagedResponse",
    "NoticePeriodPagedResponse",
    # Leave Paged Responses
    "LeaveRequestPagedResponse", "LeaveBalancePagedResponse",
    "LeaveTypePagedResponse", "LeavePlanPagedResponse", "LeaveRequestCreateResponse",
    # Helpdesk Paged Responses
    "TicketPagedResponse", "TicketCategoryPagedResponse",
    "TicketClosingReasonPagedResponse", "TicketCreateResponse", "TicketUpdateResponse",
    # Legacy
    "KekaResponse",
]
