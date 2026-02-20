import sys
import subprocess

def ensure(pkg: str, import_name: str | None = None):
    name = import_name or pkg
    try:
        __import__(name)
        return
    except Exception:
        pass

    print(f"[BOOTSTRAP] Installing {pkg} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

def main():
    ensure("PySide6", "PySide6")
    from main import main as run
    run()

if __name__ == "__main__":
    main()
