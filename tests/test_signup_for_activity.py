from copy import deepcopy

import pytest
from fastapi import HTTPException

from src.app import activities, signup_for_activity


@pytest.fixture(autouse=True)
def restore_activities():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


def test_signup_for_activity_adds_new_student():
    email = "new.student@mergington.edu"

    result = signup_for_activity("Chess Club", email)

    assert result == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_activity_rejects_duplicate_student():
    email = "michael@mergington.edu"

    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity("Chess Club", email)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Student is already signed up"
