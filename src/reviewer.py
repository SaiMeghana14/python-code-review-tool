import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load settings from the .env file
load_dotenv()

MODEL = os.getenv("GEMINI_MODEL")
API_KEY = os.getenv("GEMINI_API_KEY")

# Step 1: Read the Python file
def read_s_file(p_file):
    path = Path(p_file)

    if path.suffix != ".py":
         raise ValueError("Please enter a Python file ending in .py")

    if not path.is_file():
        raise FileNotFoundError("Python file not found!")

    return path.read_text(encoding="utf-8")

# Step 2: Ask Gemini to review the code
def review_code(s_code,review_request):
    if not review_request.strip():
        raise ValueError("Please describe what you want to review.")

    if not API_KEY or not MODEL:
        raise ValueError("Check your Gemini settings in the .env file.")

    # Connect to Gemini
    client = genai.Client(api_key=API_KEY)

    # Prepare the instructions for Gemini
    prompt = f"""
    You are a Python code reviewer.Review the supplied source code based on the user's request.
    Instructions:
    1. Identify relevant functions, expressions, and source lines automatically.
    2. Explain each finding and quote the relevant code that supports it.
    3. Explain how the finding could cause the reported behavior or affect the application.
    4. Separate confirmed findings from possible risks and hypotheses.
    5. Explain what information is missing or uncertain.
    6. Suggest practical next steps to investigate or fix the issue.
    7. Do not invent bugs just to provide an answer. If you cannot confirm a bug from the available evidence,say so.
    8. Do not claim that you executed the code, tested it, verified a fix, or inspected files that were not provided.
    9. If the request is vague, investigate the supplied code carefully. Ask for clarification or explain the limitations when necessary.
    10. Do not invent line numbers. Include them only when they can be identified reliably.
    Use these sections in your response:
    - Summary
    - Findings and supporting code evidence
    - Potential impact
    - Uncertainties and missing information
    - Recommended next steps
    - Limitations
    User request:
    {review_request}
    Python source code: 
    {s_code}
    
    """

    # Send the code to Gemini
    start_time = time.perf_counter()
    response = client.models.generate_content(model=MODEL,contents=prompt)
    duration = time.perf_counter()-start_time

    if not response.text or not response.text.strip():
            raise RuntimeError("Gemini did not return a response.")

    # Get token usage information
    usage = response.usage_metadata

    if usage:
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_tokens = usage.total_token_count
        thought_tokens = usage.thoughts_token_count
    else:
        input_tokens = None
        output_tokens = None
        total_tokens = None

    return prompt,response.text,duration,input_tokens,output_tokens,total_tokens,thought_tokens

# Step 3: Save the review report
def save_report(review_request, prompt, raw_response, report_name, duration, assessment,
                input_tokens,output_tokens,total_tokens,thought_tokens): 
    Path("reviews").mkdir(exist_ok=True)

    # Prepare the report
    report = f"""
# Python Code Review Report

## Review Request
{review_request}

## Provider and Model
Provider: Google Gemini
Model: {MODEL}

## Outcome
Success

## Duration
{duration:.2f} seconds

## Token Usage
- Input tokens: {input_tokens if input_tokens is not None else "Unknown"}
- Output tokens: {output_tokens if output_tokens is not None else "Unknown"}
- Total tokens: {total_tokens if total_tokens is not None else "Unknown"}
- Thought tokens: {thought_tokens if thought_tokens is not None else "Unknown"}

## Prompt Sent to Gemini
{prompt}

## Raw Gemini Response
{raw_response}

## My Assessment
{assessment}
"""

    # Save the report
    report_path = Path("reviews") / report_name

    if report_path.exists():
            raise FileExistsError(
                "This report already exists. Choose another filename."
            )
    
    report_path.write_text(report, encoding="utf-8")
    print(f"Report saved to: {report_path}")

# Step 4: Run the program
def main():
    print("=== Python Code Review Tool ===")
    p_file = input("Enter the Python file path: ").strip()
    review_request = input("What do you want to investigate? ").strip()

    try:
        # Read the Python file
        s_code = read_s_file(p_file)

        # Get the AI review
        prompt,raw_response,duration,input_tokens,output_tokens,total_tokens,thought_tokens = review_code(s_code,review_request)

        # Ask for the report filename & assessment
        report_name = input("Enter report filename (e.g. request1_quantity.md): ").strip()

        if not report_name or Path(report_name).name != report_name:
            raise ValueError("Please enter a valid filename, not a folder path.")
        
        assessment = input("Enter your assessment of the findings: ").strip()
        # Save the report
        save_report(review_request,prompt,raw_response,report_name,duration,assessment,
                    input_tokens,output_tokens,total_tokens,thought_tokens)

        # Display the results
        print("\nReview completed!")
        print(f"Report saved to: reviews/{report_name}")
        print("\nAI Findings:")
        print(raw_response)

    except Exception as error:
        print("\nReview failed:", error)

# Start the program
if __name__ == "__main__":
    main()