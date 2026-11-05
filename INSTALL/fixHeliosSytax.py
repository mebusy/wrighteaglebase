#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Migrate std::binary_function to C++17-compatible using declarations.

Default mode: dry-run, no files modified.
Apply changes: python3 fixHeliosSytax.py --apply

Example:
    struct ScoreCmp
        : public std::binary_function<Course, Course, bool>
    {
        ...
    };

Becomes:
    struct ScoreCmp
    {
    public:
        using first_argument_type = Course;
        using second_argument_type = Course;
        using result_type = bool;

        ...
    };
"""

from pathlib import Path
import argparse
import difflib
import re
import shutil
import sys

DEFAULT_EXTENSIONS = {
    ".h",
    ".hh",
    ".hpp",
    ".hxx",
    ".cpp",
    ".cc",
    ".cxx",
}

EXCLUDED_DIRS = {
    ".git",
    ".svn",
    ".hg",
    "build",
    "dist",
    "autom4te.cache",
}


# Match std::binary_function with optional access specifier.
BASE_PATTERN = re.compile(
    r"(?:(?:virtual\s+)?(?:public|protected|private)\s+)?"
    r"std\s*::\s*binary_function\s*<"
)


def skip_comment_or_string(source, pos):
    """Skip C++ comments and ordinary string/character literals."""

    n = len(source)

    if source.startswith("//", pos):
        end = source.find("\n", pos)
        return n if end < 0 else end

    if source.startswith("/*", pos):
        end = source.find("*/", pos + 2)
        return n if end < 0 else end + 2

    if source[pos] in ('"', "'"):
        quote = source[pos]
        i = pos + 1

        while i < n:
            if source[i] == "\\":
                i += 2
                continue

            if source[i] == quote:
                return i + 1

            i += 1

        return n

    return pos


def find_matching_angle(source, open_pos):
    """
    Find matching '>' for a template '<'.

    Supports nested templates, for example:
        std::binary_function<
            std::pair<int, double>,
            std::vector<Course>,
            bool
        >
    """

    depth = 1
    i = open_pos + 1
    n = len(source)

    while i < n:
        skipped = skip_comment_or_string(source, i)

        if skipped != i:
            i = skipped
            continue

        ch = source[i]

        if ch == "<":
            depth += 1

        elif ch == ">":
            depth -= 1

            if depth == 0:
                return i

        i += 1

    return -1


def split_template_arguments(text):
    """Split template arguments at top-level commas."""

    args = []
    start = 0

    angle = 0
    paren = 0
    bracket = 0
    brace = 0

    i = 0

    while i < len(text):
        skipped = skip_comment_or_string(text, i)

        if skipped != i:
            i = skipped
            continue

        ch = text[i]

        if ch == "<":
            angle += 1
        elif ch == ">":
            angle -= 1
        elif ch == "(":
            paren += 1
        elif ch == ")":
            paren -= 1
        elif ch == "[":
            bracket += 1
        elif ch == "]":
            bracket -= 1
        elif ch == "{":
            brace += 1
        elif ch == "}":
            brace -= 1

        elif ch == "," and angle == 0 and paren == 0 and bracket == 0 and brace == 0:
            args.append(text[start:i].strip())
            start = i + 1

        i += 1

    args.append(text[start:].strip())

    return args


def find_matching_brace(source, open_pos):
    """Find matching class-body closing brace."""

    depth = 1
    i = open_pos + 1
    n = len(source)

    while i < n:
        skipped = skip_comment_or_string(source, i)

        if skipped != i:
            i = skipped
            continue

        if source[i] == "{":
            depth += 1

        elif source[i] == "}":
            depth -= 1

            if depth == 0:
                return i

        i += 1

    return -1


def find_class_body(source, inheritance_end):
    """
    Find the class opening brace after the inheritance declaration.

    Skip comments and strings.
    """

    i = inheritance_end
    n = len(source)

    while i < n:
        skipped = skip_comment_or_string(source, i)

        if skipped != i:
            i = skipped
            continue

        ch = source[i]

        if ch == "{":
            return i

        # A class declaration ending without a body.
        if ch == ";":
            return -1

        i += 1

    return -1


def has_existing_alias(body, alias):
    """Check whether the class already declares an alias."""

    pattern = re.compile(
        r"\busing\s+" + re.escape(alias) + r"\s*="
        r"|\btypedef\b[^;]*\b" + re.escape(alias) + r"\s*;"
    )

    return bool(pattern.search(body))


def build_alias_block(args, body):
    names = [
        "first_argument_type",
        "second_argument_type",
        "result_type",
    ]

    lines = ["", "public:"]

    for name, value in zip(names, args):
        if not has_existing_alias(body, name):
            lines.append(f"    using {name} = {value};")

    if len(lines) == 2:
        return ""

    lines.append("")

    return "\n".join(lines)


def remove_base_specifier(source, start, end):
    """
    Remove the binary_function base while preserving other bases.

    Examples:

        : public binary_function<A, B, R>
        ->

        : public Base, public binary_function<A, B, R>
        ->
        : public Base

        : public binary_function<A, B, R>, public Base
        ->
        : public Base
    """

    left = start - 1

    while left >= 0 and source[left].isspace():
        left -= 1

    right = end

    while right < len(source) and source[right].isspace():
        right += 1

    # If it is not the first base, remove the preceding comma.
    if left >= 0 and source[left] == ",":
        return source[:left] + source[end:]

    # First base, but another base follows.
    if right < len(source) and source[right] == ",":
        return source[:start] + source[right + 1 :]

    # The only base: remove the inheritance colon as well.
    if left >= 0 and source[left] == ":":
        return source[:left] + source[end:]

    return source[:start] + source[end:]


def migrate_file(source):
    """
    Migrate all supported binary_function occurrences in one file.

    Returns:
        updated_source, changes, errors
    """

    changes = 0
    errors = []

    # Work from right to left so offsets remain valid.
    matches = list(BASE_PATTERN.finditer(source))

    for match in reversed(matches):
        start = match.start()
        open_angle = match.end() - 1

        close_angle = find_matching_angle(source, open_angle)

        if close_angle < 0:
            errors.append(f"Cannot match template brackets at offset {start}")
            continue

        args = split_template_arguments(source[open_angle + 1 : close_angle])

        if len(args) != 3 or any(not arg for arg in args):
            errors.append(
                f"Expected 3 template arguments at offset {start}; "
                f"found {len(args)}"
            )
            continue

        inheritance_end = close_angle + 1
        body_start = find_class_body(source, inheritance_end)

        if body_start < 0:
            errors.append(f"Cannot locate class body at offset {start}")
            continue

        body_end = find_matching_brace(source, body_start)

        if body_end < 0:
            errors.append(f"Cannot locate class closing brace at offset {body_start}")
            continue

        body = source[body_start + 1 : body_end]
        alias_block = build_alias_block(args, body)

        # Remove the base first, then adjust the body offset for the removed text.
        updated_source = remove_base_specifier(source, start, inheritance_end)
        body_start += len(updated_source) - len(source)
        source = updated_source

        if alias_block:
            insert_pos = body_start + 1
            source = source[:insert_pos] + alias_block + source[insert_pos:]

        changes += 1

    return source, changes, errors


def collect_files(root, extensions):
    result = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix.lower() not in extensions:
            continue

        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        result.append(path)

    return sorted(result)


def main():
    parser = argparse.ArgumentParser(
        description="Migrate std::binary_function for C++17."
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually modify files. Default is dry-run.",
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create .bak files (not recommended).",
    )

    parser.add_argument(
        "--extensions",
        default=",".join(sorted(DEFAULT_EXTENSIONS)),
        help="Comma-separated source file extensions",
    )

    args = parser.parse_args()

    root = Path(args.root).resolve()

    if not root.is_dir():
        print(f"ERROR: Directory not found: {root}")
        sys.exit(1)

    extensions = {
        (
            ext.strip().lower()
            if ext.strip().startswith(".")
            else "." + ext.strip().lower()
        )
        for ext in args.extensions.split(",")
        if ext.strip()
    }

    files = collect_files(root, extensions)

    total_files = 0
    total_changes = 0
    total_errors = 0

    for path in files:
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            print(f"[SKIP] {path}: {exc}")
            continue

        if "std::binary_function" not in original:
            continue

        updated, changes, errors = migrate_file(original)

        if errors:
            total_errors += len(errors)

            for error in errors:
                print(f"[ERROR] {path}: {error}")

        if changes == 0 or updated == original:
            continue

        total_files += 1
        total_changes += changes

        print(f"\n[FOUND] {path}")
        print(f"  Occurrences: {changes}")

        diff = difflib.unified_diff(
            original.splitlines(),
            updated.splitlines(),
            fromfile=str(path),
            tofile=str(path) + " (migrated)",
            lineterm="",
        )

        for line in diff:
            print(line)

        if args.apply:
            backup = path.with_suffix(path.suffix + ".bak")

            if not args.no_backup:
                if backup.exists():
                    print(f"[SKIP] Backup already exists: {backup}")
                    print("       Remove it manually before retrying.")
                    continue

                shutil.copy2(path, backup)

            path.write_text(updated, encoding="utf-8")

            print(f"[APPLIED] {path}")

    print("\n========== Summary ==========")
    print(f"Files scanned:       {len(files)}")
    print(f"Files to modify:     {total_files}")
    print(f"Occurrences found:   {total_changes}")
    print(f"Parsing errors:      {total_errors}")

    if args.apply:
        print("Mode: APPLY")
    else:
        print("Mode: DRY-RUN")
        print("No files were modified.")
        print("\nRun with --apply to apply the changes.")

    if total_errors:
        print("\nWARNING: Some occurrences need manual inspection.")
        sys.exit(2)


if __name__ == "__main__":
    main()
