from __future__ import annotations
import os
import json
from typing import Callable
from .fs import remove_mafile_extension

LogCb = Callable[[str, str], None]
ProgressCb = Callable[[int, str], None]

class AsfConverter:
    def __init__(self, log: LogCb, progress: ProgressCb):
        self.log = log
        self.progress = progress

    def _parse_logpass(self, path: str) -> dict[str, str]:
        encs = ["utf-8", "cp1251", "latin-1", "iso-8859-1", "utf-16", "cp866"]
        for enc in encs:
            try:
                out: dict[str, str] = {}
                with open(path, "r", encoding=enc) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        for delim in [":", ";", ",", "|", " ", "\t"]:
                            if delim in line:
                                login, pwd = line.split(delim, 1)
                                login, pwd = login.strip(), pwd.strip()
                                if login and pwd:
                                    out[login] = pwd
                                break
                if out:
                    return out
            except Exception:
                continue
        return {}

    def _find_best_match(self, steam_id: str, filename: str, logpass: dict[str, str]):
        fn = remove_mafile_extension(filename).strip()
        sid = str(steam_id).strip()
        variants = {sid, fn}

        if sid.startswith("7656119"):
            variants.update([sid[7:], sid[3:], sid[-8:], sid[-10:], sid[-12:]])

        for sep in ["_", "-", ".", " ", "__", "--", ".."]:
            if sep in fn:
                parts = [p for p in fn.split(sep) if p]
                variants.update(parts)
                if parts:
                    variants.add(parts[0])
                    variants.add(parts[-1])

        for v in variants:
            if v in logpass:
                return v, logpass[v]

        sid_l = sid.lower()
        fn_l = fn.lower()
        for login, pwd in logpass.items():
            lc = login.strip().lower()
            if lc in sid_l or sid_l in lc or lc in fn_l or fn_l in lc:
                return login, pwd

        return None, None

    def convert(self, mafiles_paths: list[str], logpass_path: str, output_folder: str | None):
        out_dir = output_folder or "ASFmaFiles"
        os.makedirs(out_dir, exist_ok=True)

        logpass = self._parse_logpass(logpass_path)
        if not logpass:
            raise ValueError("В файле не найдено корректных записей login:password")

        self.log(f"Загружено {len(logpass)} записей из файла с логинами", "info")
        available = dict(logpass)

        total = len(mafiles_paths)
        ok = 0
        failed: list[tuple[str, str]] = []

        ma_data = []
        for p in mafiles_paths:
            fn = os.path.basename(p)
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                steam_id = data.get("account_name") or data.get("Session", {}).get("SteamID") or remove_mafile_extension(fn)
                ma_data.append({"path": p, "filename": fn, "steam_id": steam_id, "data": data})
            except Exception as e:
                failed.append((fn, f"Ошибка чтения: {e}"))
                self.log(f"[ОШИБКА ЧТЕНИЯ] {fn} - {e}", "error")

        remaining = []
        for i, item in enumerate(ma_data, 1):
            fn = item["filename"]
            sid = item["steam_id"]
            login, pwd = self._find_best_match(sid, fn, available)
            if login and pwd:
                try:
                    safe = str(sid).replace(":", "_").replace("/", "_").replace("\\", "_")
                    with open(os.path.join(out_dir, f"{safe}.maFile"), "w", encoding="utf-8") as f:
                        json.dump(item["data"], f, indent=2, ensure_ascii=False)
                    cfg = {"Enabled": True, "OnlineStatus": 7, "RemoteCommunication": 0, "SteamLogin": login, "SteamPassword": pwd}
                    with open(os.path.join(out_dir, f"{safe}.json"), "w", encoding="utf-8") as f:
                        json.dump(cfg, f, indent=4, ensure_ascii=False)

                    ok += 1
                    self.log(f"[УСПЕХ] {fn} -> Логин: {login}", "success")
                    available.pop(login, None)
                except Exception as e:
                    failed.append((fn, f"Ошибка обработки: {e}"))
                    self.log(f"[ОШИБКА ОБРАБОТКИ] {fn} - {e}", "error")
            else:
                remaining.append(item)

            self.progress(int(i * 60 / max(1, total)), f"Матчинг {i}/{total}")

        if remaining and available:
            self.log(f"Осталось {len(remaining)} файлов и {len(available)} логинов", "info")
            self.log("Назначаем оставшиеся логины по порядку...", "info")
            avail_list = list(available.items())
            for j, item in enumerate(remaining, 1):
                fn = item["filename"]
                sid = item["steam_id"]
                if j - 1 < len(avail_list):
                    login, pwd = avail_list[j - 1]
                    try:
                        safe = str(sid).replace(":", "_").replace("/", "_").replace("\\", "_")
                        with open(os.path.join(out_dir, f"{safe}.maFile"), "w", encoding="utf-8") as f:
                            json.dump(item["data"], f, indent=2, ensure_ascii=False)
                        cfg = {"Enabled": True, "OnlineStatus": 7, "RemoteCommunication": 0, "SteamLogin": login, "SteamPassword": pwd}
                        with open(os.path.join(out_dir, f"{safe}.json"), "w", encoding="utf-8") as f:
                            json.dump(cfg, f, indent=4, ensure_ascii=False)
                        ok += 1
                        self.log(f"[УСПЕХ-АВТО] {fn} -> Логин: {login}", "success")
                    except Exception as e:
                        failed.append((fn, f"Ошибка авто-обработки: {e}"))
                        self.log(f"[ОШИБКА АВТО-ОБРАБОТКИ] {fn} - {e}", "error")
                else:
                    failed.append((fn, "Не хватает логинов"))
                    self.log(f"[НЕ ХВАТАЕТ ЛОГИНОВ] {fn}", "warning")
                self.progress(60 + int(j * 40 / max(1, len(remaining))), f"Запись {j}/{len(remaining)}")

        self.progress(100, "Готово!")
        self.log(f"Конвертация завершена. Успешно: {ok}/{total}", "success")
        return {"success": ok, "failed": failed, "output_folder": out_dir}
