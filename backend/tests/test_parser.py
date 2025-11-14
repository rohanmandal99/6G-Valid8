import pytest
from backend.app.log_parser import parse_log_file, events_to_summary

def test_log_parser_with_timestamp():
    # Provide a log file with known expected values
    result = events_to_summary(parse_log_file("backend/sample_logs/simple_rach_log.txt"))
    
    # Check total lines are parsed
    assert result["total_lines"] == 42

    # Check if expected events are counted correctly
    counts = result["counts"]
    assert counts["sync_start"] == 1
    assert counts["sync_success"] == 1
    assert counts["rach_start"] == 1
    assert counts["rach_success"] == 1
    assert counts["rrc_connected"] == 1

def test_empty_log():
    # Test empty log file
    result = events_to_summary(parse_log_file("backend/sample_logs/empty_log.txt"))
    assert result["total_lines"] == 0
    assert result["counts"] == {}
