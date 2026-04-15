#!/usr/bin/env python3
"""生成 release notes — 将上次 tag 到现在的 commit 消息写入 msg.txt"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "msg.txt"


def run_git(*args: str) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git"] + list(args), capture_output=True, text=True, cwd=ROOT,
        encoding="utf-8", errors="replace"
    )
    return result


def get_last_tag() -> str:
    result = run_git("describe", "--tags", "--abbrev=0")
    if result.returncode != 0:
        print("未找到任何 tag，将使用所有提交记录")
        return None
    return result.stdout.strip()


def main():
    last_tag = get_last_tag()

    if last_tag:
        range_ref = f"{last_tag}..HEAD"
        print(f"生成 release notes: {last_tag}..HEAD")
    else:
        range_ref = "HEAD"
        print("生成 release notes: 全部提交记录")

    result = run_git("log", range_ref, "--pretty=format:%s", "--no-merges", "--invert-grep", "--grep=^docs:")
    if result.returncode != 0:
        print(f"git log 失败: {result.stderr}")
        sys.exit(1)

    commits = result.stdout.strip()
    if not commits:
        print("没有新的提交记录")
        sys.exit(1)

    header = "# Release Notes\n\n"
    OUTPUT.write_text(header + commits + "\n", encoding="utf-8")
    print(f"已写入 {OUTPUT}")


if __name__ == "__main__":
    main()