# Python Code Review Tool

## Overview

The Python Code Review Tool is a Python application that uses the Google Gemini API to review Python source code based on a user's request.

It helps identify potential bugs, understand their impact, examine supporting code evidence, and suggest practical next steps.

The tool reads the provided Python file and sends its contents, along with the user's review request, to Gemini. It then saves the AI-generated review and the user's assessment in a Markdown report.

The tool is designed to assist code review, not replace manual testing or developer judgment.

## Features

- Reads Python source files.
- Accepts a natural-language review request from the user.
- Uses Google Gemini to analyze the supplied code.
- Requests findings supported by relevant code evidence.
- Separates confirmed findings from possible risks and hypotheses.
- Requests explanations of potential impact, uncertainties, and recommended next steps.
- Measures the time taken for a review.
- Records available token usage information.
- Saves the review request, exact prompt, raw AI response, and user's assessment.
- Handles invalid inputs, missing files, empty AI responses, and API errors.
- Prevents existing reports from being overwritten.
- Includes automated tests using pytest.

## Technologies Used

- Python 3.11 or newer
- Google Gemini API
- Google Gen AI Python SDK
- python-dotenv
- pytest
- Git and GitHub

## LLM Provider and Model

**Provider:** Google Gemini  
**Model:** `gemini-3.5-flash-lite`

### Why this provider and model?

Google Gemini was selected because it provides an API that can be integrated into a Python application.

The Flash-Lite model was selected as a lightweight option for code-review experiments, aiming to keeping API usage manageable while generating useful review findings.

API access, free-tier eligibility, quotas, and model availability depend on Google's current policies and the user's API account. The application may encounter rate limits or temporary service interruptions.

## Project Structure

```text
python-code-review-tool/
├── review-input/
│   ├── order_service.py
│   ├── README.md
│   ├── REQUESTS.md
│   ├── BUSINESS_RULES.md
│   ├── SHA256SUMS.txt
│   └── cases/
│       ├── cancel.json
│       ├── import.jsonl
│       ├── quantity.json
│       ├── shipping.json
│       └── single.json
├── src/
│   ├── __init__.py
│   └── reviewer.py
├── tests/
│   └── test_reviewer.py
├── reviews/
│   ├── request1_total.md
│   ├── request2_cancelled.md
│   └── request3_general.md
├── evidence/
│   ├── test_results.txt
│   └── usage_summary.md
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

The `review-input/` directory contains the original Python source file supplied for review.

The `src/` directory contains the application code.

The `tests/` directory contains automated tests.

The `reviews/` directory contains the three completed code-review reports.

The `evidence/` directory contains the automated test results and API usage summary.

The `.env.example` file documents the required environment variables without containing a real API key.

## Requirements

Before running the application, ensure you have:

- Python 3.11 or newer.
- A Google Gemini API key.
- Internet access for live API requests.
- Git, if you want to clone the repository.

## Installation and Setup

The following instructions cover Windows and macOS.

### 1. Clone the repository

Replace the placeholder with the URL of your public GitHub repository.

```bash
git clone <your-public-github-repository-url>
cd ai-code-reviewer
```

If you have already downloaded or cloned the project, open a terminal in the project directory instead.

### 2. Check your Python version

Run:

```bash
python --version
```

On macOS, if `python` is not available, try:

```bash
python3 --version
```

Use Python 3.11 or newer.

### 3. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
```

**macOS:**

```bash
python3 -m venv .venv
```

A virtual environment keeps the project's Python dependencies separate from other Python projects.

### 4. Activate the virtual environment

**Windows - PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows - Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

**macOS:**

```bash
source .venv/bin/activate
```

After activation, the terminal usually displays `(.venv)` before the command prompt.

If PowerShell blocks script execution, you can use Command Prompt and run the activation command shown above instead.

### 5. Install dependencies

With the virtual environment activated, run:

**Windows and macOS:**

```bash
python -m pip install -r requirements.txt
```

On macOS, if `python` is unavailable, use:

```bash
python3 -m pip install -r requirements.txt
```

## Environment Configuration

### Required environment variables

The application uses the following environment variables:

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Authenticates requests to the Google Gemini API. |
| `GEMINI_MODEL` | Specifies the Gemini model used for code reviews. |

### Configure the `.env` file

1. Locate `.env.example` in the project root.
2. Create a file named `.env` in the same directory.
3. Add your own API key and model configuration.

Example:

```text
GEMINI_API_KEY=your_actual_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace the placeholder API key with your own key.

The example above assumes that the selected model remains available to your API account. If you change models, ensure that the configured model is supported.

**Security:** Never commit your actual `.env` file, API key, or `.venv` directory to a public repository. The `.gitignore` file should exclude them.

## Running the Application

From the project root, activate the virtual environment and run:

```bash
python src/reviewer.py
```

On macOS, if needed, use:

```bash
python3 src/reviewer.py
```

The application asks for:

1. The path to a Python source file.
2. The issue or behavior you want to investigate.
3. A filename for the review report.
4. Your assessment of the findings.

After a successful review, the generated report is saved in the `reviews/` directory.

For example, the completed reports are:

- `reviews/request1_total.md`
- `reviews/request2_cancelled.md`
- `reviews/request3_general.md`

Use a new filename for each additional review to preserve existing reports.

The tool reviews the source code provided to it; it is not intended to execute the reviewed Python program.

## Running the Automated Tests

The project uses pytest for automated testing.

Run the following command from the project root:

```bash
python -m pytest tests/test_reviewer.py -v
```

On macOS, if needed, use:

```bash
python3 -m pytest tests/test_reviewer.py -v
```

### Test coverage

The test suite contains 12 automated test cases:

| No. | Test case | Purpose |
|---:|---|---|
| 1 | `test_read_python_file` | Checks that a Python source file can be read. |
| 2 | `test_file_not_found` | Checks handling of a missing file. |
| 3 | `test_invalid_file_extension` | Checks rejection of an invalid file extension. |
| 4 | `test_blank_review_request` | Checks handling of an empty review request. |
| 5 | `test_missing_api_settings` | Checks handling of missing API configuration. |
| 6 | `test_successful_review` | Checks a successful review using a mocked AI response. |
| 7 | `test_empty_ai_response` | Checks handling of an empty AI response. |
| 8 | `test_api_failure` | Checks handling of an API failure. |
| 9 | `test_save_report` | Checks that a review report is saved correctly. |
| 10 | `test_source_file_is_not_modified` | Checks that reading the source file does not modify it. |
| 11 | `test_unreadable_file` | Checks handling of an unreadable file. |
| 12 | `test_existing_report_is_not_overwritten` | Checks that an existing report is preserved. |

**Latest test result:** 12 passed, 0 failed.

The test suite includes mocked API responses, so passing the tests does not require making a live Gemini API request for every test.

The recorded test output is stored in:

```text
evidence/test_results.txt
```

To save a fresh test run to that file, use:

**Windows - PowerShell:**

```powershell
python -m pytest tests/test_reviewer.py -v *> evidence/test_results.txt
```

**macOS:**

```bash
python -m pytest tests
```
Review the output file to confirm the latest test results.

## Review Reports

Each successfully generated review report records:

- The user's review request.
- The provider and model.
- The review duration.
- Available token usage information.
- The exact prompt sent to Gemini.
- The raw Gemini response.
- The user's assessment of the findings.

The `reviews/` directory contains the three completed code-review reports.

| Report | Description |
|---|---|
| `request1_total.md` | Investigation of order totals and subtotal calculations. |
| `request2_cancelled.md` | Investigation of cancelled orders in sales reporting. |
| `request3_general.md` | General review focusing on order totals and stock. |

Token counts that are unavailable from the API are recorded as `Unknown`.

## Usage Summary and Evidence

The `evidence/` directory contains:

- `test_results.txt` - Recorded automated test results.
- `usage_summary.md` - Documented review usage information, including available token counts, durations, outcomes, and relevant API errors.

The usage summary records the following totals for the three completed reviews:

| Metric | Total |
|---|---:|
| Input tokens | 39,046 |
| Output tokens | 2,353 |
| Total tokens | 41,399 |

These totals correspond to the three completed reviews documented in the usage summary.

## Limitations and Known Issues

- Review quality depends on the supplied source code, the review request, and the AI-generated response.
- AI-generated findings may be incomplete or incorrect and should be checked manually.
- The tool does not execute the reviewed source code or independently verify proposed fixes.
- The application requires a valid Gemini API configuration and internet access for live reviews.
- API requests may fail because of rate limits, quota restrictions, temporary service unavailability, or other provider errors.
- Token usage information depends on the information returned by the API.
- A successful API response does not guarantee that every finding is correct or that every possible bug has been identified.

If a live review fails, the failure should be reported clearly rather than presented as a successful review.

## Project Status

The application includes the code-review workflow, report generation, automated tests, and documentation of the three completed reviews.

The automated test suite has **12 passing tests and 0 failing tests**.

The three completed review reports and the usage evidence are stored in the `reviews/` and `evidence/` directories, respectively.