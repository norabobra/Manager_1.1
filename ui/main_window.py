from __future__ import annotations

import os
import webbrowser

from PySide6.QtCore import Qt, QThread, Signal, QPoint
from PySide6.QtGui import QFont, QIcon, QCursor
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel,
    QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QFileDialog,
    QRadioButton, QButtonGroup, QMessageBox, QProgressBar, QPlainTextEdit,
    QScrollArea, QToolButton, QSizePolicy, QGraphicsDropShadowEffect
)

from ui.styles import qss
from core.fs import list_mafiles
from core.processor import MaFileProcessor
from core.asf import AsfConverter


class Worker(QThread):
    progress = Signal(int, str)
    log = Signal(str, str)
    done = Signal(object)
    failed = Signal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            res = self.fn(*self.args, **self.kwargs)
            self.done.emit(res)
        except Exception as e:
            self.failed.emit(str(e))


class MainWindow(QMainWindow):
    RESIZE_MARGIN = 14  # px

    def __init__(self, version: str = "1.3.0"):
        super().__init__()
        self.version = version

        # Frameless: removes Windows white title bar; we draw our own black one.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.setWindowTitle(f"MaFile Manager v{version}")
        self.resize(450, 700)
        self.setMinimumSize(360, 560)

        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "app.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet(qss())

        # state for move/resize
        self._drag_pos: QPoint | None = None
        self._resizing = False
        self._resize_dir = ""
        self._press_global: QPoint | None = None
        self._start_geom = None

        # Outer layout (space for shadow / rounded corners)
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Rounded container
        self.container = QWidget()
        self.container.setObjectName("appContainer")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        outer.addWidget(self.container)

        root = QVBoxLayout(self.container)
        root.setContentsMargins(12, 10, 12, 12)
        root.setSpacing(8)

        # Title bar (black)
        self.titlebar = QWidget()
        self.titlebar.setObjectName("titleBar")
        tb = QHBoxLayout(self.titlebar)
        tb.setContentsMargins(8, 6, 8, 6)
        tb.setSpacing(8)

        self.title_text = QLabel(f"MaFile Manager v{version}")
        self.title_text.setObjectName("titleText")
        self.title_text.setFont(QFont("Arial", 10, QFont.Bold))
        tb.addWidget(self.title_text, 1)

        btn_min = QToolButton()
        btn_min.setObjectName("winBtn")
        btn_min.setText("—")
        btn_min.setFocusPolicy(Qt.NoFocus)
        btn_min.clicked.connect(self.showMinimized)

        btn_max = QToolButton()
        btn_max.setObjectName("winBtn")
        btn_max.setText("□")
        btn_max.setFocusPolicy(Qt.NoFocus)
        btn_max.clicked.connect(self._toggle_max_restore)

        btn_close = QToolButton()
        btn_close.setObjectName("winClose")
        btn_close.setText("✕")
        btn_close.setFocusPolicy(Qt.NoFocus)
        btn_close.clicked.connect(self.close)

        tb.addWidget(btn_min)
        tb.addWidget(btn_max)
        tb.addWidget(btn_close)

        root.addWidget(self.titlebar)

        # Header
        title = QLabel("MAFILE MANAGER")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))

        subtitle = QLabel(f"v{version} • @Nora_Bobra_CS2")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#AAAAAA;")

        root.addWidget(title)
        root.addWidget(subtitle)

        # Tabs
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        self.tabs.addTab(self._tab_processing(), "Обработка")
        self.tabs.addTab(self._tab_asf(), "ASF")
        self.tabs.addTab(self._tab_dev(), "Dev")

        # Remove focus on tab bar to avoid dotted focus
        self.tabs.tabBar().setFocusPolicy(Qt.NoFocus)

    # ---------- Window controls ----------
    def _toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # ---------- Resize helpers ----------
    def _hit_test(self, pos) -> str:
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        m = self.RESIZE_MARGIN

        left = x <= m
        right = x >= w - m
        top = y <= m
        bottom = y >= h - m

        if top and left:
            return "TL"
        if top and right:
            return "TR"
        if bottom and left:
            return "BL"
        if bottom and right:
            return "BR"
        if left:
            return "L"
        if right:
            return "R"
        if top:
            return "T"
        if bottom:
            return "B"
        return ""

    def _update_cursor(self, region: str):
        cursors = {
            "L": Qt.SizeHorCursor,
            "R": Qt.SizeHorCursor,
            "T": Qt.SizeVerCursor,
            "B": Qt.SizeVerCursor,
            "TL": Qt.SizeFDiagCursor,
            "BR": Qt.SizeFDiagCursor,
            "TR": Qt.SizeBDiagCursor,
            "BL": Qt.SizeBDiagCursor,
            "": Qt.ArrowCursor,
        }
        self.setCursor(QCursor(cursors.get(region, Qt.ArrowCursor)))

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return super().mousePressEvent(event)

        if self.titlebar.geometry().contains(event.position().toPoint()):
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            return

        region = self._hit_test(event.position().toPoint())
        if region:
            self._resizing = True
            self._resize_dir = region
            self._press_global = event.globalPosition().toPoint()
            self._start_geom = self.geometry()
            event.accept()
            return

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # dragging
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton and not self._resizing:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
            return

        # resizing
        if self._resizing and self._start_geom is not None and self._press_global is not None:
            g = self._start_geom
            delta = event.globalPosition().toPoint() - self._press_global
            dx, dy = delta.x(), delta.y()

            x, y, w, h = g.x(), g.y(), g.width(), g.height()
            minw, minh = self.minimumWidth(), self.minimumHeight()
            d = self._resize_dir

            if "L" in d:
                nx = x + dx
                nw = w - dx
                if nw >= minw:
                    x, w = nx, nw
            if "R" in d:
                nw = w + dx
                if nw >= minw:
                    w = nw
            if "T" in d:
                ny = y + dy
                nh = h - dy
                if nh >= minh:
                    y, h = ny, nh
            if "B" in d:
                nh = h + dy
                if nh >= minh:
                    h = nh

            self.setGeometry(x, y, w, h)
            event.accept()
            return

        # cursor update when hovering edges
        region = self._hit_test(event.position().toPoint())
        if not self.isMaximized():
            self._update_cursor(region)
        else:
            self._update_cursor("")
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        self._resizing = False
        self._resize_dir = ""
        self._press_global = None
        self._start_geom = None
        self._update_cursor("")
        return super().mouseReleaseEvent(event)

    # ---------- Logs ----------
    def _append_log(self, box: QPlainTextEdit, msg: str, level: str = "info"):
        prefix = {"success": "✓", "error": "✗", "warning": "!", "info": "i"}.get(level, "i")
        box.appendPlainText(f"[{prefix}] {msg}")
        box.verticalScrollBar().setValue(box.verticalScrollBar().maximum())

    def _set_no_focus(self, *widgets):
        for w in widgets:
            try:
                w.setFocusPolicy(Qt.NoFocus)
            except Exception:
                pass

    # ---------- Tab 1: processing ----------
    def _tab_processing(self) -> QWidget:
        tab = QWidget()
        wrap = QVBoxLayout(tab)
        wrap.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        wrap.addWidget(scroll, 1)

        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setSpacing(12)

        gb_folder = QGroupBox("Папка с maFiles")
        l1 = QVBoxLayout(gb_folder)

        row = QHBoxLayout()
        self.folder_edit = QLineEdit()
        self.folder_edit.setPlaceholderText("Выберите папку с .mafile/.mafiles/.maFile/.maFiles")
        btn_browse = QPushButton("Выбрать…")
        btn_browse.setObjectName("secondary")
        btn_browse.clicked.connect(self._pick_folder)
        self._set_no_focus(btn_browse)

        row.addWidget(self.folder_edit, 1)
        row.addWidget(btn_browse)
        l1.addLayout(row)

        self.files_hint = QLabel("Выберите папку")
        self.files_hint.setStyleSheet("color:#AAAAAA;")
        l1.addWidget(self.files_hint)
        layout.addWidget(gb_folder)

        gb_mode = QGroupBox("Режим обработки")
        l2 = QVBoxLayout(gb_mode)
        self.mode_group = QButtonGroup(self)

        self.rb1 = QRadioButton("1) Переименовать по account_name (копирует в fullmafiles)")
        self.rb2 = QRadioButton("2) Урезать для FSM (shared_secret, account_name, SteamID)")
        self.rb3 = QRadioButton("3) Урезать для DM (shared_secret, SteamID)")
        self.rb1.setChecked(True)

        for rb, i in [(self.rb1, 1), (self.rb2, 2), (self.rb3, 3)]:
            self.mode_group.addButton(rb, i)
            self._set_no_focus(rb)
            l2.addWidget(rb)

        layout.addWidget(gb_mode)

        self.btn_start = QPushButton("НАЧАТЬ ОБРАБОТКУ")
        self.btn_start.clicked.connect(self._start_processing)
        self._set_no_focus(self.btn_start)
        layout.addWidget(self.btn_start)

        self.progress_label = QLabel("Готов к работе")
        self.progress_label.setStyleSheet("color:#AAAAAA;")
        layout.addWidget(self.progress_label)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        gb_log = QGroupBox("Лог выполнения")
        l3 = QVBoxLayout(gb_log)

        row2 = QHBoxLayout()
        btn_clear = QPushButton("Очистить")
        btn_clear.setObjectName("secondary")
        btn_clear.clicked.connect(lambda: self.log_box.setPlainText(""))
        btn_copy = QPushButton("Копировать")
        btn_copy.setObjectName("secondary")
        btn_copy.clicked.connect(self._copy_processing_log)
        self._set_no_focus(btn_clear, btn_copy)

        row2.addWidget(btn_clear)
        row2.addWidget(btn_copy)
        row2.addStretch(1)
        l3.addLayout(row2)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        l3.addWidget(self.log_box)
        layout.addWidget(gb_log)

        self.folder_edit.textChanged.connect(self._update_files_hint)
        layout.addStretch(1)
        return tab

    def _pick_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с maFiles")
        if folder:
            self.folder_edit.setText(folder)

    def _update_files_hint(self):
        folder = self.folder_edit.text().strip()
        if not folder or not os.path.exists(folder):
            self.files_hint.setText("Выберите папку")
            return
        try:
            files = list_mafiles(folder)
            self.files_hint.setText(f"Найдено файлов: {len(files)}")
        except Exception:
            self.files_hint.setText("Ошибка доступа к папке")

    def _copy_processing_log(self):
        self.clipboard().setText(self.log_box.toPlainText())
        self._append_log(self.log_box, "Лог скопирован в буфер обмена", "success")

    def _start_processing(self):
        folder = self.folder_edit.text().strip()
        if not folder:
            QMessageBox.warning(self, "Внимание", "Выберите папку с файлами!")
            return
        if not os.path.exists(folder):
            QMessageBox.critical(self, "Ошибка", "Папка не существует!")
            return

        files = list_mafiles(folder)
        if not files:
            QMessageBox.information(self, "Информация", "В папке нет maFile файлов.")
            return

        mode = self.mode_group.checkedId()
        if mode not in (1, 2, 3):
            mode = 1

        self.btn_start.setEnabled(False)
        self.progress.setValue(0)
        self.progress_label.setText("Старт…")
        self._append_log(self.log_box, f"Начата обработка: {len(files)} файлов", "info")

        def run_job():
            return self._process_job(mode, folder, files)

        self.w1 = Worker(run_job)
        self.w1.progress.connect(lambda v, t: (self.progress.setValue(v), self.progress_label.setText(t)))
        self.w1.log.connect(lambda m, lvl: self._append_log(self.log_box, m, lvl))
        self.w1.done.connect(lambda _: self._finish_processing(len(files)))
        self.w1.failed.connect(self._fail_processing)
        self.w1.start()

    def _process_job(self, mode: int, folder: str, files: list[str]):
        def log(m: str, lvl: str = "info"):
            self.w1.log.emit(m, lvl)

        def prog(v: int, t: str):
            self.w1.progress.emit(v, t)

        proc = MaFileProcessor(log=log, progress=prog)
        if mode == 1:
            return proc.process_mode1(folder, files)
        if mode == 2:
            return proc.process_mode2(folder, files)
        return proc.process_mode3(folder, files)

    def _finish_processing(self, count: int):
        self.progress.setValue(100)
        self.progress_label.setText("Завершено!")
        self._append_log(self.log_box, "Обработка завершена успешно!", "success")
        self.btn_start.setEnabled(True)
        QMessageBox.information(self, "Успешно", f"Обработано файлов: {count}")

    def _fail_processing(self, err: str):
        self.progress.setValue(0)
        self.progress_label.setText("Ошибка")
        self._append_log(self.log_box, err, "error")
        self.btn_start.setEnabled(True)
        QMessageBox.critical(self, "Ошибка", err)

    # ---------- Tab 2: ASF ----------
    def _tab_asf(self) -> QWidget:
        tab = QWidget()
        wrap = QVBoxLayout(tab)
        wrap.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        wrap.addWidget(scroll, 1)

        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setSpacing(12)

        self.asf_mafiles: list[str] = []
        self.asf_logpass: str | None = None
        self.asf_out: str | None = None

        gb_sel = QGroupBox("Файлы для конвертации")
        l1 = QVBoxLayout(gb_sel)

        row1 = QHBoxLayout()
        btn_ma = QPushButton("Выбрать MaFiles")
        btn_ma.setObjectName("secondary")
        btn_ma.clicked.connect(self._pick_asf_mafiles)
        self.lbl_ma = QLabel("Не выбрано")
        self.lbl_ma.setStyleSheet("color:#AAAAAA;")
        self._set_no_focus(btn_ma)
        row1.addWidget(btn_ma)
        row1.addWidget(self.lbl_ma, 1)
        l1.addLayout(row1)

        row2 = QHBoxLayout()
        btn_lp = QPushButton("Выбрать login:password файл")
        btn_lp.setObjectName("secondary")
        btn_lp.clicked.connect(self._pick_asf_logpass)
        self.lbl_lp = QLabel("Не выбран")
        self.lbl_lp.setStyleSheet("color:#AAAAAA;")
        self._set_no_focus(btn_lp)
        row2.addWidget(btn_lp)
        row2.addWidget(self.lbl_lp, 1)
        l1.addLayout(row2)

        row3 = QHBoxLayout()
        btn_out = QPushButton("Папка для сохранения")
        btn_out.setObjectName("secondary")
        btn_out.clicked.connect(self._pick_asf_out)
        self.lbl_out = QLabel("Текущая папка")
        self.lbl_out.setStyleSheet("color:#AAAAAA;")
        self._set_no_focus(btn_out)
        row3.addWidget(btn_out)
        row3.addWidget(self.lbl_out, 1)
        l1.addLayout(row3)

        layout.addWidget(gb_sel)

        self.btn_asf = QPushButton("НАЧАТЬ КОНВЕРТАЦИЮ ASF")
        self.btn_asf.clicked.connect(self._start_asf)
        self._set_no_focus(self.btn_asf)
        layout.addWidget(self.btn_asf)

        self.asf_progress_label = QLabel("Готов к конвертации")
        self.asf_progress_label.setStyleSheet("color:#AAAAAA;")
        layout.addWidget(self.asf_progress_label)

        self.asf_progress = QProgressBar()
        self.asf_progress.setValue(0)
        layout.addWidget(self.asf_progress)

        gb_log = QGroupBox("Лог конвертации")
        l2 = QVBoxLayout(gb_log)
        self.asf_log = QPlainTextEdit()
        self.asf_log.setReadOnly(True)
        l2.addWidget(self.asf_log)
        layout.addWidget(gb_log)

        layout.addStretch(1)
        return tab

    def _pick_asf_mafiles(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Выберите MaFiles",
            filter="MaFiles (*.mafile *.mafiles *.maFile *.maFiles);;All files (*.*)"
        )
        if files:
            self.asf_mafiles = files
            self.lbl_ma.setText(f"Выбрано: {len(files)}")
            self._append_log(self.asf_log, f"Выбрано {len(files)} maFile файлов", "success")

    def _pick_asf_logpass(self):
        f, _ = QFileDialog.getOpenFileName(self, "Выберите файл с логинами", filter="Text (*.txt);;All files (*.*)")
        if f:
            self.asf_logpass = f
            self.lbl_lp.setText(os.path.basename(f))
            self._append_log(self.asf_log, f"Выбран файл: {os.path.basename(f)}", "success")

    def _pick_asf_out(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            self.asf_out = folder
            self.lbl_out.setText(os.path.basename(folder) or folder)
            self._append_log(self.asf_log, f"Папка сохранения: {folder}", "success")

    def _start_asf(self):
        if not self.asf_mafiles:
            QMessageBox.critical(self, "Ошибка", "Выберите MaFiles!")
            return
        if not self.asf_logpass:
            QMessageBox.critical(self, "Ошибка", "Выберите login:password файл!")
            return

        self.btn_asf.setEnabled(False)
        self.asf_progress.setValue(0)
        self.asf_progress_label.setText("Старт…")

        def run_job():
            return self._asf_job(self.asf_mafiles, self.asf_logpass, self.asf_out)

        self.w2 = Worker(run_job)
        self.w2.progress.connect(lambda v, t: (self.asf_progress.setValue(v), self.asf_progress_label.setText(t)))
        self.w2.log.connect(lambda m, lvl: self._append_log(self.asf_log, m, lvl))
        self.w2.done.connect(self._finish_asf)
        self.w2.failed.connect(self._fail_asf)
        self.w2.start()

    def _asf_job(self, mafiles: list[str], logpass: str, out_dir: str | None):
        def log(m: str, lvl: str = "info"):
            self.w2.log.emit(m, lvl)

        def prog(v: int, t: str):
            self.w2.progress.emit(v, t)

        conv = AsfConverter(log=log, progress=prog)
        return conv.convert(mafiles, logpass, out_dir)

    def _finish_asf(self, res: object):
        self.btn_asf.setEnabled(True)
        self.asf_progress.setValue(100)
        self.asf_progress_label.setText("Готово!")
        try:
            out_dir = res.get("output_folder")
            ok = res.get("success")
            failed = len(res.get("failed", []))
        except Exception:
            out_dir = ""
            ok = "?"
            failed = "?"
        QMessageBox.information(self, "Результат", f"Успешно: {ok}\nОшибок/пропущено: {failed}\nПапка: {out_dir}")

    def _fail_asf(self, err: str):
        self.btn_asf.setEnabled(True)
        self.asf_progress.setValue(0)
        self.asf_progress_label.setText("Ошибка")
        self._append_log(self.asf_log, err, "error")
        QMessageBox.critical(self, "Ошибка", err)

    # ---------- Tab 3: Dev ----------
    def _tab_dev(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(12)

        gb = QGroupBox("Контакты")
        l = QVBoxLayout(gb)

        title = QLabel("DEVELOPER")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color:#FF7A00;")
        l.addWidget(title)

        user = QLabel("@Nora_Bobra_CS2")
        user.setAlignment(Qt.AlignCenter)
        user.setStyleSheet("color:#AAAAAA;")
        l.addWidget(user)

        links = [
            ("Telegram Channel", "https://t.me/Nora_Bobra_CS2"),
            ("Shop Bot", "https://t.me/Nora_BoBra_Shop50_bot"),
            ("Telegram Chat", "https://t.me/Nora_Bobra_CS"),
            ("YouTube Channel", "https://www.youtube.com/@SaKuRa_KoTt"),
            ("Twitch Channel", "https://www.twitch.tv/sakura_kot"),
        ]
        for text, url in links:
            b = QPushButton(text)
            b.setObjectName("linkBtn")
            b.setFocusPolicy(Qt.NoFocus)
            b.clicked.connect(lambda _=False, u=url: webbrowser.open(u))
            l.addWidget(b)

        layout.addWidget(gb)

        info = QGroupBox("Информация")
        li = QVBoxLayout(info)
        inf = QLabel(f"MaFile Manager\nВерсия: {self.version}\nUI: Black/Orange\nQt: PySide6")
        inf.setStyleSheet("color:#AAAAAA;")
        li.addWidget(inf)
        layout.addWidget(info)

        layout.addStretch(1)
        return tab
