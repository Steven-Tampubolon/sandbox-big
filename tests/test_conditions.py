import pytest
import json
from datetime import datetime
from ingestion.conditions import get_current_conditions
from ingestion.errors import IngestionError

def test_get_current_conditions_success():
    # Fixtures based on .agent-context.md
    aqi_data = {
        "station": "JKT-01",
        "current": {"aqi": 87, "time": "2026-10-19T05:00:00Z"},
        "forecast": [
            {"time": "2026-10-20T06:00:00Z", "aqi": 95},
            {"time": "2026-10-21T06:00:00Z", "aqi": 120}
        ]
    }
    uv_data = {
        "location": "JKT",
        "uv": {"index": 7.2, "time": "2026-10-19T05:00:00Z"}
    }

    aqi_fetcher = lambda: aqi_data
    uv_fetcher = lambda: uv_data
    
    # Fixed time for deterministic test
    now_fixed = lambda: datetime(2026, 10, 19, 5, 10, 0)

    expected = {
        "aqi": 87,
        "aqi_forecast": [
            {"time": "2026-10-20T06:00:00Z", "aqi": 95},
            {"time": "2026-10-21T06:00:00Z", "aqi": 120}
        ],
        "uv_index": 7.2,
        "uv_time": "2026-10-19T05:00:00Z",
        "fetched_at": "2026-10-19T05:10:00Z"
    }

    result = get_current_conditions(aqi_fetcher, uv_fetcher, now=now_fixed)
    assert result == expected

def test_get_current_conditions_aqi_failure():
    aqi_fetcher = lambda: ("failure") # Trigger TypeError in fetch_aqi
    uv_fetcher = lambda: {"location": "JKT", "uv": {"index": 7.2, "time": "2026-10-19T05:00:00Z"}}

    with pytest.raises(IngestionError):
        get_current_conditions(aqi_fetcher, uv_fetcher)

def test_get_current_conditions_uv_failure():
    aqi_fetcher = lambda: {"station": "JKT-01", "current": {"aqi": 87, "time": "2026-10-19T05:00:00Z"}, "forecast": []}
    uv_fetcher = lambda: ("failure") # Trigger TypeError in fetch_uv

    with pytest.raises(IngestionError):
        get_current_conditions(aqi_fetcher, uv_fetcher)

def test_get_current_conditions_timeout():
    def aqi_fetcher():
        raise TimeoutError()
    
    uv_fetcher = lambda: {"location": "JKT", "uv": {"index": 7.2, "time": "2026-10-19T05:00:00Z"}}
    
    with pytest.raises(IngestionError):
        get_current_conditions(aqi_fetcher, uv_fetcher)
