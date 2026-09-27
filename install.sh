#!/bin/bash
# MiniOS installer untuk Kali Linux
set -e

echo "⚡ MiniOS Installer"
echo "==================="

# Cek python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan. Install dulu:"
    echo "   sudo apt update && sudo apt install python3 python3-tk"
    exit 1
fi

# Cek tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "📦 Install tkinter..."
    sudo apt update
    sudo apt install -y python3-tk
fi

echo "✅ Dependencies OK"

# Bikin command global 'minios'
MINIOS_PATH="$(pwd)/main.py"
LAUNCHER="/usr/local/bin/minios"

sudo bash -c "cat > $LAUNCHER <<EOF
#!/bin/bash
cd $(pwd)
exec python3 main.py \"\\\$@\"
EOF"
sudo chmod +x "$LAUNCHER"

echo "✅ Command 'minios' installed"
echo ""
echo "Jalankan dengan: minios"
