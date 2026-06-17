#!/bin/bash
set -e
cd "$(dirname "$0")"

VENV_DIR="./venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "Instalando dependencias..."
pip install --quiet pygame pyinstaller

echo "Gerando executavel..."
pyinstaller algoquest.spec --noconfirm

echo "Comprimindo para download..."
cd dist && zip -r ../AlgoQuest-macOS.zip AlgoQuest.app && cd ..

echo ""
echo "Build concluido!"
echo "  App bundle: dist/AlgoQuest.app"
echo "  Zip:        AlgoQuest-macOS.zip  ($(du -sh AlgoQuest-macOS.zip | cut -f1))"
