from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QTabWidget, QMessageBox, QSplitter, QLabel, QHBoxLayout, 
    QFrame, QGraphicsDropShadowEffect, QProgressBar, QApplication
)
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCharFormat, QTextCursor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect
from compiler import lexer, parser, semantic_analyzer, intermediate_gen, optimizer, code_generator


class GlowEffect(QGraphicsDropShadowEffect):
    def __init__(self, color=QColor(97, 175, 239), blur_radius=20):
        super().__init__()
        self.setColor(color)
        self.setBlurRadius(blur_radius)
        self.setOffset(0, 0)


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self._glow_radius = 0
        self.glow_animation = QPropertyAnimation(self, b"glow_radius")
        self.glow_animation.setDuration(300)
        self.glow_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    @pyqtProperty(int)
    def glow_radius(self):
        return self._glow_radius
    
    @glow_radius.setter
    def glow_radius(self, value):
        self._glow_radius = value
        self.update()
        
    def enterEvent(self, event):
        self.glow_animation.setStartValue(0)
        self.glow_animation.setEndValue(25)
        self.glow_animation.start()
        
    def leaveEvent(self, event):
        self.glow_animation.setStartValue(25)
        self.glow_animation.setEndValue(0)
        self.glow_animation.start()


class NeonTextEdit(QTextEdit):
    def __init__(self, is_readonly=False, accent_color="#61AFEF"):
        super().__init__()
        self.accent_color = accent_color
        
        # Enhanced styling with glassmorphism effect
        font = QFont("JetBrains Mono", 11)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        
        if is_readonly:
            self.setReadOnly(True)
            self.setStyleSheet(f"""
                QTextEdit {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(30, 30, 47, 0.95),
                        stop:1 rgba(44, 49, 60, 0.95));
                    color: {accent_color};
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    padding: 15px;
                    selection-background-color: rgba(97, 175, 239, 0.3);
                    backdrop-filter: blur(10px);
                }}
                QScrollBar:vertical {{
                    background: rgba(255, 255, 255, 0.05);
                    width: 12px;
                    border-radius: 6px;
                }}
                QScrollBar::handle:vertical {{
                    background: {accent_color};
                    border-radius: 6px;
                    min-height: 20px;
                }}
                QScrollBar::handle:vertical:hover {{
                    background: rgba(97, 175, 239, 0.8);
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QTextEdit {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(18, 18, 24, 0.98),
                        stop:1 rgba(30, 30, 47, 0.98));
                    color: #E8E8E8;
                    border: 2px solid rgba(97, 175, 239, 0.3);
                    border-radius: 15px;
                    padding: 20px;
                    font-size: 12pt;
                    line-height: 1.6;
                    selection-background-color: rgba(97, 175, 239, 0.4);
                }}
                QTextEdit:focus {{
                    border: 2px solid {accent_color};
                    box-shadow: 0 0 20px rgba(97, 175, 239, 0.5);
                }}
                QScrollBar:vertical {{
                    background: rgba(255, 255, 255, 0.05);
                    width: 14px;
                    border-radius: 7px;
                }}
                QScrollBar::handle:vertical {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {accent_color}, stop:1 rgba(97, 175, 239, 0.7));
                    border-radius: 7px;
                    min-height: 25px;
                }}
            """)
        
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        # Add glow effect
        glow = GlowEffect(QColor(accent_color), 15)
        self.setGraphicsEffect(glow)


class GlassFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(15px);
            }
        """)


class StatusBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(97, 175, 239, 0.2),
                    stop:0.5 rgba(152, 195, 121, 0.2),
                    stop:1 rgba(198, 120, 221, 0.2));
                border: none;
                border-radius: 20px;
                margin: 5px;
            }
        """)
        
        layout = QHBoxLayout()
        self.status_label = QLabel("Compile ⚡")
        self.status_label.setStyleSheet("color: #E8E8E8; font: 11pt 'Segoe UI'; padding: 8px;")
        layout.addWidget(self.status_label)
        
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #61AFEF, stop:1 #98C379);
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.progress)
        self.setLayout(layout)


class CompilerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨Compiler - Advanced Code Processor")
        self.setGeometry(100, 50, 1400, 900)
        
        # Dark gradient background
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0D1117,
                    stop:0.3 #161B22,
                    stop:0.7 #21262D,
                    stop:1 #30363D);
            }
        """)
        
        self.initUI()
        
        # Add entrance animation
        self.fade_in_animation()

    def fade_in_animation(self):
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Futuristic Header
        header_frame = GlassFrame()
        header_layout = QVBoxLayout()
        
        title = QLabel("Compiler")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #61AFEF, stop:0.5 #98C379, stop:1 #C678DD);
            padding: 15px;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Advanced Code Processing System")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: rgba(232, 232, 232, 0.7); padding-bottom: 10px;")
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)

        # Main Content Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(12)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(97, 175, 239, 0.3),
                    stop:1 rgba(152, 195, 121, 0.3));
                border-radius: 6px;
                margin: 3px;
            }
            QSplitter::handle:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #61AFEF, stop:1 #98C379);
            }
        """)

        # Left Panel - Code Editor
        left_panel = GlassFrame()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        editor_header = QLabel("📝 Source Code Editor")
        editor_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        editor_header.setStyleSheet("""
            color: #61AFEF;
            padding: 10px;
            background: rgba(97, 175, 239, 0.1);
            border-radius: 8px;
            border-left: 4px solid #61AFEF;
        """)
        left_layout.addWidget(editor_header)

        self.editor = NeonTextEdit(is_readonly=False)
        self.editor.setPlaceholderText("// Enter your source code here...\n// The compiler will process it through multiple stages\n\nint main() {\n    // Your code here\n}")
        left_layout.addWidget(self.editor)

        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)

        # Right Panel - Output Tabs
        right_panel = GlassFrame()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        output_header = QLabel("🔬 Compilation Pipeline Results")
        output_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        output_header.setStyleSheet("""
            color: #98C379;
            padding: 10px;
            background: rgba(152, 195, 121, 0.1);
            border-radius: 8px;
            border-left: 4px solid #98C379;
        """)
        right_layout.addWidget(output_header)

        self.output_tabs = QTabWidget()
        self.output_tabs.setStyleSheet("""
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(255, 255, 255, 0.02));
                color: #ABB2BF;
                min-width: 140px;
                min-height: 40px;
                margin: 1px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                padding: 8px 16px;
                font: bold 10pt "Segoe UI";
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(97, 175, 239, 0.3),
                    stop:1 rgba(97, 175, 239, 0.1));
                color: #61AFEF;
                border-bottom: none;
            }
            QTabBar::tab:hover:!selected {
                background: rgba(255, 255, 255, 0.08);
                color: #E8E8E8;
            }
            QTabWidget::pane {
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                background: rgba(0, 0, 0, 0.2);
                top: -2px;
            }
        """)

        self.tabs = {}
        tab_configs = [
            ("🔤 Tokens", "#E06C75", "Lexical Analysis Results"),
            ("🌳 AST", "#C678DD", "Abstract Syntax Tree"),
            ("✅ Semantics", "#98C379", "Semantic Analysis"),
            ("⚙️ IR", "#56B6C2", "Intermediate Representation"),
            ("🚀 Optimized", "#D19A66", "Optimized IR Code"),
            ("💻 Target", "#61AFEF", "Generated Machine Code"),
        ]

        for name, color, tooltip in tab_configs:
            tab = NeonTextEdit(is_readonly=True, accent_color=color)
            tab.setToolTip(tooltip)
            tab.setPlaceholderText(f"Compilation output will appear here after processing...")
            self.output_tabs.addTab(tab, name)
            self.tabs[name.split(' ', 1)[1]] = tab

        right_layout.addWidget(self.output_tabs)
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)

        splitter.setSizes([700, 670])
        main_layout.addWidget(splitter)

        # Control Panel
        controls_frame = GlassFrame()
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)

        # Compile Button
        self.compile_btn = AnimatedButton("🛠️COMPILE ")
        self.compile_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.compile_btn.setFixedWidth(220)
        self.compile_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #61AFEF, stop:0.5 #21A1F1, stop:1 #98C379);
                color: white;
                border-radius: 25px;
                padding: 15px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #98C379, stop:0.5 #61AFEF, stop:1 #C678DD);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #21A1F1, stop:1 #56B6C2);
            }
        """)
        self.compile_btn.clicked.connect(self.compile_code)

        # Clear Button
        clear_btn = AnimatedButton("🗑️CLEAR")
        clear_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        clear_btn.setFixedWidth(120)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(224, 108, 117, 0.8),
                    stop:1 rgba(224, 108, 117, 0.6));
                color: white;
                border-radius: 20px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(224, 108, 117, 1.0);
            }
        """)
        clear_btn.clicked.connect(self.clear_all)

        controls_layout.addStretch()
        controls_layout.addWidget(clear_btn)
        controls_layout.addWidget(self.compile_btn)
        controls_layout.addStretch()
        controls_frame.setLayout(controls_layout)
        main_layout.addWidget(controls_frame)

        # Status Bar
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)

        main_widget.setLayout(main_layout)

    def clear_all(self):
        self.editor.clear()
        for tab in self.tabs.values():
            tab.clear()
        self.status_bar.status_label.setText("Ready to compile ⚡")

    def update_status(self, message, show_progress=False):
        self.status_bar.status_label.setText(message)
        self.status_bar.progress.setVisible(show_progress)
        QApplication.processEvents()

    def compile_code(self):
        code = self.editor.toPlainText().strip()
        if not code:
            QMessageBox.warning(
                self, 
                "Input Required", 
                "Please enter source code to compile.",
                QMessageBox.Ok
            )
            return

        # Clear previous outputs
        for tab in self.tabs.values():
            tab.clear()

        try:
            self.update_status("🔍 Starting lexical analysis...", True)
            self.status_bar.progress.setValue(10)
            
            # Step 1: Lexical Analysis
            tokens = lexer.tokenize(code)
            token_display = []
            for i, (typ, val) in enumerate(tokens, 1):
                token_display.append(f"{i:3d}. {typ:15} → '{val}'")
            self.tabs["Tokens"].setText("\n".join(token_display))
            self.status_bar.progress.setValue(25)
            
            self.update_status("🌳 Building syntax tree...")
            # Step 2: Parsing
            ast = parser.Parser(tokens).parse()
            self.tabs["AST"].setText(str(ast))
            self.status_bar.progress.setValue(40)

            self.update_status("✅ Performing semantic analysis...")
            # Step 3: Semantic Analysis
            sem_result = semantic_analyzer.analyze(ast)
            self.tabs["Semantics"].setText(str(sem_result))
            self.status_bar.progress.setValue(55)

            self.update_status("⚙️ Generating intermediate code...")
            # Step 4: Intermediate Representation
            ir = intermediate_gen.generate_ir(ast)
            self.tabs["IR"].setText(str(ir))
            self.status_bar.progress.setValue(70)

            self.update_status("🚀 Optimizing code...")
            # Step 5: Optimizer
            opt_ir = optimizer.optimize(ir)
            self.tabs["Optimized"].setText(str(opt_ir))
            self.status_bar.progress.setValue(85)

            self.update_status("💻 Generating target code...")
            # Step 6: Code Generation
            code_output = code_generator.generate_code(opt_ir)
            self.tabs["Target"].setText(str(code_output))
            self.status_bar.progress.setValue(100)

            self.update_status("✨ Compilation completed successfully!", False)
            
            # Success animation
            QTimer.singleShot(2000, lambda: self.update_status("Ready for next compilation ⚡"))

        except Exception as e:
            self.update_status("❌ Compilation failed!", False)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Compilation Error")
            msg.setText("An error occurred during compilation:")
            msg.setDetailedText(str(e))
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1E1E2F;
                    color: #E8E8E8;
                }
                QMessageBox QPushButton {
                    background-color: #61AFEF;
                    color: white;
                    border-radius: 6px;
                    padding: 8px 16px;
                    min-width: 80px;
                }
            """)
            msg.exec_()