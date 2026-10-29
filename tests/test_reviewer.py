import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src import reviewer

# Test 1: Read a Python file successfully
def test_read_python_file(tmp_path):
    python_file = tmp_path / "sample.py"
    python_file.write_text("print('Hello')", encoding="utf-8")

    result = reviewer.read_s_file(python_file)
    assert result == "print('Hello')"

# Test 2: File does not exist
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        reviewer.read_s_file("missing_file.py")

# Test 3: File must have a .py extension
def test_invalid_file_extension(tmp_path):
    text_file = tmp_path / "sample.txt"
    text_file.write_text("Hello", encoding="utf-8")

    with pytest.raises(ValueError):
        reviewer.read_s_file(text_file)

# Test 4: Review request cannot be blank
def test_blank_review_request():
    with pytest.raises(ValueError):
        reviewer.review_code("print('Hello')", "   ")

# Test 5: Missing API settings
def test_missing_api_settings():
    with patch.object(reviewer, "API_KEY", None):
        with patch.object(reviewer, "MODEL", None):
            with pytest.raises(ValueError):
                reviewer.review_code("print('Hello')", "Find bugs")

# Test 6: Successful code review
def test_successful_review():
    fake_response = MagicMock()
    fake_response.text = "No confirmed bugs found."
    fake_response.usage_metadata = MagicMock()
    fake_response.usage_metadata.prompt_token_count = 100
    fake_response.usage_metadata.candidates_token_count = 50
    fake_response.usage_metadata.total_token_count = 150
    fake_response.usage_metadata.thoughts_token_count = 0

    with patch.object(reviewer, "API_KEY", "test_key"):
        with patch.object(reviewer, "MODEL", "test_model"):
            with patch.object(reviewer.genai, "Client") as mock_client:
                mock_client.return_value.models.generate_content.return_value = fake_response

                result = reviewer.review_code(
                    "def add(a, b): return a + b",
                    "Check for bugs"
                )

    assert result[0]  # Prompt was created
    assert result[1] == "No confirmed bugs found."
    assert result[2] >= 0  # Duration
    assert result[3] == 100  # Input tokens
    assert result[4] == 50   # Output tokens
    assert result[5] == 150  # Total tokens
    assert result[6] == 0    # Thought tokens

# Test 7: Gemini returns an empty response
def test_empty_ai_response():
    fake_response = MagicMock()
    fake_response.text = "   "
    fake_response.usage_metadata = None

    with patch.object(reviewer, "API_KEY", "test_key"):
        with patch.object(reviewer, "MODEL", "test_model"):
            with patch.object(reviewer.genai, "Client") as mock_client:
                mock_client.return_value.models.generate_content.return_value = fake_response

                with pytest.raises(RuntimeError):
                    reviewer.review_code("print('Hello')", "Find bugs")

# Test 8: API call fails
def test_api_failure():
    with patch.object(reviewer, "API_KEY", "test_key"):
        with patch.object(reviewer, "MODEL", "test_model"):
            with patch.object(reviewer.genai, "Client") as mock_client:
                mock_client.return_value.models.generate_content.side_effect = Exception(
                    "API unavailable")
                with pytest.raises(Exception, match="API unavailable"):
                    reviewer.review_code("print('Hello')", "Find bugs")

# Test 9: Save a report successfully
def test_save_report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    reviewer.save_report(
        "Find bugs",
        "Review prompt",
        "No confirmed bugs found.",
        "test_report.md",
        1.5,
        "The review looks reasonable.",
        100,
        50,
        150,
        0
    )

    report_file = tmp_path / "reviews" / "test_report.md"
    assert report_file.exists()

    report_text = report_file.read_text(encoding="utf-8")
    assert "Find bugs" in report_text
    assert "Review prompt" in report_text
    assert "No confirmed bugs found." in report_text
    assert "The review looks reasonable." in report_text
    assert "Input tokens: 100" in report_text

# Test 10: Source file remains unchanged
def test_source_file_is_not_modified(tmp_path):
    python_file = tmp_path / "sample.py"
    original_code = "def add(a, b):\n    return a + b\n"
    python_file.write_text(original_code, encoding="utf-8")
    reviewer.read_s_file(python_file)
    assert python_file.read_text(encoding="utf-8") == original_code

# Test 11: Unreadable source file
def test_unreadable_file(tmp_path, monkeypatch):
    python_file = tmp_path / "sample.py"
    python_file.write_text("print('Hello')", encoding="utf-8")

    def raise_permission_error(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr(Path, "read_text", raise_permission_error)

    with pytest.raises(PermissionError):
        reviewer.read_s_file(python_file)

# Test 12: Existing report is not overwritten
def test_existing_report_is_not_overwritten(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    reviews_folder = tmp_path / "reviews"
    reviews_folder.mkdir()

    report_path = reviews_folder / "existing_report.md"
    original_content = "This is my original report."
    report_path.write_text(original_content, encoding="utf-8")

    with pytest.raises(FileExistsError):
        reviewer.save_report(
            review_request="Test request",
            prompt="Test prompt",
            raw_response="Test response",
            report_name="existing_report.md",
            duration=1.0,
            assessment="Test assessment",
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
            thought_tokens=None,
        )

    assert report_path.read_text(encoding="utf-8") == original_content