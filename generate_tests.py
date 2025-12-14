import os
import re
import sys
import google.generativeai as genai

# ---------------- CONFIG ----------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ---------------- UTILS ----------------
def detect_language(filename: str) -> str:
    ext = filename.split(".")[-1]
    return {
        "py": "Python (pytest)",
        "js": "JavaScript (Jest)",
        "ts": "TypeScript (Jest)",
        "java": "Java (JUnit)",
        "cpp": "C++ (GoogleTest)",
        "c": "C (Unity)",
        "go": "Go (testing)",
        "rs": "Rust (cargo test)",
    }.get(ext, "the same language")


def clean_output(text: str) -> str:
    match = re.search(r"```(?:[a-zA-Z]*)?\n([\s\S]*?)```", text)
    if match:
        text = match.group(1)

    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    text = re.sub(r"(^|[^:])//.*$", r"\1", text, flags=re.MULTILINE)
    text = re.sub(r"(^|[^:])#.*$", r"\1", text, flags=re.MULTILINE)

    return text.strip()


def read_source_files(root="."):
    sources = []
    for dirpath, _, files in os.walk(root):
        if any(x in dirpath for x in [".git", "node_modules", "dist", "build", "venv"]):
            continue

        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs")):
                path = os.path.join(dirpath, file)
                with open(path, "r", errors="ignore") as f:
                    sources.append((file, f.read()))
    return sources


# ---------------- CORE ----------------
def generate_tests(source_code: str, language: str) -> str:
    prompt = f"""
You are a senior QA engineer.

Generate COMPLETE unit test code for the following source.
Use best practices for {language}.

STRICT RULES:
- RETURN ONLY RAW TEST CODE
- NO MARKDOWN
- NO COMMENTS
- NO EXPLANATIONS

SOURCE CODE:
{source_code}
"""
    response = model.generate_content(prompt)
    return clean_output(response.text)


# ---------------- ENTRY ----------------
if __name__ == "__main__":
    sources = read_source_files()

    if not sources:
        print("ERROR: No source files found", file=sys.stderr)
        sys.exit(1)

    # For now: generate tests for the first source file
    filename, code = sources[0]
    language = detect_language(filename)

    tests = generate_tests(code, language)

    # Jenkins will capture stdout
    print(tests)
