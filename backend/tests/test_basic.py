from app.log_parser import parse_log_file

def test_parse_log_file_counts():
    result = parse_log_file("backend/sample_logs/simple_rach_log.txt")
    assert "total_lines" in result
    assert isinstance(result["total_lines"], int)
