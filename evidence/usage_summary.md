# Python Code Review Tool - Usage Summary

## 1. Project Information

- **Project:** Python Code Review Tool
- **Provider:** Google Gemini
- **Model:** gemini-3.5-flash-lite
- **Purpose:** Review Python source code based on a user's request.
- **Review method:** Gemini API

## 2. Review Results

| Review | Provider | Model | Input Tokens | Output Tokens | Total Tokens | Duration | Outcome |
|---|---|---|---:|---:|---:|---:|---|
| Review 1 - Quantity and Subtotal | Google Gemini | gemini-3.5-flash-lite | 13,029 | 847 | 13,876 | 4.03 seconds | Success |
| Review 2 - Cancelled Orders | Google Gemini | gemini-3.5-flash-lite | 13,010 | 717 | 13,727 | 3.62 seconds | Success |
| Review 3 - General Code Review | Google Gemini | gemini-3.5-flash-lite | 13,007 | 789 | 13,796 | 5.03 seconds | Success |

## 3. Token Usage

Token usage is based on the values recorded in the three successful API responses.

- **Total input tokens:** 39,046
- **Total output tokens:** 2,353
- **Total tokens used:** 41,399
- **Thought tokens:** Unknown for all three reviews

The total token count is the sum of the total tokens reported for the three reviews. Thought-token counts were unavailable in the recorded reports and have not been estimated.

## 4. Testing

- **Automated testing framework:** pytest
- **Tests executed:** 12
- **Tests passed:** 12
- **Tests failed:** 0
- **Test execution time:** 1.28 seconds

Test results are saved in `evidence/test_results.txt`.

## 5. API Availability

An earlier live API request returned a `503 UNAVAILABLE` error because the requested model gemini-3.8-flash was experiencing high demand.

To address this issue, the model configuration was changed to use gemini-3.5-flash-lite available to use with the API key. After this change, all three required code reviews were completed successfully.

The recorded outcomes, durations, and token usage for the three completed reviews are listed in Section 3.

## 6. Review Reports

The following reports were generated and saved in the `reviews` directory:

1. `request1_total.md` - Quantity and subtotal investigation.
2. `request2_cancelled.md` - Cancelled orders in sales reporting.
3. `request3_general.md` - General review focusing on order totals and stock.

Each report contains the review request, provider and model information, duration, token usage, prompt sent to Gemini, raw AI response, and personal assessment.
