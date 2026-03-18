import sys
import threading
from datetime import datetime
from pathlib import Path
from config import MUSIC_DIR

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import pyqtSignal, Qt
    from PyQt5.QtGui import *
    GUI_TYPE = 'pyqt'
except ImportError:
    try:
        import tkinter as tk
        from tkinter import filedialog, scrolledtext, messagebox
        import tkinter.ttk as ttk
        GUI_TYPE = 'tk'
    except ImportError:
        GUI_TYPE = None

def run_gui(main_func, report_func=None):
    if GUI_TYPE == 'pyqt':
        run_pyqt_gui(main_func, report_func)
    elif GUI_TYPE == 'tk':
        run_tk_gui(main_func)
    else:
        print("No GUI available. Install PyQt5 or Tkinter.")

def run_pyqt_gui(main_func, report_func=None):
    app = QApplication(sys.argv)
    
    # Modern dark theme stylesheet
    app.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        QGroupBox {
            font-size: 14px;
            font-weight: bold;
            border: 2px solid #4a90e2;
            border-radius: 8px;
            margin-top: 1ex;
            background-color: #3a3a3a;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px 0 10px;
            color: #4a90e2;
            font-weight: bold;
        }
        
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #4a90e2, stop:1 #357abd);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: bold;
            min-width: 100px;
        }
        
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #5ba0f2, stop:1 #4285d6);
        }
        
        QPushButton:pressed {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #357abd, stop:1 #2c5aa0);
        }
        
        QPushButton#runButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #28a745, stop:1 #218838);
        }
        
        QPushButton#runButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #34d058, stop:1 #28a745);
        }
        
        QPushButton#exitButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #dc3545, stop:1 #c82333);
        }
        
        QPushButton#pauseButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #ffa500, stop:1 #ff8c00);
        }
        
        QPushButton#pauseButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #ffb347, stop:1 #ffa500);
        }
        
        QPushButton#stopButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #ff4444, stop:1 #cc0000);
        }
        
        QPushButton#stopButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #ff6666, stop:1 #ff4444);
        }
        
        QGroupBox#songCard {
            background-color: #2a2a2a;
            border: 2px solid #4a90e2;
            border-radius: 10px;
            margin-top: 5px;
            padding: 10px;
        }
        
        QGroupBox#songCard::title {
            color: #4a90e2;
            font-weight: bold;
            padding: 0 5px;
        }
        
        QLabel#songTitle {
            font-size: 13px;
            font-weight: bold;
            color: #ffffff;
        }
        
        QLabel#songArtist, QLabel#songTitleLabel, QLabel#songAlbum, QLabel#songDuration {
            font-size: 11px;
            color: #cccccc;
            padding: 2px 0px;
        }
        
        QLabel#songDetails {
            font-size: 10px;
            color: #888;
            background-color: #1a1a1a;
            border-radius: 4px;
            padding: 6px;
            margin-top: 4px;
        }
        
        QLabel#songProgress {
            font-size: 9px;
            color: #666;
            font-style: italic;
        }
        
        QLabel#songStatus {
            font-size: 16px;
            padding: 2px 6px;
            border-radius: 3px;
        }
        
        QLabel#songStatus.processing {
            background-color: #4a90e2;
            color: white;
        }
        
        QLabel#songStatus.completed {
            background-color: #28a745;
            color: white;
        }
        
        QLabel#songStatus.error {
            background-color: #dc3545;
            color: white;
        }
        
        QLineEdit {
            background-color: #404040;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 8px;
            font-size: 12px;
        }
        
        QLineEdit:focus {
            border: 1px solid #4a90e2;
        }
        
        QProgressBar {
            border: 2px solid #555555;
            border-radius: 5px;
            text-align: center;
            background-color: #404040;
        }
        
        QProgressBar::chunk {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                              stop:0 #4a90e2, stop:1 #357abd);
            border-radius: 3px;
        }
        
        QTextEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 6px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 10px;
            padding: 8px;
        }
        
        QLabel {
            color: #ffffff;
        }
        
        QLabel#titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: #4a90e2;
        }
    """)
    
    class MainWindow(QWidget):
        output_signal = pyqtSignal(str)
        song_card_signal = pyqtSignal(dict)
        progress_signal = pyqtSignal(int, str)
        completion_signal = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.setWindowTitle("Orpheus — Music Metadata Updater")
            self.setGeometry(100, 100, 1200, 900)
            self.setWindowIcon(QIcon())

            # Processing control
            self.is_processing = False
            self.is_paused = False
            self.is_stopped = False
            self.pause_event = threading.Event()
            self.pause_event.set()
            self.stop_event = threading.Event()

            # Store last run data for the report dialog
            self._last_results = []
            self._last_music_dir = ""
            self._report_func = report_func
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title = QLabel("🎵 Orpheus — Music Metadata Updater")
            title.setObjectName("titleLabel")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            # Configuration Group
            config_group = QGroupBox("Configuration")
            config_layout = QVBoxLayout()
            
            folder_layout = QHBoxLayout()
            folder_label = QLabel("Music Folder:")
            folder_label.setStyleSheet("font-weight: bold;")
            folder_layout.addWidget(folder_label)
            
            self.folder_entry = QLineEdit("")
            folder_layout.addWidget(self.folder_entry)
            
            select_button = QPushButton("Browse...")
            select_button.clicked.connect(self.select_folder)
            folder_layout.addWidget(select_button)
            
            config_layout.addLayout(folder_layout)
            config_group.setLayout(config_layout)
            layout.addWidget(config_group)
            
            # Progress Group
            progress_group = QGroupBox("Progress")
            progress_layout = QVBoxLayout()
            
            self.progress_bar = QProgressBar()
            self.progress_bar.setMinimumHeight(25)
            progress_layout.addWidget(self.progress_bar)
            
            self.progress_label = QLabel("Ready to start")
            self.progress_label.setStyleSheet("font-style: italic;")
            progress_layout.addWidget(self.progress_label)
            
            progress_group.setLayout(progress_layout)
            layout.addWidget(progress_group)
            
            # Songs Cards Area
            songs_group = QGroupBox("Song Processing Status")
            songs_layout = QVBoxLayout()
            
            # Scroll area for song cards
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setMinimumHeight(300)
            self.scroll_area.setMaximumHeight(400)
            
            self.songs_widget = QWidget()
            self.songs_layout = QVBoxLayout(self.songs_widget)
            self.songs_layout.setSpacing(10)
            
            self.scroll_area.setWidget(self.songs_widget)
            songs_layout.addWidget(self.scroll_area)
            
            songs_group.setLayout(songs_layout)
            layout.addWidget(songs_group)
            
            # Output Group
            output_group = QGroupBox("Output Log")
            output_layout = QVBoxLayout()
            
            self.text_area = QTextEdit()
            self.text_area.setMinimumHeight(150)
            output_layout.addWidget(self.text_area)
            
            output_group.setLayout(output_layout)
            layout.addWidget(output_group)
            
            # Buttons Group
            buttons_group = QGroupBox("")
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(20)
            
            self.run_button = QPushButton("🚀 Start Update")
            self.run_button.setObjectName("runButton")
            self.run_button.clicked.connect(self.run_process)
            buttons_layout.addWidget(self.run_button)
            
            self.pause_button = QPushButton("⏸️ Pause")
            self.pause_button.setObjectName("pauseButton")
            self.pause_button.clicked.connect(self.toggle_pause)
            self.pause_button.setEnabled(False)
            buttons_layout.addWidget(self.pause_button)
            
            self.stop_button = QPushButton("⏹️ Stop")
            self.stop_button.setObjectName("stopButton")
            self.stop_button.clicked.connect(self.stop_process)
            self.stop_button.setEnabled(False)
            buttons_layout.addWidget(self.stop_button)
            
            self.exit_button = QPushButton("❌ Exit")
            self.exit_button.setObjectName("exitButton")
            self.exit_button.clicked.connect(app.quit)
            buttons_layout.addWidget(self.exit_button)
            
            buttons_layout.addStretch()
            buttons_group.setLayout(buttons_layout)
            layout.addWidget(buttons_group)
            
            self.setLayout(layout)
            
            self.output_signal.connect(self.append_output)
            self.song_card_signal.connect(self.update_song_card)
            self.progress_signal.connect(self.update_progress)
            self.completion_signal.connect(self.on_process_complete)
        
        def select_folder(self):
            folder = QFileDialog.getExistingDirectory(self, "Select Music Folder", self.folder_entry.text())
            if folder:
                self.folder_entry.setText(folder)
        
        def append_output(self, text):
            self.text_area.append(text)
            self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())
        
        def update_progress(self, value, text):
            """Update progress bar and label safely"""
            try:
                self.progress_bar.setValue(value)
                self.progress_label.setText(text)
            except Exception as e:
                print(f"Error updating progress: {e}")
        
        def on_process_complete(self):
            """Show completion summary and optional report dialog in the main thread."""
            try:
                if self.is_paused or self.is_stopped:
                    return

                results = self._last_results
                updated   = [r for r in results if r.get('changes')]
                no_change = [r for r in results if not r.get('changes') and not r.get('errors')]
                errors    = [r for r in results if r.get('errors')]

                # Build a summary text for the dialog
                lines = [
                    f"Processing finished!\n",
                    f"  Updated   : {len(updated)} file(s)",
                    f"  Unchanged : {len(no_change)} file(s)",
                    f"  Errors    : {len(errors)} file(s)",
                ]
                if updated:
                    lines.append("\nUpdated files:")
                    for r in updated[:10]:   # show max 10 to keep dialog compact
                        changes_str = ', '.join(r['changes'])
                        lines.append(f"  + {r['file'].name}  [{changes_str}]")
                    if len(updated) > 10:
                        lines.append(f"  ... and {len(updated) - 10} more")
                if errors:
                    lines.append("\nErrors:")
                    for r in errors[:5]:
                        lines.append(f"  ! {r['file'].name}: {r['errors'][0]}")

                summary = "\n".join(lines)

                msg = QMessageBox(self)
                msg.setWindowTitle("Processing Complete")
                msg.setText(summary)
                msg.setInformativeText("Generate an Excel report with these results?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setDefaultButton(QMessageBox.Yes)

                if msg.exec_() == QMessageBox.Yes and self._report_func and results:
                    try:
                        music_dir = Path(self._last_music_dir)
                        report_path = music_dir / f"orpheus_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                        self._report_func(results, report_path)
                        QMessageBox.information(self, "Report Saved",
                                                f"Report saved to:\n{report_path}")
                    except Exception as e:
                        QMessageBox.warning(self, "Report Error",
                                            f"Could not save the report:\n{e}")

            except Exception as e:
                print(f"Error in completion dialog: {e}")
        
        def clear_song_cards(self):
            """Safely clear all song cards"""
            try:
                while self.songs_layout.count() > 0:
                    child = self.songs_layout.takeAt(0)
                    if child and child.widget():
                        widget = child.widget()
                        widget.hide()
                        widget.deleteLater()
            except Exception as e:
                print(f"Error clearing song cards: {e}")
        
        def update_song_card(self, song_data):
            """Update or create a song card with the given data - runs in main thread"""
            try:
                if not song_data:
                    return

                song_name = str(song_data.get('name', 'Unknown'))
                status    = str(song_data.get('status', 'waiting'))
                artist    = str(song_data.get('artist', ''))
                title     = str(song_data.get('title', ''))
                album     = str(song_data.get('album', ''))
                quality   = str(song_data.get('quality', ''))
                file_size = str(song_data.get('file_size', ''))
                changes   = list(song_data.get('changes', []))
                errors    = list(song_data.get('errors', []))

                # Find existing card or create new one
                card = None
                for i in range(self.songs_layout.count()):
                    item = self.songs_layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        if hasattr(widget, 'song_name') and widget.song_name == song_name:
                            card = widget
                            break

                if not card:
                    card = self.create_song_card(song_name)
                    self.songs_layout.addWidget(card)

                self.update_card_content(card, status, artist, title,
                                         album, quality, file_size, changes, errors)

                if status == 'processing':
                    self.scroll_area.ensureWidgetVisible(card)
            except Exception as e:
                print(f"Error updating song card: {e}")
        
        def create_song_card(self, song_name):
            """Create a new song card widget"""
            card = QWidget()
            card.setObjectName("songCard")
            card.song_name = song_name

            card.setStyleSheet("""
                QWidget#songCard {
                    background-color: #2a2a2a;
                    border: 2px solid #4a90e2;
                    border-radius: 10px;
                    margin-top: 5px;
                    padding: 8px;
                }
            """)

            layout = QVBoxLayout()
            layout.setContentsMargins(8, 6, 8, 6)
            layout.setSpacing(3)

            # ── Row 1: filename + status badge ──────────────────────
            row1 = QHBoxLayout()
            name_label = QLabel(f"🎵  {song_name}")
            name_label.setObjectName("songTitle")
            name_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #ffffff;")
            row1.addWidget(name_label, stretch=1)

            status_label = QLabel("⏳  Waiting")
            status_label.setObjectName("songStatus")
            status_label.setStyleSheet(
                "font-size: 11px; padding: 2px 8px; border-radius: 4px;"
                "background-color: #555; color: #ccc; font-weight: bold;")
            row1.addWidget(status_label)
            layout.addLayout(row1)

            # ── Row 2: artist · title ────────────────────────────────
            row2 = QHBoxLayout()
            artist_label = QLabel("👤  --")
            artist_label.setStyleSheet("font-size: 11px; color: #cccccc;")
            row2.addWidget(artist_label)
            row2.addWidget(QLabel("·"))
            title_label = QLabel("🎵  --")
            title_label.setStyleSheet("font-size: 11px; color: #cccccc;")
            row2.addWidget(title_label, stretch=1)
            layout.addLayout(row2)

            # ── Row 3: album · quality · size ───────────────────────
            row3 = QHBoxLayout()
            album_label = QLabel("")
            album_label.setStyleSheet("font-size: 10px; color: #999;")
            row3.addWidget(album_label, stretch=1)
            meta_label = QLabel("")
            meta_label.setStyleSheet("font-size: 10px; color: #777;")
            row3.addWidget(meta_label)
            layout.addLayout(row3)

            # ── Row 4: changes / errors ──────────────────────────────
            changes_label = QLabel("")
            changes_label.setStyleSheet(
                "font-size: 10px; color: #aaa; background-color: #1e1e1e;"
                "border-radius: 4px; padding: 4px 6px;")
            changes_label.setWordWrap(True)
            changes_label.setObjectName("songChanges")
            layout.addWidget(changes_label)

            # Store references
            card.name_label    = name_label
            card.artist_label  = artist_label
            card.title_label   = title_label
            card.album_label   = album_label
            card.meta_label    = meta_label
            card.status_label  = status_label
            card.changes_label = changes_label

            card.setLayout(layout)
            card.setMaximumHeight(170)
            return card

        # Map change keywords to emoji prefixes shown in the card
        _CARD_EMOJIS = {
            'year': '📅', 'date': '📅',
            'genre': '🎸', 'album': '💿',
            'track': '🔢', 'cover': '🖼️', 'lyric': '📝',
        }

        def _change_emoji(self, text):
            low = text.lower()
            for key, emoji in self._CARD_EMOJIS.items():
                if key in low:
                    return emoji
            return '✅'

        def update_card_content(self, card, status, artist, title,
                                album, quality, file_size, changes, errors):
            """Update the content of a song card"""
            try:
                if not card or not card.artist_label:
                    return

                # Artist / title
                card.artist_label.setText(f"👤  {artist}" if artist else "👤  --")
                card.title_label.setText(f"🎵  {title}" if title else "🎵  --")

                # Album + quality/size on the same row
                card.album_label.setText(f"💿  {album}" if album else "")
                meta_parts = []
                if quality:
                    meta_parts.append(f"🏷️ {quality}")
                if file_size:
                    meta_parts.append(f"📁 {file_size}")
                card.meta_label.setText("  ".join(meta_parts))

                # Status badge
                STATUS_MAP = {
                    'processing': ("🔄  Processing", "#4a90e2"),
                    'completed':  ("✅  Completed",  "#28a745"),
                    'error':      ("❌  Error",       "#dc3545"),
                    'waiting':    ("⏳  Waiting",     "#555555"),
                }
                label_text, bg = STATUS_MAP.get(status, ("⏳  Waiting", "#555555"))
                card.status_label.setText(label_text)
                card.status_label.setStyleSheet(
                    f"font-size: 11px; padding: 2px 8px; border-radius: 4px;"
                    f"background-color: {bg}; color: white; font-weight: bold;")

                # Changes / errors section
                if errors:
                    err_text = "  ❗ " + "\n  ❗ ".join(errors)
                    card.changes_label.setText(err_text)
                    card.changes_label.setStyleSheet(
                        "font-size: 10px; color: #ff8080; background-color: #2a1a1a;"
                        "border-radius: 4px; padding: 4px 6px;")
                elif changes:
                    lines = "   ".join(
                        f"{self._change_emoji(c)} {c}" for c in changes
                    )
                    card.changes_label.setText(lines)
                    card.changes_label.setStyleSheet(
                        "font-size: 10px; color: #90ee90; background-color: #1a2a1a;"
                        "border-radius: 4px; padding: 4px 6px;")
                else:
                    card.changes_label.setText(
                        "➖  No changes" if status == 'completed' else "")
                    card.changes_label.setStyleSheet(
                        "font-size: 10px; color: #888; background-color: #1e1e1e;"
                        "border-radius: 4px; padding: 4px 6px;")

            except Exception as e:
                print(f"Error updating card: {e}")
        
        def toggle_pause(self):
            """Toggle pause/resume processing"""
            if self.is_processing:
                if self.is_paused:
                    # Resume
                    self.pause_event.set()
                    self.is_paused = False
                    self.pause_button.setText("⏸️ Pause")
                    self.output_signal.emit("▶️ Resuming processing...\n")
                    self.progress_label.setText("Resuming...")
                else:
                    # Pause
                    self.pause_event.clear()
                    self.is_paused = True
                    self.pause_button.setText("▶️ Resume")
                    self.output_signal.emit("⏸️ Processing paused...\n")
                    self.progress_label.setText("Paused")
        
        def stop_process(self):
            """Stop the processing"""
            if self.is_processing:
                self.is_stopped = True
                self.stop_event.set()    # Signal the worker to stop
                self.pause_event.set()   # Unblock if currently paused
                self.is_paused = False
                self.output_signal.emit("⏹️ Stopping processing...\n")
                self.progress_label.setText("Stopping...")
                self.run_button.setEnabled(True)
                self.pause_button.setEnabled(False)
                self.pause_button.setText("⏸️ Pause")
                self.stop_button.setEnabled(False)
        
        def run_process(self):
            self.text_area.clear()
            self.output_signal.emit("🚀 Starting music metadata update process...\n")
            self.progress_bar.setValue(0)
            self.progress_label.setText("Initializing...")
            
            # Clear existing song cards
            self.clear_song_cards()
            
            # Reset state
            self.is_processing = True
            self.is_paused = False
            self.is_stopped = False
            self.pause_event.set()
            self.stop_event.clear()
            
            self.run_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.pause_button.setText("⏸️ Pause")
            self.stop_button.setEnabled(True)
            
            def worker():
                try:
                    self._last_music_dir = self.folder_entry.text()
                    results = main_func(
                        self._last_music_dir,
                        lambda text: self.output_signal.emit(str(text)),
                        lambda current, total, file: self.progress_signal.emit(
                            int((current / total) * 100) if total > 0 else 0,
                            str(f"Processing: {file}")
                        ),
                        self.pause_event,
                        lambda song_data: self.song_card_signal.emit(dict(song_data)),
                        stop_event=self.stop_event,
                    )
                    self._last_results = results or []
                    if self.is_processing:
                        self.output_signal.emit("\nProcess completed successfully!")
                except Exception as e:
                    print(f"Worker error: {e}")
                    self.output_signal.emit(f"\nError: {e}\n")
                finally:
                    self.is_processing = False
                    self.progress_signal.emit(100, "Completed")
                    self.run_button.setEnabled(True)
                    self.pause_button.setEnabled(False)
                    self.stop_button.setEnabled(False)
                    self.completion_signal.emit()
            
            import threading
            t = threading.Thread(target=worker, daemon=True)
            t.start()
        
        def closeEvent(self, event):
            """Handle window close event with proper cleanup"""
            try:
                # Ensure processing is stopped
                self.is_processing = False
                self.pause_event.set()
                
                # Clear song cards
                self.clear_song_cards()
                
                # Accept the close event
                event.accept()
            except Exception as e:
                print(f"Error during cleanup: {e}")
                event.accept()
    
    # Allow Python's default signal handler to run inside the Qt event loop,
    # so Ctrl+C and normal window-close both exit cleanly without a traceback.
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    try:
        window = MainWindow()
        window.show()
        exit_code = app.exec_()
    except Exception as e:
        print(f"Error running PyQt GUI: {e}")
        exit_code = 1
    finally:
        pass

    sys.exit(exit_code)

def run_tk_gui(main_func):
    # Tkinter version remains unchanged for compatibility
    root = tk.Tk()
    root.title("🎵 Orpheus — Music Metadata Updater")
    root.geometry("900x700")
    root.configure(bg="#f0f0f0")
    
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=5)
    style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
    
    folder_var = tk.StringVar(value="")
    
    def select_folder():
        folder = filedialog.askdirectory(initialdir=folder_var.get())
        if folder:
            folder_var.set(folder)
    
    header = tk.Label(root, text="Orpheus — Music Metadata Updater", font=("Arial", 16, "bold"), bg="#4a90e2", fg="white", pady=10)
    header.pack(fill=tk.X)
    
    frame_folder = ttk.Frame(root, padding=10)
    frame_folder.pack(fill=tk.X, padx=10, pady=5)
    ttk.Label(frame_folder, text="Music folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
    entry = ttk.Entry(frame_folder, textvariable=folder_var, width=50)
    entry.grid(row=0, column=1, padx=5)
    ttk.Button(frame_folder, text="Browse", command=select_folder).grid(row=0, column=2)

    progress_var = tk.DoubleVar()
    progress = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress.pack(fill=tk.X, padx=10, pady=5)
    progress_label = ttk.Label(root, text="Ready")
    progress_label.pack(pady=5)
    
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, font=("Courier", 9))
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def run_process():
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "Starting process...\n")
        progress_var.set(0)
        progress_label.config(text="Starting...")
        
        def worker():
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            try:
                with redirect_stdout(f):
                    main_func(folder_var.get())
            except Exception as e:
                f.write(f"Error: {e}\n")

            output = f.getvalue()
            text_area.insert(tk.END, output)
            text_area.see(tk.END)
            progress_var.set(100)
            progress_label.config(text="Completed")
            messagebox.showinfo("Completed", "Process finished")
        
        import threading
        t = threading.Thread(target=worker, daemon=True)
        t.start()
    
    frame_buttons = ttk.Frame(root, padding=10)
    frame_buttons.pack(fill=tk.X)
    ttk.Button(frame_buttons, text="Run Update", command=run_process).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_buttons, text="Exit", command=root.quit).pack(side=tk.RIGHT, padx=5)
    
    root.mainloop()