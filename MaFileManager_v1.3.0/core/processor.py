from __future__ import annotations
import os
import json
import shutil
from typing import Callable

LogCb = Callable[[str, str], None]
ProgressCb = Callable[[int, str], None]

class MaFileProcessor:
    def __init__(self, log: LogCb, progress: ProgressCb):
        self.log = log
        self.progress = progress

    def process_mode1(self, folder: str, files: list[str]) -> str:
        out_dir = os.path.join(folder, "fullmafiles")
        os.makedirs(out_dir, exist_ok=True)
        total = len(files)
        ok = 0
        for i, fn in enumerate(files, 1):
            path = os.path.join(folder, fn)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                acc = data.get("account_name", "")
                if not acc:
                    self.log(f"{fn}: нет account_name", "warning")
                else:
                    shutil.copy2(path, os.path.join(out_dir, f"{acc}.maFile"))
                    ok += 1
            except Exception as e:
                self.log(f"{fn}: {e}", "error")
            self.progress(int(i * 100 / max(1, total)), f"Файл {i}/{total}")
        self.log(f"Режим 1: {ok}/{total} файлов", "success")
        return out_dir

    def process_mode2(self, folder: str, files: list[str]) -> str:
        out_dir = os.path.join(folder, "shortmaffsmpanel")
        os.makedirs(out_dir, exist_ok=True)
        total = len(files)
        ok = 0
        for i, fn in enumerate(files, 1):
            path = os.path.join(folder, fn)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                trimmed = {
                    "shared_secret": data.get("shared_secret", ""),
                    "account_name": data.get("account_name", ""),
                    "Session": {"SteamID": data.get("Session", {}).get("SteamID", "")},
                }
                acc = trimmed["account_name"]
                if acc and trimmed["shared_secret"] and trimmed["Session"]["SteamID"]:
                    with open(os.path.join(out_dir, f"{acc}.maFile"), "w", encoding="utf-8") as f:
                        json.dump(trimmed, f, indent=2, ensure_ascii=False)
                    ok += 1
                else:
                    self.log(f"{fn}: неполные данные", "warning")
            except Exception as e:
                self.log(f"{fn}: {e}", "error")
            self.progress(int(i * 100 / max(1, total)), f"Файл {i}/{total}")
        self.log(f"Режим 2: {ok}/{total} файлов", "success")
        return out_dir

    def process_mode3(self, folder: str, files: list[str]) -> str:
        out_dir = os.path.join(folder, "shortmafdmpanel")
        os.makedirs(out_dir, exist_ok=True)
        total = len(files)
        ok = 0
        for i, fn in enumerate(files, 1):
            path = os.path.join(folder, fn)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                secret = data.get("shared_secret", "")
                steamid = data.get("Session", {}).get("SteamID", "")
                acc = data.get("account_name", "")
                if secret and steamid and acc:
                    trimmed = {"shared_secret": secret, "Session": {"SteamID": steamid}}
                    with open(os.path.join(out_dir, f"{acc}.maFile"), "w", encoding="utf-8") as f:
                        json.dump(trimmed, f, indent=4, ensure_ascii=False)
                    ok += 1
                else:
                    self.log(f"{fn}: неполные данные", "warning")
            except Exception as e:
                self.log(f"{fn}: {e}", "error")
            self.progress(int(i * 100 / max(1, total)), f"Файл {i}/{total}")
        self.log(f"Режим 3: {ok}/{total} файлов", "success")
        return out_dir
