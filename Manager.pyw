import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

class CompactMaFileManager:
    def __init__(self):
        self.username = "@Nora_Bobra_CS2"
        self.window = tk.Tk()
        self.window.title("MaFile Manager")
        self.window.geometry("520x580")  # Увеличил немного размер
        self.window.configure(bg='#000000')
        self.window.resizable(False, False)
        
        # Центрирование окна
        self.center_window()
        
        # Черная тема с акцентами
        self.colors = {
            'bg': '#000000',
            'bg_secondary': '#111111',
            'primary': '#00ff00',  # Зеленый
            'secondary': '#666666',
            'accent': '#0088ff',
            'success': '#00ff00',
            'error': '#ff4444',
            'warning': '#ffaa00',
            'text': '#ffffff',
            'text_secondary': '#aaaaaa',
            'button_bg': '#222222',
            'button_hover': '#333333',
            'entry_bg': '#0a0a0a',
            'border': '#333333'
        }
        
        self.create_widgets()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.window.update_idletasks()
        width = 520
        height = 580
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создание компактного интерфейса"""
        
        # ========== ЗАГОЛОВОК ==========
        title_frame = tk.Frame(self.window, bg=self.colors['bg'])
        title_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        title_label = tk.Label(title_frame,
                              text="MAFILE MANAGER",
                              font=('Arial', 14, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['primary'])
        title_label.pack()
        
        user_label = tk.Label(title_frame,
                             text=self.username,
                             font=('Arial', 8),
                             bg=self.colors['bg'],
                             fg=self.colors['text_secondary'])
        user_label.pack(pady=(2, 0))
        
        # Разделитель
        tk.Frame(self.window, height=1, bg=self.colors['border']).pack(fill='x', padx=15, pady=5)
        
        # ========== ВЫБОР ПАПКИ ==========
        folder_frame = tk.Frame(self.window, bg=self.colors['bg'])
        folder_frame.pack(fill='x', padx=15, pady=8)
        
        folder_label = tk.Label(folder_frame,
                               text="Папка с maFiles:",
                               font=('Arial', 9),
                               bg=self.colors['bg'],
                               fg=self.colors['text'],
                               anchor='w')
        folder_label.pack(fill='x', pady=(0, 5))
        
        # Поле ввода и кнопка в одной строке
        input_frame = tk.Frame(folder_frame, bg=self.colors['bg'])
        input_frame.pack(fill='x')
        
        self.folder_var = tk.StringVar()
        folder_entry = tk.Entry(input_frame,
                               textvariable=self.folder_var,
                               font=('Arial', 9),
                               bg=self.colors['entry_bg'],
                               fg=self.colors['text'],
                               insertbackground=self.colors['text'],
                               relief='flat',
                               bd=1,
                               highlightbackground=self.colors['border'],
                               highlightcolor=self.colors['primary'],
                               highlightthickness=1)
        folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        browse_btn = tk.Button(input_frame,
                              text="...",
                              command=self.browse_folder,
                              font=('Arial', 9, 'bold'),
                              bg=self.colors['button_bg'],
                              fg=self.colors['text'],
                              activebackground=self.colors['button_hover'],
                              activeforeground=self.colors['text'],
                              relief='flat',
                              bd=0,
                              padx=12,
                              cursor='hand2')
        browse_btn.pack(side='right')
        
        # Информация о файлах
        self.file_info_label = tk.Label(folder_frame,
                                       text="Выберите папку",
                                       font=('Arial', 8),
                                       bg=self.colors['bg'],
                                       fg=self.colors['text_secondary'],
                                       anchor='w')
        self.file_info_label.pack(fill='x', pady=(5, 0))
        
        # ========== РЕЖИМЫ ОБРАБОТКИ ==========
        mode_frame = tk.Frame(self.window, bg=self.colors['bg'])
        mode_frame.pack(fill='x', padx=15, pady=8)
        
        mode_label = tk.Label(mode_frame,
                             text="Режим обработки:",
                             font=('Arial', 9),
                             bg=self.colors['bg'],
                             fg=self.colors['text'],
                             anchor='w')
        mode_label.pack(fill='x', pady=(0, 8))
        
        # Компактные радиокнопки режимов
        self.mode_var = tk.IntVar(value=0)
        modes = [
            (1, "1. Переименовать", "По account_name"),
            (2, "2. Урезать для FSM", "shared_secret, account_name, SteamID"),
            (3, "3. Урезать для DM", "shared_secret, SteamID (без account)")
        ]
        
        # Используем Frame для компактного расположения
        modes_grid = tk.Frame(mode_frame, bg=self.colors['bg'])
        modes_grid.pack(fill='x')
        
        for i, (value, title, desc) in enumerate(modes):
            # Фрейм для каждого режима
            mode_item = tk.Frame(modes_grid, bg=self.colors['bg'])
            mode_item.pack(fill='x', pady=4)
            
            # Радиокнопка и текст
            rb_frame = tk.Frame(mode_item, bg=self.colors['bg'])
            rb_frame.pack(side='left', anchor='w')
            
            mode_btn = tk.Radiobutton(rb_frame,
                                     text="",
                                     variable=self.mode_var,
                                     value=value,
                                     font=('Arial', 9),
                                     bg=self.colors['bg'],
                                     fg=self.colors['text'],
                                     activebackground=self.colors['bg'],
                                     activeforeground=self.colors['primary'],
                                     selectcolor=self.colors['bg'],
                                     indicatoron=1,
                                     highlightthickness=0,
                                     cursor='hand2',
                                     padx=0)
            mode_btn.pack(side='left')
            
            # Текст режима
            text_frame = tk.Frame(mode_item, bg=self.colors['bg'])
            text_frame.pack(side='left', fill='x', expand=True, padx=(5, 0))
            
            title_label = tk.Label(text_frame,
                                  text=title,
                                  font=('Arial', 9),
                                  bg=self.colors['bg'],
                                  fg=self.colors['text'],
                                  anchor='w')
            title_label.pack(anchor='w')
            
            desc_label = tk.Label(text_frame,
                                 text=desc,
                                 font=('Arial', 8),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text_secondary'],
                                 anchor='w',
                                 wraplength=400)  # Ограничиваем ширину текста
            desc_label.pack(anchor='w', pady=(1, 0))
        
        # ========== ПРОГРЕСС БАР ==========
        progress_frame = tk.Frame(self.window, bg=self.colors['bg'])
        progress_frame.pack(fill='x', padx=15, pady=8)
        
        self.progress_label = tk.Label(progress_frame,
                                      text="Готов к работе",
                                      font=('Arial', 9),
                                      bg=self.colors['bg'],
                                      fg=self.colors['text_secondary'],
                                      anchor='w')
        self.progress_label.pack(fill='x', pady=(0, 5))
        
        # Прогресс бар
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           mode='determinate',
                                           length=490,
                                           style='black.Horizontal.TProgressbar')
        self.progress_bar.pack(fill='x')
        
        # Стиль для прогресс бара
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('black.Horizontal.TProgressbar',
                       background=self.colors['primary'],
                       troughcolor=self.colors['bg_secondary'],
                       bordercolor=self.colors['bg'],
                       lightcolor=self.colors['primary'],
                       darkcolor=self.colors['primary'])
        
        # ========== КНОПКА СТАРТ ==========
        self.process_btn = tk.Button(self.window,
                                    text="НАЧАТЬ ОБРАБОТКУ",
                                    command=self.process_files,
                                    font=('Arial', 10, 'bold'),
                                    bg=self.colors['primary'],
                                    fg='#000000',
                                    activebackground=self.colors['success'],
                                    activeforeground='#000000',
                                    relief='flat',
                                    bd=0,
                                    padx=20,
                                    pady=6,
                                    cursor='hand2')
        self.process_btn.pack(pady=10)
        
        # ========== ЛОГ ==========
        log_frame = tk.Frame(self.window, bg=self.colors['bg'])
        log_frame.pack(fill='both', expand=True, padx=15, pady=(5, 10))
        
        # Заголовок лога с кнопками
        log_header = tk.Frame(log_frame, bg=self.colors['bg'])
        log_header.pack(fill='x', pady=(0, 5))
        
        log_label = tk.Label(log_header,
                            text="Лог выполнения:",
                            font=('Arial', 9),
                            bg=self.colors['bg'],
                            fg=self.colors['text'],
                            anchor='w')
        log_label.pack(side='left')
        
        # Кнопки управления логом
        buttons_frame = tk.Frame(log_header, bg=self.colors['bg'])
        buttons_frame.pack(side='right')
        
        clear_btn = tk.Button(buttons_frame,
                             text="Очистить",
                             command=self.clear_log,
                             font=('Arial', 8),
                             bg=self.colors['button_bg'],
                             fg=self.colors['text_secondary'],
                             activebackground=self.colors['button_hover'],
                             activeforeground=self.colors['text'],
                             relief='flat',
                             bd=0,
                             padx=6,
                             pady=1,
                             cursor='hand2')
        clear_btn.pack(side='left', padx=(0, 5))
        
        copy_btn = tk.Button(buttons_frame,
                            text="Копировать",
                            command=self.copy_log,
                            font=('Arial', 8),
                            bg=self.colors['button_bg'],
                            fg=self.colors['text_secondary'],
                            activebackground=self.colors['button_hover'],
                            activeforeground=self.colors['text'],
                            relief='flat',
                            bd=0,
                            padx=6,
                            pady=1,
                            cursor='hand2')
        copy_btn.pack(side='left')
        
        # Текстовое поле лога с прокруткой
        log_container = tk.Frame(log_frame, bg=self.colors['border'])
        log_container.pack(fill='both', expand=True)
        
        # Полоса прокрутки
        scrollbar = tk.Scrollbar(log_container)
        scrollbar.pack(side='right', fill='y')
        
        self.log_text = tk.Text(log_container,
                               height=6,  # Увеличил высоту
                               font=('Consolas', 8),
                               bg=self.colors['entry_bg'],
                               fg=self.colors['text'],
                               insertbackground=self.colors['text'],
                               wrap=tk.WORD,
                               relief='flat',
                               bd=0,
                               yscrollcommand=scrollbar.set)
        self.log_text.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.log_text.yview)
        
        # ========== СТАТУС БАР ==========
        status_frame = tk.Frame(self.window,
                               bg=self.colors['bg_secondary'],
                               height=22)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_var = tk.StringVar(value="Готов")
        status_label = tk.Label(status_frame,
                               textvariable=self.status_var,
                               font=('Arial', 8),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_secondary'],
                               anchor='w',
                               padx=8)
        status_label.pack(side='left', fill='x')
        
        self.result_btn = tk.Button(status_frame,
                                   text="",
                                   command=self.open_result_folder,
                                   font=('Arial', 8),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['primary'],
                                   activebackground=self.colors['bg_secondary'],
                                   activeforeground=self.colors['accent'],
                                   relief='flat',
                                   bd=0,
                                   padx=8,
                                   cursor='hand2',
                                   state='disabled')
        self.result_btn.pack(side='right')
        
        # Бинд для обновления информации о файлах
        self.folder_var.trace('w', self.on_folder_changed)
    
    def on_folder_changed(self, *args):
        """Обновление информации при изменении папки"""
        folder = self.folder_var.get()
        if folder and os.path.exists(folder):
            try:
                files = [f for f in os.listdir(folder) if f.endswith('.maFile')]
                count = len(files)
                self.file_info_label.config(
                    text=f"Найдено файлов: {count}",
                    fg=self.colors['success'] if count > 0 else self.colors['warning']
                )
            except:
                self.file_info_label.config(
                    text="Ошибка доступа",
                    fg=self.colors['error']
                )
        else:
            self.file_info_label.config(
                text="Выберите папку",
                fg=self.colors['text_secondary']
            )
    
    def browse_folder(self):
        """Выбор папки через диалоговое окно"""
        folder = filedialog.askdirectory(
            title="Выберите папку с .maFile файлами",
            initialdir=os.path.expanduser("~")
        )
        
        if folder:
            self.folder_var.set(folder)
    
    def log_message(self, message, type="info"):
        """Добавление сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if type == "success":
            prefix = "[✓]"
            color = self.colors['success']
        elif type == "error":
            prefix = "[✗]"
            color = self.colors['error']
        elif type == "warning":
            prefix = "[!]"
            color = self.colors['warning']
        else:
            prefix = "[i]"
            color = self.colors['text']
        
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, f"{prefix} [{timestamp}] {message}\n", type)
        self.log_text.tag_config(type, foreground=color)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
    
    def copy_log(self):
        """Копирование лога в буфер обмена"""
        log_content = self.log_text.get(1.0, tk.END)
        self.window.clipboard_clear()
        self.window.clipboard_append(log_content)
        self.log_message("Лог скопирован в буфер обмена", "success")
    
    def update_progress(self, value, text):
        """Обновление прогресс бара"""
        self.progress_bar['value'] = value
        self.progress_label.config(text=text)
        self.window.update_idletasks()
    
    def clear_log(self):
        """Очистка лога"""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.log_message("Лог очищен", "info")
    
    def process_files(self):
        """Обработка файлов"""
        folder = self.folder_var.get()
        mode = self.mode_var.get()
        
        # Валидация
        if not folder:
            messagebox.showwarning("Внимание", "Выберите папку с файлами!")
            return
        
        if not os.path.exists(folder):
            messagebox.showerror("Ошибка", "Папка не существует!")
            return
        
        if mode == 0:
            messagebox.showwarning("Внимание", "Выберите режим обработки!")
            return
        
        # Отключаем кнопку во время обработки
        self.process_btn.config(state='disabled', text="ОБРАБОТКА...")
        self.result_btn.config(state='disabled', text="")
        
        try:
            files = [f for f in os.listdir(folder) if f.endswith('.maFile')]
            total = len(files)
            
            if total == 0:
                messagebox.showinfo("Информация", "В выбранной папке нет .maFile файлов!")
                return
            
            self.log_message(f"Начата обработка {total} файлов", "info")
            
            # Определяем режим
            if mode == 1:
                result_folder = self.process_mode1(folder, files)
            elif mode == 2:
                result_folder = self.process_mode2(folder, files)
            elif mode == 3:
                result_folder = self.process_mode3(folder, files)
            
            # Успешное завершение
            self.process_btn.config(state='normal', text="НАЧАТЬ ОБРАБОТКУ")
            self.update_progress(100, "Завершено!")
            
            # Активируем кнопку открытия папки
            self.result_btn.config(
                state='normal',
                text="📂 Открыть папку",
                cursor='hand2'
            )
            self.result_path = result_folder
            
            self.log_message(f"Обработка завершена успешно!", "success")
            self.status_var.set(f"Готов | Файлов: {len(os.listdir(result_folder))}")
            
            # Показать уведомление
            messagebox.showinfo("Успешно", f"Обработано файлов: {total}")
            
        except Exception as e:
            self.process_btn.config(state='normal', text="НАЧАТЬ ОБРАБОТКУ")
            self.update_progress(0, "Ошибка")
            self.log_message(f"Ошибка: {str(e)}", "error")
            self.status_var.set("Ошибка обработки")
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
    
    def process_mode1(self, folder, files):
        """Режим 1: Переименование файлов"""
        output_folder = os.path.join(folder, "fullmafiles")
        os.makedirs(output_folder, exist_ok=True)
        
        processed = 0
        total = len(files)
        
        for i, filename in enumerate(files, 1):
            try:
                filepath = os.path.join(folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                account_name = data.get("account_name", "")
                if account_name:
                    new_name = f"{account_name}.maFile"
                    shutil.copy2(filepath, os.path.join(output_folder, new_name))
                    processed += 1
                else:
                    self.log_message(f"{filename}: нет account_name", "warning")
            
            except Exception as e:
                self.log_message(f"{filename}: {str(e)}", "error")
            
            # Обновление прогресса
            progress = (i / total) * 100
            self.update_progress(progress, f"Файл {i}/{total}")
        
        self.log_message(f"Режим 1: {processed}/{total} файлов", "success")
        return output_folder
    
    def process_mode2(self, folder, files):
        """Режим 2: Урезание для FSM"""
        output_folder = os.path.join(folder, "shortmaffsmpanel")
        os.makedirs(output_folder, exist_ok=True)
        
        processed = 0
        total = len(files)
        
        for i, filename in enumerate(files, 1):
            try:
                filepath = os.path.join(folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                trimmed = {
                    "shared_secret": data.get("shared_secret", ""),
                    "account_name": data.get("account_name", ""),
                    "Session": {"SteamID": data.get("Session", {}).get("SteamID", "")}
                }
                
                account = trimmed["account_name"]
                if account and trimmed["shared_secret"] and trimmed["Session"]["SteamID"]:
                    output_path = os.path.join(output_folder, f"{account}.maFile")
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(trimmed, f, indent=2, ensure_ascii=False)
                    processed += 1
                else:
                    self.log_message(f"{filename}: неполные данные", "warning")
            
            except Exception as e:
                self.log_message(f"{filename}: {str(e)}", "error")
            
            # Обновление прогресса
            progress = (i / total) * 100
            self.update_progress(progress, f"Файл {i}/{total}")
        
        self.log_message(f"Режим 2: {processed}/{total} файлов", "success")
        return output_folder
    
    def process_mode3(self, folder, files):
        """Режим 3: Урезание для DM"""
        output_folder = os.path.join(folder, "shortmafdmpanel")
        os.makedirs(output_folder, exist_ok=True)
        
        processed = 0
        total = len(files)
        
        for i, filename in enumerate(files, 1):
            try:
                filepath = os.path.join(folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                secret = data.get("shared_secret", "")
                steamid = data.get("Session", {}).get("SteamID", "")
                account = data.get("account_name", "")
                
                if secret and steamid and account:
                    trimmed = {
                        "shared_secret": secret,
                        "Session": {"SteamID": steamid}
                    }
                    
                    output_path = os.path.join(output_folder, f"{account}.maFile")
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(trimmed, f, indent=4, ensure_ascii=False)
                    processed += 1
                else:
                    self.log_message(f"{filename}: неполные данные", "warning")
            
            except Exception as e:
                self.log_message(f"{filename}: {str(e)}", "error")
            
            # Обновление прогресса
            progress = (i / total) * 100
            self.update_progress(progress, f"Файл {i}/{total}")
        
        self.log_message(f"Режим 3: {processed}/{total} файлов", "success")
        return output_folder
    
    def open_result_folder(self):
        """Открытие папки с результатами (только Windows)"""
        if hasattr(self, 'result_path') and os.path.exists(self.result_path):
            try:
                os.startfile(self.result_path)
            except:
                messagebox.showinfo("Путь к папке", self.result_path)
        else:
            messagebox.showwarning("Внимание", "Папка с результатами не найдена!")
    
    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

if __name__ == "__main__":
    app = CompactMaFileManager()
    app.run()
