import argparse
import json
import re
from pathlib import Path


DEFAULT_LOG_PATH = Path("data/logs/corrupt_entries_log.json")
CODE_BLOCK_PATTERN = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def escape_inner_quotes(payload: str) -> str:
    """Escape bare quotation marks that appear inside JSON string values."""

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

                if next_char in {'}', ']'} or next_char == "":
                    in_string = False
                    string_is_key = False
                    result.append(char)
                    continue

                result.extend(("\\", '"'))
                continue

            result.append(char)
            continue

        # Not currently inside a string
        if char == '"':
            container = context_stack[-1] if context_stack else None
            container_type = container['type'] if container else None
            string_is_key = bool(
                container_type == 'object' and container.get('expecting_key', False)
            )
            in_string = True
            result.append(char)
            continue

        if char == '{':
            context_stack.append({'type': 'object', 'expecting_key': True})
        elif char == '}':
            if context_stack:
                context_stack.pop()
        elif char == '[':
            context_stack.append({'type': 'array'})
        elif char == ']':
            if context_stack:
                context_stack.pop()
        elif char == ':':
            if context_stack and context_stack[-1]['type'] == 'object':
                context_stack[-1]['expecting_key'] = False
        elif char == ',':
            if context_stack:
                top = context_stack[-1]
                if top['type'] == 'object':
                    top['expecting_key'] = True

        result.append(char)

    return "".join(result)

def extract_code_block(payload: str) -> str | None:
    match = CODE_BLOCK_PATTERN.search(payload)
    if match:
        return match.group(1).strip()
    return None


def clean_log(path: Path) -> int:
    entries = json.loads(path.read_text())
    updates = 0

    for entry in entries:
        raw = entry.get("raw_response", "")
        cleaned = escape_inner_quotes(raw)

        try:
            json.loads(cleaned)
        except json.JSONDecodeError as error:
            block = extract_code_block(raw)
            if block is None:
                raise ValueError(
                    f"Failed to normalise entry {entry.get('custom_id', 'unknown')}: {error}"
                ) from error

            cleaned = escape_inner_quotes(block)
            json.loads(cleaned)

        if cleaned != raw:
            entry["raw_response"] = cleaned
            updates += 1

    path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=4) + "\n"
    )

    return updates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Escape stray double quotes inside JSON string values"
    )
    parser.add_argument(
        "log_path",
        nargs="?",
        default=DEFAULT_LOG_PATH,
        type=Path,
        help="Path to the corrupt entries log (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    updates = clean_log(args.log_path)
    print(f"Updated {updates} entries in {args.log_path}")


if __name__ == "__main__":
    main()
