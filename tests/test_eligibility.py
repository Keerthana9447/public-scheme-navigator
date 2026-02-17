import pytest
from backend.app import check_eligibility

def test_eligibility():
    result = check_eligibility(age=65, income=100000)
    assert "eligible_schemes" in result
    assert isinstance(result["eligible_schemes"], list)
