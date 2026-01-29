import sys
import subprocess
import os
import json
import shutil
import importlib.util
from datetime import datetime


# Функция для установки пакетов
def install_package(package):
    """Устанавливает пакет через pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Установлен пакет: {package}")
        return True
    except Exception as e:
        print(f"✗ Ошибка установки {package}: {e}")
        return False


# Проверяем и устанавливаем необходимые пакеты
def check_and_install_packages():
    """Проверяет и устанавливает все необходимые пакеты"""
    required_packages = []

    # Проверяем tkinter (часть стандартной библиотеки Python)
    try:
        import tkinter
    except ImportError:
        print("✗ Tkinter не найден!")
        print("Установите Tkinter вручную:")
        print("Для Windows: установите Python с опцией 'tcl/tk and IDLE'")
        print("Для Linux: sudo apt-get install python3-tk")
        print("Для Mac: brew install python-tk")
        return False

    # Список пакетов для установки
    packages_to_install = []

    # Проверяем webbrowser (часть стандартной библиотеки)
    try:
        import webbrowser
    except ImportError:
        print("✗ Webbrowser не найден (входит в стандартную библиотеку)")
        return False

    # Проверяем все стандартные модули
    standard_modules = ['os', 'json', 'shutil', 'datetime']
    for module in standard_modules:
        spec = importlib.util.find_spec(module)
        if spec is None:
            print(f"✗ Модуль {module} не найден (должен быть в стандартной библиотеке)")
            return False

    print("✓ Все необходимые пакеты установлены!")
    return True


# Запускаем проверку пакетов
if not check_and_install_packages():
    print("\n⚠ Не удалось проверить все зависимости.")
    print("Попробуйте запустить: pip install -r requirements.txt")
    print("Или установите пакеты вручную.")

    # Создаем файл requirements.txt
    requirements = """# Requirements for MaFile Manager
# Standard Python libraries (no need to install):
# - tkinter
# - os
# - json
# - shutil
# - datetime
# - webbrowser

# No external packages required!"""

    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)

    print(f"\nФайл requirements.txt создан в: {os.path.abspath('requirements.txt')}")

    # Спрашиваем пользователя, продолжать ли
    if sys.platform != 'linux':
        input("\nНажмите Enter чтобы продолжить (если уверены, что все установлено)...")

# Теперь импортируем все модули
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser


class CompactMaFileManager:
    def __init__(self):
        self.username = "@Nora_Bobra_CS2"
        self.window = tk.Tk()
        self.window.title("MaFile Manager")
        self.window.geometry("620x720")
        self.window.configure(bg='#000000')
        self.window.resizable(False, False)

        # Устанавливаем иконку приложения
        try:
            self.window.iconbitmap('icon.ico')
        except Exception as e:
            print(f"⚠ Не удалось загрузить иконку: {e}")
            print("Поместите файл icon.ico в ту же папку, что и программу")

        # Центрирование окна
        self.center_window()

        # Черная тема с акцентами
        self.colors = {
            'bg': '#000000',
            'bg_secondary': '#111111',
            'primary': '#00ff00',
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
            'border': '#333333',
            'link': '#00aaff'
        }

        self.create_widgets()
        self.setup_asf_tab()
        self.setup_developer_tab()

        # Добавляем информацию о зависимостях в лог
        self.log_message("MaFile Manager v1.2.2 запущен", "success")
        self.log_message("Все зависимости проверены", "success")

    def center_window(self):
        """Центрирование окна на экране"""
        self.window.update_idletasks()
        width = 520
        height = 620
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Создание компактного интерфейса с вкладками"""

        # ========== ЗАГОЛОВОК ==========
        title_frame = tk.Frame(self.window, bg=self.colors['bg'])
        title_frame.pack(fill='x', padx=15, pady=(15, 5))

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

        # ========== NOTEBOOK (ВКЛАДКИ) ==========
        self.notebook = ttk.Notebook(self.window, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=15, pady=5)

        # Стили для вкладок
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TNotebook',
                        background=self.colors['bg'],
                        borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                        background=self.colors['button_bg'],
                        foreground=self.colors['text'],
                        padding=[10, 5],
                        font=('Arial', 9))
        style.map('Custom.TNotebook.Tab',
                  background=[('selected', self.colors['primary'])],
                  foreground=[('selected', '#000000')])

        # ========== ВКЛАДКА 1: ОБРАБОТКА ==========
        self.main_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.main_frame, text="Обработка")

        self.create_main_tab()

        # ========== ВКЛАДКА 2: КОНВЕРТАЦИЯ ASF ==========
        self.asf_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.asf_frame, text="Конвертация ASF")

        # ========== ВКЛАДКА 3: DEVELOPER ==========
        self.dev_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.dev_frame, text="Developer")

    def setup_developer_tab(self):
        """Создание вкладки Developer"""
        # ========== ЗАГОЛОВОК ==========
        dev_header = tk.Frame(self.dev_frame, bg=self.colors['bg'])
        dev_header.pack(fill='x', padx=15, pady=(15, 10))

        dev_title = tk.Label(dev_header,
                             text="DEVELOPER CONTACTS",
                             font=('Arial', 12, 'bold'),
                             bg=self.colors['bg'],
                             fg=self.colors['primary'])
        dev_title.pack()

        dev_subtitle = tk.Label(dev_header,
                                text="@Nora_Bobra_CS2",
                                font=('Arial', 9),
                                bg=self.colors['bg'],
                                fg=self.colors['text_secondary'])
        dev_subtitle.pack(pady=(2, 0))

        # Разделитель
        tk.Frame(self.dev_frame, height=1, bg=self.colors['border']).pack(fill='x', padx=15, pady=5)

        # ========== КОНТАКТЫ ==========
        contacts_frame = tk.Frame(self.dev_frame, bg=self.colors['bg'])
        contacts_frame.pack(fill='both', expand=True, padx=15, pady=10)

        # Создаем список контактов (без салатовых символов - только текст)
        contacts = [
            ("Tg: @rdn_rrdn", None),
            ("Telegram Channel", "https://t.me/Nora_Bobra_CS2"),
            ("Shop Bot", "https://t.me/Nora_BoBra_Shop50_bot"),
            ("Telegram Chat", "https://t.me/Nora_Bobra_CS"),
            ("YouTube Channel", "https://www.youtube.com/@SaKuRa_KoTt"),
            ("Twitch Channel", "https://www.twitch.tv/sakura_kot")
        ]

        for i, (text, url) in enumerate(contacts):
            contact_item = tk.Frame(contacts_frame, bg=self.colors['bg'])
            contact_item.pack(fill='x', pady=6)

            if url:  # Если это ссылка
                link_btn = tk.Button(contact_item,
                                     text=text,
                                     font=('Arial', 9, 'underline'),
                                     bg=self.colors['bg'],
                                     fg=self.colors['link'],
                                     activebackground=self.colors['bg'],
                                     activeforeground=self.colors['accent'],
                                     bd=0,
                                     cursor='hand2',
                                     relief='flat',
                                     anchor='w',
                                     command=lambda u=url: self.open_url(u))
                link_btn.pack(side='left', fill='x', expand=True)

            else:  # Если это просто текст
                text_label = tk.Label(contact_item,
                                      text=text,
                                      font=('Arial', 9),
                                      bg=self.colors['bg'],
                                      fg=self.colors['text'],
                                      anchor='w')
                text_label.pack(side='left', fill='x', expand=True)

        # ========== ИНФОРМАЦИЯ О ПРОГРАММЕ ==========
        info_frame = tk.Frame(self.dev_frame, bg=self.colors['bg_secondary'])
        info_frame.pack(fill='x', padx=15, pady=(20, 15))

        info_text = tk.Text(info_frame,
                            height=4,
                            font=('Arial', 8),
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_secondary'],
                            wrap=tk.WORD,
                            relief='flat',
                            bd=0,
                            highlightthickness=0)
        info_text.pack(fill='both', expand=True, padx=5, pady=5)

        info_content = """MaFile Manager - инструмент для обработки файлов мафил Steam Guard.
Версия: 1.2.2
Разработчик: @Nora_Bobra_CS2
Лицензия: Freeware"""

        info_text.insert(1.0, info_content)
        info_text.config(state='disabled')

        # ========== ЛОГ DEVELOPER ==========
        dev_log_frame = tk.Frame(self.dev_frame, bg=self.colors['bg'])
        dev_log_frame.pack(fill='both', expand=True, padx=15, pady=(5, 15))

        dev_log_label = tk.Label(dev_log_frame,
                                 text="Developer Log:",
                                 font=('Arial', 9),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text'],
                                 anchor='w')
        dev_log_label.pack(fill='x', pady=(0, 5))

        self.dev_log_text = scrolledtext.ScrolledText(dev_log_frame,
                                                      height=6,
                                                      font=('Consolas', 8),
                                                      bg=self.colors['entry_bg'],
                                                      fg=self.colors['text'],
                                                      insertbackground=self.colors['text'],
                                                      wrap=tk.WORD,
                                                      relief='flat',
                                                      bd=0)
        self.dev_log_text.pack(fill='both', expand=True)

        # Добавляем начальное сообщение
        self.log_dev_message("Developer tab initialized", "info")
        self.log_dev_message("Contacts loaded successfully", "success")

    def open_url(self, url):
        """Открытие ссылки в браузере"""
        try:
            webbrowser.open(url)
            self.log_dev_message(f"Opened: {url}", "success")
        except Exception as e:
            self.log_dev_message(f"Error opening URL: {str(e)}", "error")

    def log_dev_message(self, message, type="info"):
        """Добавление сообщения в лог developer"""
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

        self.dev_log_text.configure(state='normal')
        self.dev_log_text.insert(tk.END, f"{prefix} [{timestamp}] {message}\n")
        self.dev_log_text.tag_add(type, "end-1c linestart", "end-1c lineend")
        self.dev_log_text.tag_config(type, foreground=color)
        self.dev_log_text.see(tk.END)
        self.dev_log_text.configure(state='disabled')

    def create_main_tab(self):
        """Создание содержимого вкладки Обработка"""
        # ========== ВЫБОР ПАПКИ ==========
        folder_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
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
        mode_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
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
                                  wraplength=400)
            desc_label.pack(anchor='w', pady=(1, 0))

        # ========== ПРОГРЕСС БАР ==========
        progress_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
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
        self.process_btn = tk.Button(self.main_frame,
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
        log_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
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
                                height=8,
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

        # Бинд для обновления информации о файлах
        self.folder_var.trace('w', self.on_folder_changed)

    def setup_asf_tab(self):
        """Настройка вкладки Конвертация ASF"""
        # ========== ВЫБОР MAFILES ==========
        mafiles_frame = tk.Frame(self.asf_frame, bg=self.colors['bg'])
        mafiles_frame.pack(fill='x', padx=15, pady=8)

        mafiles_label = tk.Label(mafiles_frame,
                                 text="MaFiles:",
                                 font=('Arial', 9),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text'],
                                 anchor='w')
        mafiles_label.pack(fill='x', pady=(0, 5))

        # Кнопка выбора MaFiles
        btn_frame1 = tk.Frame(mafiles_frame, bg=self.colors['bg'])
        btn_frame1.pack(fill='x')

        self.select_mafiles_btn = tk.Button(btn_frame1,
                                            text="Выбрать MaFiles",
                                            command=self.select_mafiles,
                                            font=('Arial', 9),
                                            bg=self.colors['button_bg'],
                                            fg=self.colors['text'],
                                            activebackground=self.colors['button_hover'],
                                            activeforeground=self.colors['text'],
                                            relief='flat',
                                            bd=0,
                                            padx=15,
                                            pady=8,
                                            cursor='hand2')
        self.select_mafiles_btn.pack(side='left', fill='x', expand=True)

        # Счетчик выбранных файлов
        self.mafiles_count_var = tk.StringVar(value="Не выбрано")
        mafiles_count_label = tk.Label(btn_frame1,
                                       textvariable=self.mafiles_count_var,
                                       font=('Arial', 9),
                                       bg=self.colors['bg'],
                                       fg=self.colors['text_secondary'])
        mafiles_count_label.pack(side='right', padx=(10, 0))

        # ========== ВЫБОР ФАЙЛА С ЛОГИНАМИ/ПАРОЛЯМИ ==========
        logpass_frame = tk.Frame(self.asf_frame, bg=self.colors['bg'])
        logpass_frame.pack(fill='x', padx=15, pady=8)

        logpass_label = tk.Label(logpass_frame,
                                 text="Файл с логинами и паролями (login:password):",
                                 font=('Arial', 9),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text'],
                                 anchor='w')
        logpass_label.pack(fill='x', pady=(0, 5))

        # Кнопка выбора файла с логинами/паролями
        btn_frame2 = tk.Frame(logpass_frame, bg=self.colors['bg'])
        btn_frame2.pack(fill='x')

        self.select_logpass_btn = tk.Button(btn_frame2,
                                            text="Выбрать файл с логинами",
                                            command=self.select_logpass_file,
                                            font=('Arial', 9),
                                            bg=self.colors['button_bg'],
                                            fg=self.colors['text'],
                                            activebackground=self.colors['button_hover'],
                                            activeforeground=self.colors['text'],
                                            relief='flat',
                                            bd=0,
                                            padx=15,
                                            pady=8,
                                            cursor='hand2')
        self.select_logpass_btn.pack(side='left', fill='x', expand=True)

        # Информация о выбранном файле
        self.logpass_file_var = tk.StringVar(value="Не выбран")
        logpass_file_label = tk.Label(btn_frame2,
                                      textvariable=self.logpass_file_var,
                                      font=('Arial', 9),
                                      bg=self.colors['bg'],
                                      fg=self.colors['text_secondary'],
                                      wraplength=200)
        logpass_file_label.pack(side='right', padx=(10, 0))

        # ========== ВЫБОР ПАПКИ ДЛЯ СОХРАНЕНИЯ ==========
        output_frame = tk.Frame(self.asf_frame, bg=self.colors['bg'])
        output_frame.pack(fill='x', padx=15, pady=8)

        output_label = tk.Label(output_frame,
                                text="Папка для сохранения ASF файлов:",
                                font=('Arial', 9),
                                bg=self.colors['bg'],
                                fg=self.colors['text'],
                                anchor='w')
        output_label.pack(fill='x', pady=(0, 5))

        # Кнопка выбора папки для сохранения
        btn_frame3 = tk.Frame(output_frame, bg=self.colors['bg'])
        btn_frame3.pack(fill='x')

        self.select_output_btn = tk.Button(btn_frame3,
                                           text="Выбрать папку для сохранения",
                                           command=self.select_output_folder,
                                           font=('Arial', 9),
                                           bg=self.colors['button_bg'],
                                           fg=self.colors['text'],
                                           activebackground=self.colors['button_hover'],
                                           activeforeground=self.colors['text'],
                                           relief='flat',
                                           bd=0,
                                           padx=15,
                                           pady=8,
                                           cursor='hand2')
        self.select_output_btn.pack(side='left', fill='x', expand=True)

        # Информация о выбранной папке
        self.output_folder_var = tk.StringVar(value="Текущая папка")
        output_folder_label = tk.Label(btn_frame3,
                                       textvariable=self.output_folder_var,
                                       font=('Arial', 9),
                                       bg=self.colors['bg'],
                                       fg=self.colors['text_secondary'],
                                       wraplength=200)
        output_folder_label.pack(side='right', padx=(10, 0))

        # ========== КНОПКА КОНВЕРТАЦИИ ==========
        self.create_asf_btn = tk.Button(self.asf_frame,
                                        text="НАЧАТЬ КОНВЕРТАЦИЮ",
                                        command=self.create_asf_files,
                                        font=('Arial', 10, 'bold'),
                                        bg=self.colors['primary'],
                                        fg='#000000',
                                        activebackground=self.colors['success'],
                                        activeforeground='#000000',
                                        relief='flat',
                                        bd=0,
                                        padx=20,
                                        pady=10,
                                        cursor='hand2')
        self.create_asf_btn.pack(pady=15)

        # ========== ПРОГРЕСС КОНВЕРТАЦИИ ==========
        asf_progress_frame = tk.Frame(self.asf_frame, bg=self.colors['bg'])
        asf_progress_frame.pack(fill='x', padx=15, pady=8)

        self.asf_progress_label = tk.Label(asf_progress_frame,
                                           text="Готов к конвертации",
                                           font=('Arial', 9),
                                           bg=self.colors['bg'],
                                           fg=self.colors['text_secondary'],
                                           anchor='w')
        self.asf_progress_label.pack(fill='x', pady=(0, 5))

        self.asf_progress_bar = ttk.Progressbar(asf_progress_frame,
                                                mode='determinate',
                                                length=490,
                                                style='green.Horizontal.TProgressbar')

        # Стиль для зеленого прогресс бара ASF
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('green.Horizontal.TProgressbar',
                        background=self.colors['primary'],
                        troughcolor=self.colors['bg_secondary'],
                        bordercolor=self.colors['bg'],
                        lightcolor=self.colors['primary'],
                        darkcolor=self.colors['primary'])
        self.asf_progress_bar.pack(fill='x')

        # ========== ЛОГ КОНВЕРТАЦИИ ==========
        asf_log_frame = tk.Frame(self.asf_frame, bg=self.colors['bg'])
        asf_log_frame.pack(fill='both', expand=True, padx=15, pady=(5, 10))

        asf_log_label = tk.Label(asf_log_frame,
                                 text="Лог конвертации:",
                                 font=('Arial', 9),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text'],
                                 anchor='w')
        asf_log_label.pack(fill='x', pady=(0, 5))

        # Текстовое поле лога ASF
        self.asf_log_text = scrolledtext.ScrolledText(asf_log_frame,
                                                      height=10,
                                                      font=('Consolas', 8),
                                                      bg=self.colors['entry_bg'],
                                                      fg=self.colors['text'],
                                                      insertbackground=self.colors['text'],
                                                      wrap=tk.WORD,
                                                      relief='flat',
                                                      bd=0)
        self.asf_log_text.pack(fill='both', expand=True)

        # Инициализация переменных
        self.mafiles_paths = []
        self.logpass_file_path = None
        self.output_folder = None

    def select_mafiles(self):
        """Выбор MaFiles для конвертации в ASF - поддерживает все расширения"""
        filetypes = [
            ('MaFiles (все форматы)', '*.mafile;*.mafiles;*.maFile;*.maFiles'),
            ('MaFiles (.mafile)', '*.mafile'),
            ('MaFiles (.mafiles)', '*.mafiles'),
            ('MaFiles (.maFile)', '*.maFile'),
            ('MaFiles (.maFiles)', '*.maFiles'),
            ('All files', '*.*')
        ]
        mafiles = filedialog.askopenfilenames(filetypes=filetypes, title='Выберите MaFile файлы')
        if mafiles:
            self.mafiles_paths = list(mafiles)
            count = len(self.mafiles_paths)
            self.mafiles_count_var.set(f"Выбрано: {count}")
            self.log_asf_message(f"Выбрано {count} MaFile файлов", "success")

    def select_logpass_file(self):
        """Выбор файла с логинами и паролями"""
        filetypes = [('Text files', '*.txt'), ('All files', '*.*')]
        logpass_file = filedialog.askopenfilename(filetypes=filetypes, title='Выберите файл с логинами и паролями')
        if logpass_file:
            self.logpass_file_path = logpass_file
            filename = os.path.basename(logpass_file)
            self.logpass_file_var.set(filename)
            self.log_asf_message(f"Выбран файл с логинами: {filename}", "success")

    def select_output_folder(self):
        """Выбор папки для сохранения ASF файлов"""
        folder = filedialog.askdirectory(
            title="Выберите папку для сохранения ASF файлов",
            initialdir=os.path.expanduser("~")
        )

        if folder:
            self.output_folder = folder
            folder_name = os.path.basename(folder) if folder != os.path.expanduser("~") else folder
            self.output_folder_var.set(folder_name)
            self.log_asf_message(f"Папка для сохранения: {folder}", "success")

    def find_best_match(self, steam_id, filename, logpass_dict):
        """Найти лучший вариант сопоставления"""
        filename_without_ext = self.remove_mafile_extension(filename).strip()
        steam_id = str(steam_id).strip()

        search_variants = []
        search_variants.append(steam_id)
        search_variants.append(filename_without_ext)

        if steam_id.startswith('7656119'):
            search_variants.append(steam_id[7:])
            search_variants.append(steam_id[3:])
            search_variants.append(steam_id[-8:])
            search_variants.append(steam_id[-10:])
            search_variants.append(steam_id[-12:])

        for suffix in ['_mafile', '.mafile', '_mafiles', '.mafiles',
                       '_maFile', '.maFile', '_maFiles', '.maFiles',
                       '_steam', '_account', '_acc']:
            if filename_without_ext.lower().endswith(suffix.lower()):
                clean_name = filename_without_ext[:-len(suffix)]
                search_variants.append(clean_name)

        for sep in ['_', '-', '.', ' ', '__', '--', '..']:
            if sep in filename_without_ext:
                parts = filename_without_ext.split(sep)
                search_variants.extend(parts)
                if len(parts) > 1:
                    search_variants.append(parts[-1])
                    search_variants.append(parts[0])

        search_variants = list(set([v for v in search_variants if v]))

        for variant in search_variants:
            if variant in logpass_dict:
                return variant, logpass_dict[variant]

        for login in logpass_dict.keys():
            login_clean = login.strip().lower()
            variant_lower = steam_id.lower()
            filename_lower = filename_without_ext.lower()

            if (login_clean in variant_lower or variant_lower in login_clean or
                    login_clean in filename_lower or filename_lower in login_clean):
                return login, logpass_dict[login]

        return None, None

    def remove_mafile_extension(self, filename):
        """Удаляет все возможные расширения maFiles из имени файла"""
        mafile_extensions = ['.mafile', '.mafiles', '.maFile', '.maFiles']

        filename_lower = filename.lower()

        for ext in mafile_extensions:
            if filename_lower.endswith(ext):
                return filename[:-len(ext)]

        return os.path.splitext(filename)[0]

    def create_asf_files(self):
        """Конвертация в ASF файлы - с сохранением как .maFile"""
        if not self.mafiles_paths:
            messagebox.showerror('Ошибка', 'Пожалуйста, выберите MaFiles!')
            return

        if not self.logpass_file_path:
            messagebox.showerror('Ошибка', 'Пожалуйста, выберите файл с логинами и паролями!')
            return

        if self.output_folder:
            output_folder = self.output_folder
        else:
            try:
                output_folder = 'ASFmaFiles'
                os.makedirs(output_folder, exist_ok=True)
            except PermissionError:
                messagebox.showinfo('Внимание',
                                    'Нет прав на запись в текущую директорию.\nПожалуйста, выберите папку для сохранения.')
                folder = filedialog.askdirectory(
                    title="Выберите папку для сохранения ASF файлов",
                    initialdir=os.path.expanduser("~")
                )
                if folder:
                    output_folder = folder
                    self.output_folder = folder
                    folder_name = os.path.basename(folder) if folder != os.path.expanduser("~") else folder
                    self.output_folder_var.set(folder_name)
                else:
                    self.create_asf_btn.config(state='normal', text="НАЧАТЬ КОНВЕРТАЦИЮ")
                    return

        self.create_asf_btn.config(state='disabled', text="КОНВЕРТАЦИЯ...")

        try:
            try:
                os.makedirs(output_folder, exist_ok=True)
                test_file = os.path.join(output_folder, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
            except PermissionError:
                self.log_asf_message(f"Нет прав на запись в папку: {output_folder}", "error")
                messagebox.showerror('Ошибка',
                                     f'Нет прав на запись в выбранную папку:\n{output_folder}\n\n'
                                     f'Попробуйте:\n'
                                     f'1. Запустить программу от имени администратора\n'
                                     f'2. Выбрать другую папку (например, на рабочем столе или в документах)\n'
                                     f'3. Проверить разрешения на папку')
                self.create_asf_btn.config(state='normal', text="НАЧАТЬ КОНВЕРТАЦИЮ")
                return

            logpass_dict = {}
            try:
                with open(self.logpass_file_path, 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file, 1):
                        line = line.strip()
                        if line:
                            for delimiter in [':', ';', ',', '|', ' ', '\t']:
                                if delimiter in line:
                                    parts = line.split(delimiter, 1)
                                    if len(parts) >= 2:
                                        login = parts[0].strip()
                                        password = parts[1].strip()
                                        if login and password:
                                            logpass_dict[login] = password
                                        break
            except UnicodeDecodeError:
                for encoding in ['cp1251', 'latin-1', 'iso-8859-1', 'utf-16', 'cp866']:
                    try:
                        with open(self.logpass_file_path, 'r', encoding=encoding) as file:
                            for line_num, line in enumerate(file, 1):
                                line = line.strip()
                                if line:
                                    for delimiter in [':', ';', ',', '|', ' ', '\t']:
                                        if delimiter in line:
                                            parts = line.split(delimiter, 1)
                                            if len(parts) >= 2:
                                                login = parts[0].strip()
                                                password = parts[1].strip()
                                                if login and password:
                                                    logpass_dict[login] = password
                                                break
                        break
                    except:
                        continue

            if not logpass_dict:
                messagebox.showerror('Ошибка', 'В файле не найдено корректных записей login:password')
                self.create_asf_btn.config(state='normal', text="НАЧАТЬ КОНВЕРТАЦИЮ")
                return

            self.log_asf_message(f"Загружено {len(logpass_dict)} записей из файла с логинами", "info")

            available_logins = logpass_dict.copy()

            success_count = 0
            failed_files = []

            self.log_asf_message(f"Начата конвертация в ASF файлы", "info")
            self.log_asf_message(f"MaFiles: {len(self.mafiles_paths)}", "info")
            self.log_asf_message(f"Папка сохранения: {output_folder}", "info")
            self.log_asf_message(f"Файлы будут сохранены с расширением .maFile", "info")

            ma_files_data = []
            for idx, mafile_path in enumerate(self.mafiles_paths):
                filename = os.path.basename(mafile_path)
                try:
                    with open(mafile_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    steam_id = data.get('account_name', '')
                    if not steam_id:
                        steam_id = data.get('Session', {}).get('SteamID', '')

                    if not steam_id:
                        steam_id = self.remove_mafile_extension(filename)

                    ma_files_data.append({
                        'path': mafile_path,
                        'filename': filename,
                        'steam_id': steam_id,
                        'data': data
                    })

                except Exception as e:
                    self.log_asf_message(f"[ОШИБКА ЧТЕНИЯ] {filename} - {str(e)}", "error")
                    failed_files.append((filename, f"Ошибка чтения: {str(e)}"))

            for ma_file in ma_files_data[:]:
                steam_id = ma_file['steam_id']
                filename = ma_file['filename']

                login, password = self.find_best_match(steam_id, filename, available_logins)

                if login and password:
                    try:
                        safe_filename = steam_id.replace(':', '_').replace('/', '_').replace('\\', '_')

                        with open(ma_file['path'], 'r', encoding='utf-8') as f:
                            mafile_data = json.load(f)

                        mafile_output_path = os.path.join(output_folder, f'{safe_filename}.maFile')
                        with open(mafile_output_path, 'w', encoding='utf-8') as f:
                            json.dump(mafile_data, f, indent=2, ensure_ascii=False)

                        asf_config = {
                            "Enabled": True,
                            "OnlineStatus": 7,
                            "RemoteCommunication": 0,
                            "SteamLogin": login,
                            "SteamPassword": password
                        }

                        config_output_path = os.path.join(output_folder, f'{safe_filename}.json')
                        with open(config_output_path, 'w', encoding='utf-8') as f:
                            json.dump(asf_config, f, indent=4, ensure_ascii=False)

                        success_count += 1
                        self.log_asf_message(f"[УСПЕХ] {filename} -> Логин: {login}", "success")
                        self.log_asf_message(f"  Steam ID: {steam_id}", "success")
                        self.log_asf_message(f"  Сохранен как: {safe_filename}.maFile", "success")

                        if login in available_logins:
                            del available_logins[login]

                        ma_files_data.remove(ma_file)

                    except Exception as e:
                        self.log_asf_message(f"[ОШИБКА ОБРАБОТКИ] {filename} - {str(e)}", "error")
                        failed_files.append((filename, f"Ошибка обработки: {str(e)}"))

            if ma_files_data and available_logins:
                self.log_asf_message(f"Осталось {len(ma_files_data)} файлов и {len(available_logins)} логинов", "info")
                self.log_asf_message("Назначаем оставшиеся логины по порядку...", "info")

                available_logins_list = list(available_logins.items())

                for i, ma_file in enumerate(ma_files_data):
                    if i < len(available_logins_list):
                        login, password = available_logins_list[i]
                        steam_id = ma_file['steam_id']
                        filename = ma_file['filename']

                        try:
                            safe_filename = steam_id.replace(':', '_').replace('/', '_').replace('\\', '_')

                            with open(ma_file['path'], 'r', encoding='utf-8') as f:
                                mafile_data = json.load(f)

                            mafile_output_path = os.path.join(output_folder, f'{safe_filename}.maFile')
                            with open(mafile_output_path, 'w', encoding='utf-8') as f:
                                json.dump(mafile_data, f, indent=2, ensure_ascii=False)

                            asf_config = {
                                "Enabled": True,
                                "OnlineStatus": 7,
                                "RemoteCommunication": 0,
                                "SteamLogin": login,
                                "SteamPassword": password
                            }

                            config_output_path = os.path.join(output_folder, f'{safe_filename}.json')
                            with open(config_output_path, 'w', encoding='utf-8') as f:
                                json.dump(asf_config, f, indent=4, ensure_ascii=False)

                            success_count += 1
                            self.log_asf_message(f"[УСПЕХ-АВТО] {filename} -> Логин: {login}", "success")
                            self.log_asf_message(f"  Steam ID: {steam_id}", "success")
                            self.log_asf_message(f"  Сохранен как: {safe_filename}.maFile", "success")

                        except Exception as e:
                            self.log_asf_message(f"[ОШИБКА АВТО-ОБРАБОТКИ] {filename} - {str(e)}", "error")
                            failed_files.append((filename, f"Ошибка авто-обработки: {str(e)}"))
                    else:
                        self.log_asf_message(f"[НЕ ХВАТАЕТ ЛОГИНОВ] {ma_file['filename']}", "warning")
                        failed_files.append((ma_file['filename'], "Не хватает логинов"))

            self.asf_progress_bar['value'] = 100
            self.asf_progress_label.config(text="Конвертация завершена!")
            self.create_asf_btn.config(state='normal', text="НАЧАТЬ КОНВЕРТАЦИЮ")

            result_message = (
                f"Конвертировано в ASF конфигов: {success_count}\n"
                f"Ошибок/Пропущено: {len(failed_files)}\n"
                f"Папка с результатами: {output_folder}\n\n"
                f"Все файлы сохранены с расширением .maFile"
            )

            self.log_asf_message(f"Конвертация завершена!", "success")
            self.log_asf_message(f"Успешно: {success_count}/{len(self.mafiles_paths)}", "success")
            self.log_asf_message(f"Все maFile файлы сохранены с расширением .maFile", "success")

            if failed_files:
                self.log_asf_message(f"Неудачные файлы ({len(failed_files)}):", "warning")
                for filename, reason in failed_files[:10]:
                    self.log_asf_message(f"  {filename} - {reason}", "warning")
                if len(failed_files) > 10:
                    self.log_asf_message(f"  ... и еще {len(failed_files) - 10} файлов", "warning")

            messagebox.showinfo('Результат конвертации', result_message)

        except Exception as e:
            self.create_asf_btn.config(state='normal', text="НАЧАТЬ КОНВЕРТАЦИЮ")
            self.asf_progress_bar['value'] = 0
            self.asf_progress_label.config(text="Ошибка конвертации")
            self.log_asf_message(f"Ошибка конвертации: {str(e)}", "error")
            messagebox.showerror('Ошибка конвертации', f"Произошла ошибка:\n{str(e)}")

    def log_asf_message(self, message, type="info"):
        """Добавление сообщения в лог конвертации ASF"""
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

        self.asf_log_text.configure(state='normal')
        self.asf_log_text.insert(tk.END, f"{prefix} [{timestamp}] {message}\n")
        self.asf_log_text.tag_add(type, "end-1c linestart", "end-1c lineend")
        self.asf_log_text.tag_config(type, foreground=color)
        self.asf_log_text.see(tk.END)
        self.asf_log_text.configure(state='disabled')

    def get_mafiles(self, folder):
        """Получение списка всех .mafile файлов со всеми вариантами расширений"""
        if not folder or not os.path.exists(folder):
            return []

        files = []
        for filename in os.listdir(folder):
            if any(filename.lower().endswith(ext) for ext in ['.mafile', '.mafiles', '.maFile', '.maFiles']):
                files.append(filename)

        return files

    def on_folder_changed(self, *args):
        """Обновление информации при изменении папки"""
        folder = self.folder_var.get()
        if folder and os.path.exists(folder):
            try:
                files = self.get_mafiles(folder)
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
            title="Выберите папку с .mafile файлами",
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

        if not folder:
            messagebox.showwarning("Внимание", "Выберите папку с файлами!")
            return

        if not os.path.exists(folder):
            messagebox.showerror("Ошибка", "Папка не существует!")
            return

        if mode == 0:
            messagebox.showwarning("Внимание", "Выберите режим обработки!")
            return

        self.process_btn.config(state='disabled', text="ОБРАБОТКА...")

        try:
            files = self.get_mafiles(folder)
            total = len(files)

            if total == 0:
                messagebox.showinfo("Информация",
                                    "В выбранной папке нет .mafile файлов!\n\n"
                                    "Ищет файлы с расширениями: .mafile .mafiles .maFile .maFiles")
                return

            self.log_message(f"Начата обработка {total} файлов", "info")

            if mode == 1:
                result_folder = self.process_mode1(folder, files)
            elif mode == 2:
                result_folder = self.process_mode2(folder, files)
            elif mode == 3:
                result_folder = self.process_mode3(folder, files)

            self.process_btn.config(state='normal', text="НАЧАТЬ ОБРАБОТКУ")
            self.update_progress(100, "Завершено!")

            self.log_message(f"Обработка завершена успешно!", "success")

            messagebox.showinfo("Успешно", f"Обработано файлов: {total}")

        except Exception as e:
            self.process_btn.config(state='normal', text="НАЧАТЬ ОБРАБОТКУ")
            self.update_progress(0, "Ошибка")
            self.log_message(f"Ошибка: {str(e)}", "error")
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")

    def process_mode1(self, folder, files):
        """Режим 1: Переименование файлов"""
        output_folder = os.path.join(folder, "fullmafiles")
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            self.log_message(f"Ошибка создания папки: {str(e)}", "error")
            raise

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

            progress = (i / total) * 100
            self.update_progress(progress, f"Файл {i}/{total}")

        self.log_message(f"Режим 1: {processed}/{total} файлов", "success")
        return output_folder

    def process_mode2(self, folder, files):
        """Режим 2: Урезание для FSM"""
        output_folder = os.path.join(folder, "shortmaffsmpanel")
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            self.log_message(f"Ошибка создания папки: {str(e)}", "error")
            raise

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

            progress = (i / total) * 100
            self.update_progress(progress, f"Файл {i}/{total}")

        self.log_message(f"Режим 2: {processed}/{total} файлов", "success")
        return output_folder

    def process_mode3(self, folder, files):
        """Режим 3: Урезание для DM"""
        output_folder = os.path.join(folder, "shortmafdmpanel")
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            self.log_message(f"Ошибка создания папки: {str(e)}", "error")
            raise

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

            progress = (i / total) * 100
            self.update_progress(progress, f"Файл {i}/{total}")

        self.log_message(f"Режим 3: {processed}/{total} файлов", "success")
        return output_folder

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()


if __name__ == "__main__":
    print("=" * 50)
    print("MaFile Manager v1.2.2")
    print("=" * 50)
    print("Проверка зависимостей...")

    # Запускаем приложение
    try:
        app = CompactMaFileManager()
        print("✓ Приложение запущено успешно!")
        print("=" * 50)
        app.run()
    except Exception as e:
        print(f"\n✗ Ошибка запуска приложения: {e}")
        print("\nВозможные решения:")
        print("1. Установите Python 3.6 или выше")
        print("2. Убедитесь, что Tkinter установлен:")
        print("   - Windows: Установите Python с опцией 'tcl/tk and IDLE'")
        print("   - Linux: sudo apt-get install python3-tk")
        print("   - Mac: brew install python-tk")
        print("3. Запустите от имени администратора")
        input("\nНажмите Enter для выхода...")
