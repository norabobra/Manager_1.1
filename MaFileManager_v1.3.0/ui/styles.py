def qss() -> str:
    return (
        "QMainWindow { background-color: #000000; }"
        "QWidget { background-color: #000000; color: #FFFFFF; font-size: 13px; }"

        "#appContainer { background-color: #000000; border-radius: 22px; }"
        "#titleBar { background-color: #000000; border-top-left-radius: 22px; border-top-right-radius: 22px; }"
        "#titleText { color: #FFFFFF; font-size: 12px; }"

        "QPushButton:focus, QToolButton:focus, QRadioButton:focus, QTabBar::tab:focus { outline: none; }"
        "QPushButton, QToolButton, QRadioButton { outline: none; }"

        "QTabWidget::pane { border: 1px solid #1A1A1A; border-radius: 16px; padding: 6px; }"
        "QTabBar::tab { background: #111111; padding: 9px 12px; border-radius: 14px; margin: 4px; }"
        "QTabBar::tab:hover { background: #1A1A1A; }"
        "QTabBar::tab:selected { background: #FF7A00; color: #000000; }"

        "QGroupBox { border: 1px solid #1A1A1A; border-radius: 16px; margin-top: 10px; padding: 10px; }"
        "QGroupBox:title { subcontrol-origin: margin; left: 14px; padding: 0 6px; color: #AAAAAA; }"

        "QLineEdit { background: #0D0D0D; border: 1px solid #1A1A1A; border-radius: 14px; padding: 10px; }"
        "QLineEdit:focus { border: 1px solid #FF7A00; }"

        "QRadioButton { spacing: 10px; }"
        "QRadioButton::indicator { width: 18px; height: 18px; border-radius: 9px; border: 2px solid #333333; background: #0D0D0D; }"
        "QRadioButton::indicator:hover { border: 2px solid #FF9A3D; }"
        "QRadioButton::indicator:checked { border: 2px solid #FF7A00; background: #FF7A00; }"

        "QPushButton { background-color: #FF7A00; color: #000000; border-radius: 16px; padding: 10px 14px; font-weight: 700; }"
        "QPushButton:hover { background-color: #FF9A3D; }"
        "QPushButton:pressed { background-color: #E86900; }"
        "QPushButton:disabled { background-color: #444444; color: #222222; }"

        "QPushButton#secondary { background-color: #111111; color: #FFFFFF; font-weight: 600; border: 1px solid #1A1A1A; }"
        "QPushButton#secondary:hover { background-color: #1A1A1A; }"
        "QPushButton#secondary:pressed { background-color: #0A0A0A; }"

        "QPushButton#linkBtn { background: transparent; color: #FF9A3D; font-weight: 600; padding: 10px; border-radius: 14px; text-align: left; }"
        "QPushButton#linkBtn:hover { background: #0A0A0A; }"
        "QPushButton#linkBtn:pressed { background: #111111; }"

        "QPlainTextEdit { background-color: #0A0A0A; border-radius: 16px; border: 1px solid #1A1A1A; padding: 10px; }"

        "QProgressBar { background-color: #111111; border-radius: 14px; border: 1px solid #1A1A1A; text-align: center; height: 18px; }"
        "QProgressBar::chunk { background-color: #FF7A00; border-radius: 14px; }"

        "QToolButton#winBtn { background: #111111; color: #FFFFFF; border-radius: 10px; border: 1px solid #1A1A1A; font-weight: 700; padding: 4px 10px; }"
        "QToolButton#winBtn:hover { background: #1A1A1A; }"
        "QToolButton#winBtn:pressed { background: #0A0A0A; }"
        "QToolButton#winClose { background: #111111; color: #FFFFFF; border-radius: 10px; border: 1px solid #1A1A1A; font-weight: 700; padding: 4px 10px; }"
        "QToolButton#winClose:hover { background: #FF4D4D; color: #000000; border: 1px solid #FF4D4D; }"
        "QToolButton#winClose:pressed { background: #D63A3A; color: #000000; border: 1px solid #D63A3A; }"
    )
