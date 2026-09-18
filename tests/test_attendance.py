"""Tests for the AttendanceResource module."""

from unittest.mock import MagicMock, patch

import pytest

from keka.auth import AuthManager, KekaAuth
from keka.config import KekaConfig
from keka.resources.attendance import (
    AttendanceResource,
    _build_approval_status_body,
    _build_attendance_records_params,
    _build_capture_scheme_params,
    _build_on_duty_body,
    _build_on_duty_params,
    _build_shift_policies_params,
    _build_time_entry_body,
    _build_tracking_policies_params,
    _build_weekly_off_policies_params,
    _build_wfh_body,
    _build_wfh_params,
)
from keka.transport import Transport


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def config():
    return KekaConfig(instance_url="https://test.keka.com")


@pytest.fixture
def transport(config):
    return MagicMock(spec=Transport)


@pytest.fixture
def auth():
    return MagicMock(spec=AuthManager)


@pytest.fixture
def resource(transport, config, auth):
    return AttendanceResource(transport, config, auth)


# =============================================================================
# PARAMETER BUILDER TESTS
# =============================================================================

class TestParameterBuilders:
    """Test parameter builder functions."""

    def test_attendance_records_params_all(self):
        params = _build_attendance_records_params(
            employee_ids="id1,id2",
            from_date="2024-01-01",
            to_date="2024-01-31",
            page_number=1,
            page_size=50,
        )
        assert params == {
            "employeeIds": "id1,id2",
            "from": "2024-01-01",
            "to": "2024-01-31",
            "pageNumber": 1,
            "pageSize": 50,
        }

    def test_attendance_records_params_empty(self):
        params = _build_attendance_records_params()
        assert params == {}

    def test_capture_scheme_params(self):
        params = _build_capture_scheme_params(capturescheme_ids="cs1")
        assert params == {"captureschemeIds": "cs1"}

    def test_shift_policies_params(self):
        params = _build_shift_policies_params(shift_policy_ids="sp1,sp2")
        assert params == {"shiftPolicyIds": "sp1,sp2"}

    def test_tracking_policies_params(self):
        params = _build_tracking_policies_params(tracking_policy_ids="tp1")
        assert params == {"trackingPolicyIds": "tp1"}

    def test_weekly_off_policies_params(self):
        params = _build_weekly_off_policies_params(
            weekly_off_policy_ids="wo1", page_number=2
        )
        assert params == {"weeklyOffPolicyIds": "wo1", "pageNumber": 2}

    def test_on_duty_params(self):
        params = _build_on_duty_params(employee_ids="e1", from_date="2024-01-01")
        assert params == {"employeeIds": "e1", "from": "2024-01-01"}

    def test_wfh_params(self):
        params = _build_wfh_params(
            employee_ids="e1", from_date="2024-01-01", to_date="2024-01-31"
        )
        assert params == {
            "employeeIds": "e1",
            "from": "2024-01-01",
            "to": "2024-01-31",
        }


# =============================================================================
# BODY BUILDER TESTS
# =============================================================================

class TestBodyBuilders:
    """Test request body builder functions."""

    def test_time_entry_body_minimal(self):
        body = _build_time_entry_body(
            employee_id="emp1", timestamp="2024-01-15T09:00:00Z"
        )
        assert body == {
            "employeeId": "emp1",
            "timestamp": "2024-01-15T09:00:00Z",
        }

    def test_time_entry_body_with_note(self):
        body = _build_time_entry_body(
            employee_id="emp1",
            timestamp="2024-01-15T09:00:00Z",
            note="Morning check-in",
        )
        assert body["note"] == "Morning check-in"

    def test_on_duty_body_minimal(self):
        body = _build_on_duty_body(
            employee_id="emp1",
            from_date="2024-01-15",
            to_date="2024-01-16",
        )
        assert body == {
            "employeeId": "emp1",
            "fromDate": "2024-01-15",
            "toDate": "2024-01-16",
        }

    def test_on_duty_body_with_sessions(self):
        body = _build_on_duty_body(
            employee_id="emp1",
            from_date="2024-01-15",
            to_date="2024-01-16",
            from_session=0,
            to_session=1,
            note="Client meeting",
        )
        assert body["fromSession"] == 0
        assert body["toSession"] == 1
        assert body["note"] == "Client meeting"

    def test_wfh_body_minimal(self):
        body = _build_wfh_body(
            employee_id="emp1",
            from_date="2024-01-15",
            to_date="2024-01-16",
        )
        assert body == {
            "employeeId": "emp1",
            "fromDate": "2024-01-15",
            "toDate": "2024-01-16",
        }

    def test_wfh_body_with_sessions(self):
        body = _build_wfh_body(
            employee_id="emp1",
            from_date="2024-01-15",
            to_date="2024-01-16",
            from_session=0,
            to_session=1,
            note="Working from home",
        )
        assert body["fromSession"] == 0
        assert body["toSession"] == 1
        assert body["note"] == "Working from home"

    def test_approval_status_body_minimal(self):
        body = _build_approval_status_body(status=1)
        assert body == {"status": 1}

    def test_approval_status_body_with_note(self):
        body = _build_approval_status_body(status=2, note="Rejected due to policy")
        assert body == {"status": 2, "note": "Rejected due to policy"}


# =============================================================================
# RESOURCE METHOD TESTS
# =============================================================================

class TestAttendanceResourceMethods:
    """Test AttendanceResource methods call the correct transport methods."""

    def test_list_records_calls_paginate(self, resource):
        """list_records should call _paginate with the correct path."""
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            with patch.object(resource, "_authorize"):
                resource.list_records(employee_ids="e1", from_date="2024-01-01")
                mock_paginate.assert_called_once()
                call_args = mock_paginate.call_args
                assert call_args[0][0] == "time/attendance"
                assert call_args[1]["params"]["employeeIds"] == "e1"

    def test_list_capture_schemes_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_capture_schemes(capturescheme_ids="cs1")
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/capturescheme"

    def test_list_shift_policies_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_shift_policies(shift_policy_ids="sp1")
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/shiftpolicies"

    def test_list_tracking_policies_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_tracking_policies(tracking_policy_ids="tp1")
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/penalisationpolicies"

    def test_list_weekly_off_policies_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_weekly_off_policies(weekly_off_policy_ids="wo1")
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/weeklyoffpolicies"

    def test_list_holiday_calendars_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_holiday_calendars()
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/holidayscalendar"

    def test_list_holidays_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_holidays(calendar_id="cal123")
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/holidayscalendar/cal123/holidays"

    def test_create_time_entry_for_employee_calls_post(self, resource):
        with patch.object(resource, "_post", return_value={}) as mock_post:
            resource.create_time_entry_for_employee(
                employee_id="emp1", timestamp="2024-01-15T09:00:00Z"
            )
            mock_post.assert_called_once()
            assert mock_post.call_args[0][0] == "attendance/employee/emp1/timeentry"

    def test_create_time_entry_calls_post(self, resource):
        with patch.object(resource, "_post", return_value={}) as mock_post:
            resource.create_time_entry(
                employee_id="emp1", timestamp="2024-01-15T09:00:00Z"
            )
            mock_post.assert_called_once()
            assert mock_post.call_args[0][0] == "attendance/employee/timeentry"

    def test_list_on_duty_requests_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_on_duty_requests(employee_ids="e1")
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/od"

    def test_create_on_duty_request_calls_post(self, resource):
        with patch.object(resource, "_post", return_value={}) as mock_post:
            resource.create_on_duty_request(
                employee_id="emp1",
                from_date="2024-01-15",
                to_date="2024-01-16",
            )
            mock_post.assert_called_once()
            assert mock_post.call_args[0][0] == "time/od"

    def test_list_wfh_requests_calls_paginate(self, resource):
        with patch.object(resource, "_paginate", return_value={}) as mock_paginate:
            resource.list_wfh_requests(employee_ids="e1")
            mock_paginate.assert_called_once()
            assert mock_paginate.call_args[0][0] == "time/wfh"

    def test_create_wfh_request_calls_post(self, resource):
        with patch.object(resource, "_post", return_value={}) as mock_post:
            resource.create_wfh_request(
                employee_id="emp1",
                from_date="2024-01-15",
                to_date="2024-01-16",
            )
            mock_post.assert_called_once()
            assert mock_post.call_args[0][0] == "time/wfh"

    def test_update_approval_status_od_calls_put(self, resource):
        with patch.object(resource, "_put", return_value={}) as mock_put:
            resource.update_approval_status(
                request_id="req1", request_type="od", status=1
            )
            mock_put.assert_called_once()
            assert mock_put.call_args[0][0] == "time/od/req1/status"

    def test_update_approval_status_wfh_calls_put(self, resource):
        with patch.object(resource, "_put", return_value={}) as mock_put:
            resource.update_approval_status(
                request_id="req1", request_type="wfh", status=2, note="Rejected"
            )
            mock_put.assert_called_once()
            assert mock_put.call_args[0][0] == "time/wfh/req1/status"

    def test_update_approval_status_invalid_type_raises(self, resource):
        with pytest.raises(ValueError, match="request_type must be 'od' or 'wfh'"):
            resource.update_approval_status(
                request_id="req1", request_type="invalid", status=1
            )
