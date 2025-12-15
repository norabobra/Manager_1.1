import os
import json
import shutil

class MaFileManager:
    def __init__(self):
        self.username = "@Nora_Bobra_CS2"
    
    def show_menu(self):
        print("╔══════════════════════════════════════════════════════╗")
        print("║               МЕНЕДЖЕР .maFile ФАЙЛОВ                ║")
        print("╠══════════════════════════════════════════════════════╣")
        print("║ 1. Переименованный мафайл (fullmafiles)              ║")
        print("║    Переименовывает по account_name                   ║")
        print("║                                                      ║")
        print("║ 2. Урезанный для FSM (shortmaffsmpanel)              ║")
        print("║    Оставляет: shared_secret, account_name, SteamID   ║")
        print("║                                                      ║")
        print("║ 3. Урезанный для DM (shortmafdmpanel)                ║")
        print("║    Оставляет: shared_secret, SteamID (без account)   ║")
        print("║                                                      ║")
        print("║ 0. Выход                                             ║")
        print("╚══════════════════════════════════════════════════════╝")
    
    def get_folder(self):
        folder = input(f"\n{self.username} Введите путь к папке с .maFile файлами: ").strip()
        folder = folder.strip('"\'')
        return folder
    
    def print_header(self, text):
        print("╔══════════════════════════════════════════════════════╗")
        print(f"║{text.center(54)}║")
        print("╠══════════════════════════════════════════════════════╣")
    
    def print_footer(self):
        print("╚══════════════════════════════════════════════════════╝")
    
    # ========== ФУНКЦИЯ 1 ==========
    def fullmafiles(self, input_folder):
        output_folder = os.path.join(input_folder, "fullmafiles")
        os.makedirs(output_folder, exist_ok=True)
        
        self.print_header("РЕЖИМ 1: ПЕРЕИМЕНОВАНИЕ ФАЙЛОВ")
        print(f"║ Папка для результатов:                               ║")
        print(f"║ {output_folder:<53} ║")
        print("╠──────────────────────────────────────────────────────╢")
        
        count = 0
        for filename in os.listdir(input_folder):
            if filename.endswith(".maFile"):
                try:
                    with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    account_name = data.get("account_name", "")
                    if account_name:
                        new_name = f"{account_name}.maFile"
                        shutil.copy2(
                            os.path.join(input_folder, filename),
                            os.path.join(output_folder, new_name)
                        )
                        print(f"║ ✓ {filename:40} → {new_name:<14} ║")
                        count += 1
                    else:
                        print(f"║ ✗ {filename:40} (нет account_name)        ║")
                except:
                    print(f"║ ✗ {filename:40} (ошибка чтения)           ║")
        
        print("╠──────────────────────────────────────────────────────╢")
        print(f"║ Обработано файлов: {count:<34} ║")
        print("╚══════════════════════════════════════════════════════╝")
        return output_folder
    
    # ========== ФУНКЦИЯ 2 ==========
    def shortmaffsmpanel(self, input_folder):
        output_folder = os.path.join(input_folder, "shortmaffsmpanel")
        os.makedirs(output_folder, exist_ok=True)
        
        self.print_header("РЕЖИМ 2: УРЕЗАНИЕ ДЛЯ FSM")
        print(f"║ Папка для результатов:                               ║")
        print(f"║ {output_folder:<53} ║")
        print("╠──────────────────────────────────────────────────────╢")
        
        count = 0
        for filename in os.listdir(input_folder):
            if filename.endswith(".maFile"):
                try:
                    with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    trimmed = {
                        "shared_secret": data.get("shared_secret", ""),
                        "account_name": data.get("account_name", ""),
                        "Session": {"SteamID": data.get("Session", {}).get("SteamID", "")}
                    }
                    
                    account = trimmed["account_name"]
                    if account and trimmed["shared_secret"] and trimmed["Session"]["SteamID"]:
                        with open(os.path.join(output_folder, f"{account}.maFile"), "w") as f:
                            json.dump(trimmed, f, indent=2)
                        print(f"║ ✓ {filename:40} → {account:<14}.maFile ║")
                        count += 1
                    else:
                        print(f"║ ✗ {filename:40} (не все данные)          ║")
                except:
                    print(f"║ ✗ {filename:40} (ошибка обработки)        ║")
        
        print("╠──────────────────────────────────────────────────────╢")
        print(f"║ Обработано файлов: {count:<34} ║")
        print("╚══════════════════════════════════════════════════════╝")
        return output_folder
    
    # ========== ФУНКЦИЯ 3 ==========
    def shortmafdmpanel(self, input_folder):
        output_folder = os.path.join(input_folder, "shortmafdmpanel")
        os.makedirs(output_folder, exist_ok=True)
        
        self.print_header("РЕЖИМ 3: УРЕЗАНИЕ ДЛЯ DM")
        print(f"║ Папка для результатов:                               ║")
        print(f"║ {output_folder:<53} ║")
        print("╠──────────────────────────────────────────────────────╢")
        
        count = 0
        for filename in os.listdir(input_folder):
            if filename.endswith(".maFile"):
                try:
                    with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    secret = data.get("shared_secret", "")
                    steamid = data.get("Session", {}).get("SteamID", "")
                    account = data.get("account_name", "")
                    
                    if secret and steamid and account:
                        trimmed = {
                            "shared_secret": secret,
                            "Session": {"SteamID": steamid}
                        }
                        
                        with open(os.path.join(output_folder, f"{account}.maFile"), "w") as f:
                            json.dump(trimmed, f, indent=4)
                        print(f"║ ✓ {filename:40} → {account:<14}.maFile ║")
                        count += 1
                    else:
                        print(f"║ ✗ {filename:40} (не все данные)          ║")
                except:
                    print(f"║ ✗ {filename:40} (ошибка обработки)        ║")
        
        print("╠──────────────────────────────────────────────────────╢")
        print(f"║ Обработано файлов: {count:<34} ║")
        print("╚══════════════════════════════════════════════════════╝")
        return output_folder
    
    def run(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("\n" + "=" * 56)
            print(f"{self.username} - МЕНЕДЖЕР .maFile ФАЙЛОВ".center(56))
            print("=" * 56)
            
            self.show_menu()
            
            choice = input(f"\n{self.username} Ваш выбор (0-3): ").strip()
            
            if choice == "0":
                print("\n" + "=" * 56)
                print(f"{self.username} Выход из программы...".center(56))
                print("=" * 56)
                break
            
            elif choice in ["1", "2", "3"]:
                folder = self.get_folder()
                
                if not os.path.exists(folder):
                    print("\n" + "=" * 56)
                    print(" ОШИБКА: Папка не существует! ".center(56))
                    print("=" * 56)
                    input("\nНажмите Enter чтобы продолжить...")
                    continue
                
                if choice == "1":
                    result_folder = self.fullmafiles(folder)
                elif choice == "2":
                    result_folder = self.shortmaffsmpanel(folder)
                elif choice == "3":
                    result_folder = self.shortmafdmpanel(folder)
                
                print("\n" + "=" * 56)
                print(" РЕЗУЛЬТАТЫ ОБРАБОТКИ ".center(56))
                print("=" * 56)
                print(f"Папка с результатами:")
                print(f"{result_folder}")
                print("-" * 56)
                
                open_it = input(f"{self.username} Открыть папку? (да/нет): ").lower()
                if open_it == "да":
                    try:
                        os.startfile(result_folder)
                    except:
                        print(f"Путь: {result_folder}")
                
                input("\nНажмите Enter чтобы вернуться в меню...")
            
            else:
                print("\n" + "=" * 56)
                print(" ОШИБКА: Неверный выбор! ".center(56))
                print("=" * 56)
                input("\nНажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    manager = MaFileManager()
    manager.run()