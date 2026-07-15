#!/bin/bash

set -e

APP_NAME="YouDlp"
INSTALL_DIR="$HOME/.local/share/youdlp"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== YouDlp Kurulumu ==="
echo ""

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

success() { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
error()   { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# Paket yöneticisi tespiti
detectPackageManager() {
    if command -v pacman &>/dev/null; then
        PKG_MGR="pacman"
    elif command -v apt &>/dev/null; then
        PKG_MGR="apt"
    elif command -v dnf &>/dev/null; then
        PKG_MGR="dnf"
    elif command -v brew &>/dev/null; then
        PKG_MGR="brew"
    else
        error "Paket yöneticisi bulunamadı!"
    fi
    success "Paket yöneticisi: $PKG_MGR"
}

# Bağımlılıkları yükle
installDependencies() {
    echo ""
    echo "Bağımlılıklar kontrol ediliyor..."

    if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
        warn "Python bulunamadı, yükleniyor..."
        case $PKG_MGR in
            pacman) sudo pacman -S --noconfirm python ;;
            apt)    sudo apt update && sudo apt install -y python3 python3-pip python3-venv ;;
            dnf)    sudo dnf install -y python3 python3-pip ;;
            brew)   brew install python ;;
        esac
    fi
    success "Python bulundu"

    if ! python3 -c "import tkinter" 2>/dev/null && ! python -c "import tkinter" 2>/dev/null; then
        warn "tkinter bulunamadı, yükleniyor..."
        case $PKG_MGR in
            pacman) sudo pacman -S --noconfirm tk ;;
            apt)    sudo apt install -y python3-tk ;;
            dnf)    sudo dnf install -y python3-tkinter ;;
            brew)   brew install python-tk ;;
        esac
    fi
    success "tkinter bulundu"

    if ! command -v ffmpeg &>/dev/null; then
        warn "ffmpeg bulunamadı, yükleniyor..."
        case $PKG_MGR in
            pacman) sudo pacman -S --noconfirm ffmpeg ;;
            apt)    sudo apt install -y ffmpeg ;;
            dnf)    sudo dnf install -y ffmpeg ;;
            brew)   brew install ffmpeg ;;
        esac
    fi
    success "ffmpeg bulundu"
}

# Uygulama dizinini oluştur ve dosyaları kopyala
installApp() {
    echo ""
    echo "Uygulama kuruluyor..."

    mkdir -p "$INSTALL_DIR"
    cp "$SCRIPT_DIR/main.py" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/requirements.txt" "$INSTALL_DIR/"

    # Virtual environment oluştur
    python3 -m venv "$INSTALL_DIR/venv"
    source "$INSTALL_DIR/venv/bin/activate"

    pip install --upgrade pip -q
    pip install -r "$INSTALL_DIR/requirements.txt" -q

    deactivate
    success "Uygulama kuruldu: $INSTALL_DIR"
}

# Başlatma scripti oluştur
createLauncher() {
    mkdir -p "$BIN_DIR"

    cat > "$BIN_DIR/youdlp" << 'LAUNCHER'
#!/bin/bash
source "$HOME/.local/share/youdlp/venv/bin/activate"
python "$HOME/.local/share/youdlp/main.py" "$@"
LAUNCHER

    chmod +x "$BIN_DIR/youdlp"
    success "Başlatıcı oluşturuldu: $BIN_DIR/youdlp"
}

# Desktop dosyası oluştur
createDesktopFile() {
    mkdir -p "$DESKTOP_DIR"

    cat > "$DESKTOP_DIR/youdlp.desktop" << EOF
[Desktop Entry]
Name=YouDlp
Comment=YouTube Video & Ses İndirici
Exec=$BIN_DIR/youdlp
Icon=video-x-generic
Terminal=false
Type=Application
Categories=AudioVideo;Video;Network;
Keywords=youtube;download;video;audio;
StartupNotify=true
EOF

    chmod +x "$DESKTOP_DIR/youdlp.desktop"
    success "Desktop dosyası oluşturuldu: $DESKTOP_DIR/youdlp.desktop"

    # Desktop dosyasını güvenilir işaretle
    if command -v gio &>/dev/null; then
        gio set "$DESKTOP_DIR/youdlp.desktop" metadata::trusted true 2>/dev/null || true
    fi
}

# PATH kontrolü
checkPath() {
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        warn "$BIN_DIR PATH'e eklenmedi"
        warn "Uygulamayı çalıştırmak için: $BIN_DIR/youdlp"
        warn "veya PATH'e eklemek için:"
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    fi
}

# Temizlik
cleanup() {
    echo ""
    echo "=== Kurulum Tamamlandı ==="
    echo ""
    echo "Kullanım:"
    echo "  Terminalden:  youdlp"
    echo "  Veya:         $BIN_DIR/youdlp"
    echo ""
    echo "Kaldırmak için:"
    echo "  rm -rf $INSTALL_DIR $BIN_DIR/youdlp $DESKTOP_DIR/youdlp.desktop"
    echo ""
}

# Ana akış
detectPackageManager
installDependencies
installApp
createLauncher
createDesktopFile
checkPath
cleanup
