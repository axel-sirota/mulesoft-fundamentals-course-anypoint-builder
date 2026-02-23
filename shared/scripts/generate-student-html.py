#!/usr/bin/env python3
"""
Generate student version of an instructor HTML notebook.

Strips all <details class="instructor-note">...</details> blocks and
the instructor-note CSS rules, producing a clean student-facing file.

Usage:
    python3 shared/scripts/generate-student-html.py modules/01-intro-to-mulesoft/module-01.html
    python3 shared/scripts/generate-student-html.py --all

The --all flag processes every module-NN.html found under modules/.
Output: module-NN-student.html in the same directory as the source.
"""

import argparse
import glob
import os
import re
import sys


def strip_instructor_notes(html: str) -> str:
    """Remove all <details class="instructor-note">...</details> blocks."""
    # Match the full <details class="instructor-note"> ... </details> block
    # Use DOTALL so . matches newlines
    pattern = r'\s*<details class="instructor-note">.*?</details>'
    return re.sub(pattern, '', html, flags=re.DOTALL)


def strip_instructor_css(html: str) -> str:
    """Remove CSS rules for .instructor-note inside the <style> block."""
    # Remove the details.instructor-note rule blocks
    # Match from "details.instructor-note" or "/* Instructor Notes */" to the closing }
    # Handle multi-rule blocks (details.instructor-note { ... } and child selectors)
    patterns = [
        r'\s*/\* Instructor Notes \*/\n',
        r'\s*details\.instructor-note\s*\{[^}]*\}',
        r'\s*details\.instructor-note\s+summary\s*\{[^}]*\}',
        r'\s*details\.instructor-note\s+ol[^{]*\{[^}]*\}',
        r'\s*details\.instructor-note\s+li\s*\{[^}]*\}',
        r'\s*details\.instructor-note\s+p\s*\{[^}]*\}',
        # Component card nested instructor notes
        r'\s*\.component-card\s+details\.instructor-note\s*\{[^}]*\}',
    ]
    for pat in patterns:
        html = re.sub(pat, '', html, flags=re.DOTALL)
    return html


def update_title(html: str) -> str:
    """Add '(Student)' to the <title> tag to distinguish versions."""
    return re.sub(
        r'<title>(.*?) — MuleSoft Basics</title>',
        r'<title>\1 — MuleSoft Basics (Student)</title>',
        html,
    )


def generate_student_version(instructor_path: str) -> str:
    """Generate student HTML from an instructor HTML file. Returns output path."""
    with open(instructor_path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = strip_instructor_notes(html)
    html = strip_instructor_css(html)
    html = update_title(html)

    # Clean up any resulting double blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    # Output path: module-NN.html -> module-NN-student.html
    base, ext = os.path.splitext(instructor_path)
    student_path = f"{base}-student{ext}"

    with open(student_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return student_path


def find_all_instructor_htmls() -> list:
    """Find all module-NN.html files (excluding -student.html)."""
    pattern = os.path.join('modules', '*', 'module-*.html')
    all_files = glob.glob(pattern)
    return [f for f in all_files if '-student' not in f]


def main():
    parser = argparse.ArgumentParser(
        description='Generate student versions of instructor HTML notebooks'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Instructor HTML file(s) to process',
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all module-NN.html files under modules/',
    )
    args = parser.parse_args()

    if args.all:
        files = find_all_instructor_htmls()
        if not files:
            print("No module HTML files found under modules/")
            sys.exit(1)
    elif args.files:
        files = args.files
    else:
        parser.print_help()
        sys.exit(1)

    for filepath in sorted(files):
        if not os.path.exists(filepath):
            print(f"SKIP: {filepath} (not found)")
            continue
        output = generate_student_version(filepath)
        # Count what was removed
        with open(filepath, 'r') as f:
            original = f.read()
        notes_count = len(re.findall(r'<details class="instructor-note">', original))
        print(f"OK: {filepath} -> {output} ({notes_count} instructor notes stripped)")


if __name__ == '__main__':
    main()
