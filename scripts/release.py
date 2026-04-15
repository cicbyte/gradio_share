#!/usr/bin/env python3
"""版本发布脚本 — 自动升级版本号、提交、打标签并推送"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "VERSION"
MSG_FILE = ROOT / "msg.txt"


def read_version() -> str:
    return VERSION_FILE.read_text().strip()


def write_version(version: str) -> None:
    VERSION_FILE.write_text(version)


def bump_version(current: str) -> str:
    parts = current.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        print(f"错误: 当前版本号格式不正确: {current}，期望 MAJOR.MINOR.PATCH")
        sys.exit(1)
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if patch == 9:
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git"] + list(args), capture_output=True, text=True, check=False
    )
    if check and result.returncode != 0:
        print(f"git {' '.join(args)} 失败:\n{result.stderr}")
        sys.exit(1)
    return result


def main():
    parser = argparse.ArgumentParser(description="版本发布脚本")
    parser.add_argument("version", nargs="?", help="手动指定版本号，例如 2.0.0")
    args = parser.parse_args()

    old_version = read_version()

    if args.version:
        new_version = args.version.lstrip("v")
        if not re.match(r"^\d+\.\d+\.\d+$", new_version):
            print(f"错误: 版本号格式不正确: {args.version}，期望 MAJOR.MINOR.PATCH")
            sys.exit(1)
    else:
        new_version = bump_version(old_version)

    if new_version == old_version:
        print(f"版本号未变化: {old_version}")
        sys.exit(1)

    print(f"版本升级: {old_version} → {new_version}")

    # 读取 release notes
    if not MSG_FILE.exists():
        print("错误: 未找到 msg.txt，请先运行 python gen_release_notes.py")
        sys.exit(1)

    release_notes = MSG_FILE.read_text(encoding="utf-8").strip()
    MSG_FILE.unlink()
    print("已读取并删除 msg.txt")

    # 写入新版本号
    write_version(new_version)

    # 提交
    run_git("add", "VERSION")
    run_git("commit", "-m", release_notes)
    print("已提交")

    # 推送
    run_git("push")
    print("已推送")

    # 打标签并推送
    tag = f"v{new_version}"
    run_git("tag", tag)
    run_git("push", "origin", tag)
    print(f"已创建并推送标签: {tag}")


if __name__ == "__main__":
    main()