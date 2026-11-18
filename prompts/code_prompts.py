"""
Code explanation, review, and documentation prompt templates for AI WriteMate.
Covers code walkthroughs, refactoring, docstrings, bug debugging, and algorithmic analysis.
"""

from typing import Optional

CODE_SYSTEM_INSTRUCTION = """
You are a Principal Software Architect, expert code reviewer, and technical educator.
Your goal is to explain code with crystal clarity, provide actionable code reviews, and produce idiomatic documentation.
Key guidelines:
1. Always specify language syntax highlighting using markdown code blocks (e.g. ```python, ```javascript).
2. Balance high-level architecture with line-by-line nuance depending on user request.
3. Highlight algorithmic complexity (Big-O time and space) where relevant.
4. Adhere to security best practices and language-specific conventions (PEP 8 for Python, ESLint for JS/TS, etc.).
5. Provide working, refactored snippets rather than abstract pseudo-code whenever possible.
""".strip()


def build_code_explanation_prompt(
    code_snippet: str,
    language: str = "Auto-detect",
    target_audience: str = "Junior Developer",
    detail_level: str = "Step-by-step walkthrough",
) -> str:
    """Builds a structured prompt to explain a block of code."""
    return f"""
Explain the following code snippet thoroughly.

PROGRAMMING LANGUAGE: {language}
TARGET AUDIENCE: {target_audience}
EXPLANATION LEVEL: {detail_level}

CODE TO EXPLAIN:
```
{code_snippet}
```

STRUCTURE YOUR EXPLANATION AS FOLLOWS:
1. High-Level Summary: What problem does this code solve in plain English?
2. Step-by-Step Breakdown: Walk through key functions, logic branches, and data transformations.
3. Time & Space Complexity: Big-O analysis of execution and memory.
4. Edge Cases & Caveats: What could cause this to fail (null checks, boundary conditions, concurrency)?
""".strip()


def build_code_review_prompt(
    code_snippet: str,
    language: str = "Auto-detect",
    focus_areas: Optional[str] = None,
) -> str:
    """Performs a thorough code review checking bugs, performance, security, and cleanliness."""
    focus_section = f"SPECIAL FOCUS: {focus_areas}\n" if focus_areas else ""

    return f"""
Perform a comprehensive code review on the snippet below.

LANGUAGE: {language}
{focus_section}
CODE:
```
{code_snippet}
```

PROVIDE STRUCTURED FEEDBACK ACROSS THESE CATEGORIES:
1. Bugs & Logic Errors: Any runtime errors, off-by-one errors, or improper exception handling.
2. Performance & Efficiency: Bottlenecks, unnecessary loops, or memory waste.
3. Security Concerns: Vulnerabilities (e.g., injections, leaks, unsafe deserialization).
4. Readability & Idiomatic Style: Naming conventions, documentation, adherence to standards.
5. Improved Implementation: The complete refactored code block with your fixes applied.
""".strip()


def build_docstring_and_comments_prompt(
    code_snippet: str,
    language: str = "Python",
    doc_style: str = "Google Style (Args, Returns, Raises)",
) -> str:
    """Generates comprehensive docstrings and inline comments for undocumented code."""
    return f"""
Add clean, comprehensive documentation to the following code snippet.

LANGUAGE: {language}
DOCSTRING STYLE: {doc_style}

ORIGINAL CODE:
```
{code_snippet}
```

REQUIREMENTS:
- Add a top-level module/class/function docstring explaining the purpose.
- Detail all parameters with types and descriptions.
- Detail return values and exceptions/errors raised.
- Add minimal, high-value inline comments explaining non-trivial logic.
- Return the full updated code snippet in a syntax-highlighted code block.
""".strip()


def build_bug_debugging_prompt(
    code_snippet: str,
    error_message: Optional[str] = None,
    expected_vs_actual: Optional[str] = None,
) -> str:
    """Diagnoses a bug given code and optional error tracebacks."""
    err_section = f"ERROR MESSAGE / STACK TRACE:\n{error_message}\n" if error_message else "No traceback provided.\n"
    exp_section = f"EXPECTED VS ACTUAL BEHAVIOR:\n{expected_vs_actual}\n" if expected_vs_actual else ""

    return f"""
Diagnose and resolve the bug in this code.

CODE:
```
{code_snippet}
```

{err_section}
{exp_section}
PLEASE PROVIDE:
1. Root Cause Analysis: Exactly what is triggering the error or incorrect behavior.
2. The Fix: Explanation of what needs to be changed.
3. Corrected Code: Complete, working snippet with the fix applied.
4. Prevention Tip: How to avoid this class of bugs in the future (e.g. unit test, type annotations).
""".strip()
