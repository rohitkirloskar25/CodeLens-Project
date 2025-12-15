import os
import re
import sys
import google.generativeai as genai

# ============================================================
# CONFIGURATION
# ============================================================
# Reads API configuration from environment variables.
# This avoids hard-coding secrets and keeps the script CI/CD safe.

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Fail fast if the API key is missing
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def detect_language(filename: str) -> str:
    """
    Detects the programming language based on file extension.
    Only identifies the language, NOT the testing framework,
    ensuring framework-agnostic behavior.
    """
    ext = filename.split(".")[-1].lower()
    return {
        "py": "Python",
        "js": "JavaScript",
        "ts": "TypeScript",
        "java": "Java",
        "cpp": "C++",
        "c": "C",
        "go": "Go",
        "rs": "Rust",
    }.get(ext, "the same language")

def clean_output(text: str) -> str:
    """
    Cleans AI output to ensure only raw executable test code is returned.
    - Extracts code from markdown blocks if present
    - Removes comments and documentation artifacts
    - Makes output suitable for CI/CD pipelines
    """

    # Extract code if wrapped inside markdown fences
    code_block = re.search(r"```(?:[a-zA-Z]*)?\n([\s\S]*?)```", text)
    if code_block:
        text = code_block.group(1)

    # Remove block comments
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    text = re.sub(r"<!--[\s\S]*?-->", "", text)

    # Remove single-line comments safely
    text = re.sub(r"(^|[^:])//.*$", r"\1", text, flags=re.MULTILINE)
    text = re.sub(r"(^|[^:])#.*$", r"\1", text, flags=re.MULTILINE)

    return text.strip()

def read_source_files(root="."):
    """
    Recursively scans the project directory for supported source files.
    Ignores build artifacts, virtual environments, and dependencies.
    """
    sources = []
    ignored_dirs = {
        ".git",
        "node_modules",
        "dist",
        "build",
        "venv",
        "__pycache__",
    }

    for dirpath, _, files in os.walk(root):
        if any(ignored in dirpath for ignored in ignored_dirs):
            continue

        for file in files:
            if file.endswith((
                ".py", ".js", ".ts", ".java",
                ".cpp", ".c", ".go", ".rs"
            )):
                path = os.path.join(dirpath, file)
                with open(path, "r", errors="ignore") as f:
                    sources.append((file, f.read()))

    return sources

# ============================================================
# CORE LOGIC
# ============================================================

def generate_tests(source_code: str, language: str) -> str:
    """
    Sends source code to the AI model and generates unit tests.
    The prompt is intentionally framework-agnostic.
    """

    prompt = f"""
You are a senior QA engineer.

Generate COMPLETE unit test code for the following source code.

Rules:
- Use the SAME programming language as the source ({language})
- Automatically infer the most appropriate testing framework or standard library
- Follow idiomatic testing conventions for that ecosystem
- Reuse any existing testing patterns detected in the source
- Tests must be runnable without modification
- RETURN ONLY RAW TEST CODE
- NO MARKDOWN
- NO COMMENTS
- NO EXPLANATIONS

SOURCE CODE:
{source_code}
"""

    response = model.generate_content(prompt)
    return clean_output(response.text)

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    """
    Entry point for CLI / CI execution.
    Currently processes the first detected source file.
    Output is written to stdout for easy pipeline integration.
    """

    sources = read_source_files()

    if not sources:
        print("ERROR: No source files found", file=sys.stderr)
        sys.exit(1)

    filename, code = sources[0]
    language = detect_language(filename)

    tests = generate_tests(code, language)

    # CI tools (Jenkins/GitHub Actions) capture stdout
    print(tests)
