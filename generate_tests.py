import os
import re
import sys
import google.generativeai as genai

# ============================================================
# CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ============================================================
# UTILITIES
# ============================================================

def clean_output(text: str) -> str:
    """
    Cleans output to ensure strictly raw code is returned.
    """
    # 1. Extract code from markdown blocks if present
    code_block = re.search(r"```(?:[a-zA-Z]*)?\n([\s\S]*?)```", text)
    if code_block:
        text = code_block.group(1)

    # 2. Aggressively strip comments (Strict Enforcement)
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)        # Block comments
    text = re.sub(r"", "", text)       # HTML/XML comments
    text = re.sub(r"(^|[^:])//.*$", r"\1", text, flags=re.MULTILINE) # Single line (C/JS)
    text = re.sub(r"(^|[^:])#.*$", r"\1", text, flags=re.MULTILINE)  # Single line (Py/Bash)

    return text.strip()

def reject_non_test_artifacts(text: str) -> None:
    """
    Guardrail to ensure no CI/CD or Docker configs leak into test files.
    """
    forbidden = [
        "pipeline {", "agent any", "stages {",
        "jobs:", "runs-on:", "trigger:",
        "FROM ", "CMD ", "ENTRYPOINT"
    ]

    if any(x in text for x in forbidden):
        raise RuntimeError("Invalid artifact detected in test output")

# ============================================================
# CORE LOGIC
# ============================================================

def generate_tests_from_source(source_code: str) -> str:
    prompt = f"""
You are an automated test generation engine.

TASK:
- Identify the programming language used in the SOURCE CODE
- Generate COMPLETE UNIT TEST SOURCE CODE in the SAME language
- Automatically choose the appropriate unit testing framework

STRICT RULES:
- Output MUST be a unit test source file
- Output MUST be written in the SAME language as the input
- Include only necessary imports required by the testing framework
- RETURN ONLY raw test source code
- NO markdown
- NO comments
- NO explanations

SOURCE CODE:
{source_code}
"""
    response = model.generate_content(prompt)
    output = clean_output(response.text)
    reject_non_test_artifacts(output)
    return output

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    source_code = ""

    # COMPATIBILITY FIX: Check for filename argument first (for Jenkins)
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, "r", errors="ignore") as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"ERROR: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)

    # Fallback: Check for piped input (STDIN)
    elif not sys.stdin.isatty():
        source_code = sys.stdin.read()

    else:
        print("ERROR: No input provided. Pass a file as argument or pipe content via STDIN.", file=sys.stderr)
        sys.exit(1)

    if not source_code.strip():
        print("ERROR: Source code input is empty", file=sys.stderr)
        sys.exit(1)

    try:
        tests = generate_tests_from_source(source_code)
        print(tests)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
