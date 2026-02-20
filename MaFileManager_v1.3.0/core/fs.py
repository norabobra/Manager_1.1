from __future__ import annotations
import os

def list_mafiles(folder: str) -> list[str]:
    if not folder or not os.path.exists(folder):
        return []
    out: list[str] = []
    for name in os.listdir(folder):
        low = name.lower()
        if low.endswith(".mafile") or low.endswith(".mafiles"):
            out.append(name)
    for name in os.listdir(folder):
        if name.endswith(".maFile") or name.endswith(".maFiles"):
            if name not in out:
                out.append(name)
    return sorted(out)

def remove_mafile_extension(filename: str) -> str:
    for ext in [".mafile", ".mafiles", ".maFile", ".maFiles"]:
        if filename.lower().endswith(ext.lower()):
            return filename[: -len(ext)]
    return os.path.splitext(filename)[0]
