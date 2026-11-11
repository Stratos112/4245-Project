#!/usr/bin/env python3
"""
Dump a Claude Code session JSONL to a formatted markdown chat log.

Usage:
    python dump_chat_log.py                        # most recent session, cwd
    python dump_chat_log.py /path/to/project       # most recent session, given project
    python dump_chat_log.py . <session-id-prefix>  # specific session by ID prefix

Output: chat-logs/<date>-<session-id-prefix>.md
"""

import json
import sys
from pathlib import Path


def project_key(project_dir: Path) -> str:
    return str(project_dir).replace("/", "-")


def find_sessions(project_dir: Path) -> list[Path]:
    store = Path.home() / ".claude" / "projects" / project_key(project_dir)
    if not store.exists():
        return []
    return sorted(store.glob("*.jsonl"))


def render_content(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    parts = []
    for block in content:
        if not isinstance(block, dict):
            continue
        match block.get("type"):
            case "text":
                text = block.get("text", "").strip()
                if text:
                    parts.append(text)
            case "tool_use":
                name = block.get("name", "?")
                inp = block.get("input", {})
                detail = inp.get("description") or inp.get("command") or inp.get("file_path") or ""
                if detail:
                    parts.append(f"*[{name}: {detail[:80]}]*")
                else:
                    parts.append(f"*[{name}]*")
            case "thinking" | "tool_result":
                pass  # skip
    return "\n\n".join(parts)


def parse_session(path: Path) -> list[dict]:
    messages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") not in ("user", "assistant"):
                continue
            msg = obj.get("message", {})
            content = render_content(msg.get("content", ""))
            if not content:
                continue
            messages.append({
                "role": obj["type"],
                "timestamp": obj.get("timestamp", ""),
                "session_id": obj.get("sessionId", path.stem),
                "content": content,
            })
    return messages


def build_markdown(session_path: Path, messages: list[dict]) -> str:
    session_id = messages[0]["session_id"] if messages else session_path.stem
    date = (messages[0]["timestamp"] or "")[:10] or "unknown"

    lines = [
        "# Chat Log\n",
        "| Field | Value |",
        "|---|---|",
        f"| Date | {date} |",
        f"| Session ID | {session_id} |",
        f"| Source | {session_path} |",
        "",
    ]

    for msg in messages:
        label = "Sky" if msg["role"] == "user" else "Claude"
        lines.append(f"---\n\n## {label} — {msg['timestamp']}\n")
        lines.append(msg["content"])
        lines.append("")

    lines.append("---")
    return "\n".join(lines)


def main():
    project_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    sessions = find_sessions(project_dir)

    if not sessions:
        sys.exit(f"No Claude Code sessions found for: {project_dir}")

    if len(sys.argv) > 2:
        prefix = sys.argv[2]
        matched = [s for s in sessions if s.stem.startswith(prefix)]
        if not matched:
            sys.exit(f"No session matching prefix: {prefix}")
        session_path = matched[0]
    else:
        session_path = sessions[-1]

    print(f"Session: {session_path.name}")
    messages = parse_session(session_path)

    if not messages:
        sys.exit("No messages found in session.")

    md = build_markdown(session_path, messages)

    out_dir = project_dir / "chat-logs"
    out_dir.mkdir(exist_ok=True)

    date = (messages[0]["timestamp"] or "")[:10] or "unknown"
    out_path = out_dir / f"{date}-{session_path.stem[:8]}.md"
    out_path.write_text(md)
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
