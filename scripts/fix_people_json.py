"""
Fix JSON corruption in Pass 2 people normalization results.

Extracts and repairs malformed JSON from _raw_content fields.
"""

import json
import re
from pathlib import Path
from shutil import copy2


def escape_inner_quotes(payload: str) -> str:
    """
    Escape bare quotation marks that appear inside JSON string values.

    This is copied from fix_json_codex.py - your proven JSON repair function.
    """
    whitespace = " \t\r\n"
    result: list[str] = []
    context_stack: list[dict[str, object]] = []

    in_string = False
    escape_next = False
    string_is_key = False
    container_type: str | None = None

    payload_len = len(payload)

    for index, char in enumerate(payload):
        if in_string:
            if escape_next:
                result.append(char)
                escape_next = False
                continue

            if char == "\\":
                result.append(char)
                escape_next = True
                continue

            if char == '"':
                next_index = index + 1
                while next_index < payload_len and payload[next_index] in whitespace:
                    next_index += 1
                next_char = payload[next_index] if next_index < payload_len else ""

                if string_is_key:
                    if next_char == ':':
                        in_string = False
                        string_is_key = False
                        result.append(char)
                        if context_stack and context_stack[-1]['type'] == 'object':
                            context_stack[-1]['expecting_key'] = False
                    else:
                        result.extend(("\\", '"'))
                    continue

                # Value string handling
                if next_char == ',':
                    immediate = payload[next_index + 1] if next_index + 1 < payload_len else ""

                    if container_type == 'object':
                        if immediate and immediate not in whitespace:
                            result.extend(("\\", '"'))
                            continue

                        look_ahead = next_index + 1
                        while look_ahead < payload_len and payload[look_ahead] in whitespace:
                            look_ahead += 1
                        following = payload[look_ahead] if look_ahead < payload_len else ""

                        if following in {'"', '}'}:
                            in_string = False
                            string_is_key = False
                            result.append(char)
                        else:
                            result.extend(("\\", '"'))
                        continue

                    if container_type == 'array':
                        look_ahead = next_index + 1
                        while look_ahead < payload_len and payload[look_ahead] in whitespace:
                            look_ahead += 1
                        following = payload[look_ahead] if look_ahead < payload_len else ""
                        allowed = {'"', '{', '[', ']', 't', 'f', 'n'}
                        if immediate and immediate not in whitespace:
                            if following and (following.isdigit() or following in allowed or following == '-'):
                                in_string = False
                                string_is_key = False
                                result.append(char)
                            else:
                                result.extend(("\\", '"'))
                            continue

                        in_string = False
                        string_is_key = False
                        result.append(char)
                        continue

                    # Top-level string treated like object value
                    in_string = False
                    string_is_key = False
                    result.append(char)
                    continue

                if next_char in {'}', ']'}:
                    in_string = False
                    string_is_key = False
                    result.append(char)
                    continue

                result.extend(("\\", '"'))
            else:
                result.append(char)
        else:
            result.append(char)
            if char == '"':
                in_string = True
                if context_stack and context_stack[-1].get('type') == 'object':
                    if context_stack[-1].get('expecting_key', True):
                        string_is_key = True
                        context_stack[-1]['expecting_key'] = False

            if char in {'{', '['}:
                ctype = 'object' if char == '{' else 'array'
                context_stack.append({'type': ctype, 'expecting_key': True})
                container_type = ctype

            if char in {'}', ']'}:
                if context_stack:
                    context_stack.pop()
                    container_type = context_stack[-1]['type'] if context_stack else None
                    if container_type == 'object' and char == '}':
                        context_stack[-1]['expecting_key'] = True

    return ''.join(result)


def fix_file(file_path: Path) -> dict:
    """
    Fix a single Pass 2 result file if it contains JSON errors.

    Returns:
        dict with keys: fixed (bool), entries_count (int), error (str or None)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if this file needs fixing
        if not isinstance(data, list):
            return {"fixed": False, "entries_count": 0, "error": "Not a list"}

        if len(data) != 1:
            # File has multiple entries - probably already good
            return {"fixed": False, "entries_count": len(data), "error": "Already has multiple entries"}

        first_entry = data[0]
        if first_entry.get("unified_id") != "oops" or "_raw_content" not in first_entry:
            # Not an error wrapper
            return {"fixed": False, "entries_count": len(data), "error": "No error detected"}

        # This file needs fixing!
        print(f"\n🔧 Fixing {file_path.name}...")
        print(f"   Error was: {first_entry.get('_error', 'unknown')}")

        # Extract the raw content
        raw_content = first_entry["_raw_content"]

        # Apply the repair
        repaired = escape_inner_quotes(raw_content)

        # Validate it parses
        try:
            people_data = json.loads(repaired)
        except json.JSONDecodeError as e:
            return {"fixed": False, "entries_count": 0, "error": f"Repair failed: {e}"}

        if not isinstance(people_data, list):
            return {"fixed": False, "entries_count": 0, "error": "Repaired data is not a list"}

        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        copy2(file_path, backup_path)
        print(f"   ✓ Created backup: {backup_path.name}")

        # Write the repaired data
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(people_data, f, ensure_ascii=False, indent=2)

        print(f"   ✓ Repaired {len(people_data)} entries")

        return {"fixed": True, "entries_count": len(people_data), "error": None}

    except Exception as e:
        return {"fixed": False, "entries_count": 0, "error": f"Exception: {e}"}


def main():
    """
    Scan Pass 2 results directory and fix any corrupted JSON files.
    """
    results_dir = Path("database/in_progress/pass2_results")

    if not results_dir.exists():
        print(f"❌ Results directory not found: {results_dir}")
        return

    # Find all result files
    result_files = sorted(results_dir.glob("results_pass2_*.json"))

    if not result_files:
        print(f"❌ No result files found in {results_dir}")
        return

    print(f"📂 Found {len(result_files)} Pass 2 result files")
    print(f"🔍 Scanning for JSON corruption...\n")

    fixed_count = 0
    error_count = 0
    total_entries_recovered = 0

    for file_path in result_files:
        result = fix_file(file_path)

        if result["fixed"]:
            fixed_count += 1
            total_entries_recovered += result["entries_count"]
        elif result["error"] and "No error detected" not in result["error"] and "Already has multiple entries" not in result["error"]:
            error_count += 1
            print(f"❌ {file_path.name}: {result['error']}")

    print(f"\n" + "="*60)
    print(f"✅ Summary:")
    print(f"   Files scanned: {len(result_files)}")
    print(f"   Files repaired: {fixed_count}")
    print(f"   Entries recovered: {total_entries_recovered}")
    if error_count > 0:
        print(f"   Files with unrecoverable errors: {error_count}")
    print(f"="*60)

    if fixed_count > 0:
        print(f"\n💡 Backup files created with .backup extension")
        print(f"   You can safely delete them once you verify the repairs")


if __name__ == "__main__":
    main()
