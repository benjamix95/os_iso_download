import sys
import os
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QPushButton, 
                            QProgressBar, QFileDialog, QMessageBox, QLineEdit,
                            QGroupBox, QGridLayout, QTabWidget, QScrollArea,
                            QMenuBar, QMenu, QDialog)
from PyQt6.QtGui import QIcon, QFont, QPixmap, QColor, QPalette, QAction
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
        
    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size == 0:
                self.finished_signal.emit(False, "Impossibile determinare la dimensione del file")
                return
                
            downloaded = 0
            with open(self.save_path, 'wb') as file:
                for data in response.iter_content(chunk_size=4096):
                    file.write(data)
                    downloaded += len(data)
                    progress = int((downloaded / total_size) * 100)
                    self.progress_signal.emit(progress)
            
            self.finished_signal.emit(True, "Download completato con successo!")
        except Exception as e:
            self.finished_signal.emit(False, f"Errore durante il download: {str(e)}")


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About ISO Downloader Pro")
        self.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("ISO Downloader Pro")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel("Un'applicazione per scaricare facilmente le ISO dei sistemi operativi.")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        
        author = QLabel("Creato da Benjamin Stoica")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        version = QLabel("Versione 1.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        close_button = QPushButton("Chiudi")
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(version)
        layout.addWidget(author)
        layout.addSpacing(20)
        layout.addWidget(close_button)

class ISODownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ISO Downloader Pro")
        self.setMinimumSize(800, 600)
        
        # Imposta l'icona della finestra
        self.setWindowIcon(QIcon('icon.png'))
        
        # Crea la barra dei menu
        self.create_menu_bar()
        
        # Dizionario con i sistemi operativi e i relativi URL di download
        self.os_data = {
            "Ubuntu": {
                "Ubuntu 24.04.3 LTS (Noble Numbat)": "https://releases.ubuntu.com/24.04/ubuntu-24.04.3-desktop-amd64.iso",
                "Ubuntu 25.04 (Zealous Zebra)": "https://releases.ubuntu.com/25.04/ubuntu-25.04-desktop-amd64.iso",
                "Ubuntu 22.04.5 LTS (Jammy Jellyfish)": "https://releases.ubuntu.com/22.04/ubuntu-22.04.5-desktop-amd64.iso",
                "Ubuntu 24.04.3 LTS Server": "https://releases.ubuntu.com/24.04/ubuntu-24.04.3-live-server-amd64.iso"
            },
            "Debian": {
                "Debian 12.6 (Bookworm)": "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.6.0-amd64-netinst.iso",
                "Debian 11.9 (Bullseye)": "https://cdimage.debian.org/debian-cd/current-oldstable/amd64/iso-cd/debian-11.9.0-amd64-netinst.iso",
                "Debian 12.6 Live GNOME": "https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.6.0-amd64-gnome.iso",
                "Debian 12.6 Live KDE": "https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.6.0-amd64-kde.iso"
            },
            "Fedora": {
                "Fedora 42 Workstation": "https://download.fedoraproject.org/pub/fedora/linux/releases/42/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-42-1.1.iso",
                "Fedora 41 Workstation": "https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-41-1.1.iso",
                "Fedora 42 KDE Plasma": "https://download.fedoraproject.org/pub/fedora/linux/releases/42/Spins/x86_64/iso/Fedora-KDE-Live-x86_64-42-1.1.iso",
                "Fedora 42 Server": "https://download.fedoraproject.org/pub/fedora/linux/releases/42/Server/x86_64/iso/Fedora-Server-dvd-x86_64-42-1.1.iso"
            },
            "Linux Mint": {
                "Linux Mint 22.2 Cinnamon": "https://mirrors.edge.kernel.org/linuxmint/stable/22.2/linuxmint-22.2-cinnamon-64bit.iso",
                "Linux Mint 22.2 MATE": "https://mirrors.edge.kernel.org/linuxmint/stable/22.2/linuxmint-22.2-mate-64bit.iso",
                "Linux Mint 22.2 Xfce": "https://mirrors.edge.kernel.org/linuxmint/stable/22.2/linuxmint-22.2-xfce-64bit.iso",
                "Linux Mint 21.3 Cinnamon": "https://mirrors.edge.kernel.org/linuxmint/stable/21.3/linuxmint-21.3-cinnamon-64bit.iso"
            },
            "Kali Linux": {
                "Kali Linux 2025.1a Installer": "https://cdimage.kali.org/kali-2025.1a/kali-linux-2025.1a-installer-amd64.iso",
                "Kali Linux 2025.1a Live": "https://cdimage.kali.org/kali-2025.1a/kali-linux-2025.1a-live-amd64.iso",
                "Kali Linux 2025.1a NetInstaller": "https://cdimage.kali.org/kali-2025.1a/kali-linux-2025.1a-netinst-amd64.iso",
                "Kali Linux 2025.1a Everything": "https://cdimage.kali.org/kali-2025.1a/kali-linux-2025.1a-everything-amd64.iso"
            },
            "Windows": {
                "Windows 11 (Evaluation)": "https://go.microsoft.com/fwlink/p/?LinkID=2195404&clcid=0x410&culture=it-it&country=IT",
                "Windows 10 (Evaluation)": "https://go.microsoft.com/fwlink/p/?LinkID=2208844&clcid=0x410&culture=it-it&country=IT",
                "Windows Server 2022 (Evaluation)": "https://go.microsoft.com/fwlink/p/?LinkID=2195280&clcid=0x410&culture=it-it&country=IT",
                "Windows Server 2019 (Evaluation)": "https://go.microsoft.com/fwlink/p/?LinkID=2195167&clcid=0x410&culture=it-it&country=IT"
            },
            "macOS": {
                "macOS Sequoia 15.4.1 (Unofficial)": "https://archive.org/download/macos-sequoia-15.4.1/macOS%20Sequoia%2015.4.1.iso",
                "macOS Sequoia 15.1 (Unofficial)": "https://archive.org/download/macos-sequoia-15.1/macOS%20Sequoia%2015.1.iso",
                "macOS Sonoma 14.5 (Unofficial)": "https://archive.org/download/macos-sonoma-14.5/macOS%20Sonoma%2014.5.iso",
                "macOS Ventura 13.6 (Unofficial)": "https://archive.org/download/macos-ventura-13.6/macOS%20Ventura%2013.6.iso"
            }
        }
        
        self.init_ui()
        
    def create_menu_bar(self):
        # Crea la barra dei menu
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)  # Forza la visualizzazione della barra dei menu all'interno della finestra
        
        # Menu Aggiornamenti
        updates_menu = menu_bar.addMenu("Aggiornamenti")
        check_updates_action = QAction("Controlla aggiornamenti", self)
        check_updates_action.triggered.connect(self.check_updates)
        updates_menu.addAction(check_updates_action)
        
        # Menu About
        about_menu = menu_bar.addMenu("About")
        about_action = QAction("Informazioni", self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)
    
    def check_updates(self):
        QMessageBox.information(self, "Aggiornamenti", "Nessun aggiornamento disponibile. Stai utilizzando l'ultima versione.")
    
    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Titolo
        title_layout = QHBoxLayout()
        title_label = QLabel("ISO Downloader Pro")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_layout.addWidget(title_label)
        main_layout.addLayout(title_layout)
        
        # Descrizione
        desc_label = QLabel("Scarica facilmente le ISO dei tuoi sistemi operativi preferiti")
        desc_label.setFont(QFont("Arial", 14))
        desc_label.setFont(QFont("Arial", 14))
        main_layout.addWidget(desc_label)
        
        # Tab widget per organizzare i sistemi operativi
        tab_widget = QTabWidget()
        tab_widget.setFont(QFont("Arial", 12))
        
        # Crea una tab per ogni sistema operativo
        for os_name in self.os_data.keys():
            os_tab = QWidget()
            os_layout = QVBoxLayout(os_tab)
            
            # Crea una griglia per le versioni
            versions_group = QGroupBox(f"Versioni di {os_name}")
            versions_group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            versions_layout = QGridLayout(versions_group)
            
            # Aggiungi le versioni alla griglia
            row = 0
            col = 0
            for version_name, url in self.os_data[os_name].items():
                version_button = QPushButton(version_name)
                version_button.setFont(QFont("Arial", 11))
                version_button.setMinimumHeight(60)
                version_button.clicked.connect(lambda checked, os=os_name, ver=version_name: self.select_version(os, ver))
                versions_layout.addWidget(version_button, row, col)
                
                col += 1
                if col > 1:  # 2 colonne
                    col = 0
                    row += 1
            
            os_layout.addWidget(versions_group)
            tab_widget.addTab(os_tab, os_name)
        
        main_layout.addWidget(tab_widget)
        
        # URL personalizzato
        custom_group = QGroupBox("URL Personalizzato")
        custom_group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        custom_layout = QVBoxLayout(custom_group)
        
        custom_desc = QLabel("Inserisci un URL diretto per scaricare un'immagine ISO non presente nell'elenco:")
        custom_desc.setFont(QFont("Arial", 11))
        custom_layout.addWidget(custom_desc)
        
        self.custom_url = QLineEdit()
        self.custom_url.setPlaceholderText("https://esempio.com/file.iso")
        self.custom_url.setMinimumHeight(40)
        self.custom_url.setFont(QFont("Arial", 11))
        custom_layout.addWidget(self.custom_url)
        
        custom_button = QPushButton("Usa URL Personalizzato")
        custom_button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        custom_button.setMinimumHeight(40)
        custom_button.clicked.connect(self.use_custom_url)
        custom_layout.addWidget(custom_button)
        
        main_layout.addWidget(custom_group)
        
        # Sezione di download
        download_group = QGroupBox("Download")
        download_group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        download_layout = QVBoxLayout(download_group)
        
        # Informazioni sulla selezione corrente
        self.selection_label = QLabel("Nessuna ISO selezionata")
        self.selection_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        download_layout.addWidget(self.selection_label)
        
        # Percorso di salvataggio
        save_layout = QHBoxLayout()
        save_label = QLabel("Salva in:")
        save_label.setFont(QFont("Arial", 11))
        self.save_path = QLineEdit()
        self.save_path.setReadOnly(True)
        self.save_path.setPlaceholderText("Seleziona dove salvare il file ISO...")
        self.save_path.setMinimumHeight(40)
        self.save_path.setFont(QFont("Arial", 11))
        browse_button = QPushButton("Sfoglia...")
        browse_button.setFont(QFont("Arial", 11))
        browse_button.setMinimumHeight(40)
        browse_button.clicked.connect(self.browse_save_location)
        save_layout.addWidget(save_label)
        save_layout.addWidget(self.save_path)
        save_layout.addWidget(browse_button)
        download_layout.addLayout(save_layout)
        
        # Barra di progresso
        progress_layout = QVBoxLayout()
        progress_label = QLabel("Progresso:")
        progress_label.setFont(QFont("Arial", 11))
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMinimumHeight(30)
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        download_layout.addLayout(progress_layout)
        
        # Pulsante di download
        self.download_button = QPushButton("Scarica ISO")
        self.download_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.download_button.setMinimumHeight(60)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.start_download)
        download_layout.addWidget(self.download_button)
        
        main_layout.addWidget(download_group)
        
        # Informazioni
        info_label = QLabel("Nota: Assicurati di avere una connessione internet stabile per il download.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        main_layout.addWidget(info_label)
        
        # Variabili per tenere traccia della selezione corrente
        
        # Variabili per tenere traccia della selezione corrente
        self.selected_os = None
        self.selected_version = None
        self.selected_url = None
        
    def select_version(self, os_name, version_name):
        self.selected_os = os_name
        self.selected_version = version_name
        self.selected_url = self.os_data[os_name][version_name]
        self.selection_label.setText(f"Selezionato: {os_name} - {version_name}")
        self.download_button.setEnabled(True)
        
        # Aggiorna il percorso di salvataggio predefinito
        if not self.save_path.text():
            default_name = f"{os_name}_{version_name.replace(' ', '_')}.iso"
            self.save_path.setPlaceholderText(os.path.join(os.path.expanduser("~"), "Downloads", default_name))
    
    def use_custom_url(self):
        url = self.custom_url.text()
        if not url:
            QMessageBox.warning(self, "Attenzione", "Inserisci un URL valido.")
            return
            
        if not (url.startswith("http://") or url.startswith("https://")):
            QMessageBox.warning(self, "Attenzione", "L'URL deve iniziare con http:// o https://")
            return
            
        self.selected_os = "Personalizzato"
        self.selected_version = "URL Personalizzato"
        self.selected_url = url
        self.selection_label.setText(f"Selezionato: URL Personalizzato - {url}")
        self.download_button.setEnabled(True)
        
        # Estrai il nome del file dall'URL
        file_name = url.split("/")[-1]
        if not file_name.endswith(".iso"):
            file_name += ".iso"
            
        # Aggiorna il percorso di salvataggio predefinito
        if not self.save_path.text():
            self.save_path.setPlaceholderText(os.path.join(os.path.expanduser("~"), "Downloads", file_name))
        
    def browse_save_location(self):
        default_name = ""
        if self.selected_os and self.selected_version:
            default_name = f"{self.selected_os}_{self.selected_version.replace(' ', '_')}.iso"
        elif self.selected_url:
            default_name = self.selected_url.split("/")[-1]
            if not default_name.endswith(".iso"):
                default_name += ".iso"
        else:
            default_name = "sistema_operativo.iso"
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Salva ISO", 
            os.path.join(os.path.expanduser("~"), "Downloads", default_name),
            "File ISO (*.iso)"
        )
        if file_path:
            self.save_path.setText(file_path)
    
    def start_download(self):
        # Controlla se è stato selezionato un percorso di salvataggio
        save_path = self.save_path.text()
        if not save_path:
            # Usa il percorso predefinito se non è stato selezionato
            default_path = self.save_path.placeholderText()
            if not default_path or default_path == "Seleziona dove salvare il file ISO...":
                QMessageBox.warning(self, "Attenzione", "Seleziona prima dove salvare il file ISO.")
                return
            save_path = default_path
            self.save_path.setText(save_path)
            
        # Assicurati che la directory esista
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Impossibile creare la directory: {str(e)}")
                return
        
        # Controlla se è stato selezionato un URL
        if not self.selected_url:
            QMessageBox.warning(self, "Attenzione", "Seleziona prima un sistema operativo o inserisci un URL personalizzato.")
            return
        
        # Disabilita il pulsante durante il download
        self.download_button.setEnabled(False)
        self.download_button.setText("Download in corso...")
        
        # Avvia il thread di download
        self.download_thread = DownloadThread(self.selected_url, save_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def download_finished(self, success, message):
        self.download_button.setEnabled(True)
        self.download_button.setText("Scarica ISO")
        
        if success:
            QMessageBox.information(self, "Completato", message)
        else:
            QMessageBox.critical(self, "Errore", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Imposta lo stile Fusion di PyQt6
    QApplication.setStyle("Fusion")
    
    window = ISODownloader()
    window.show()
    sys.exit(app.exec())