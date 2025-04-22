#!/bin/bash

# Script per generare gli eseguibili di ISO Downloader Pro

echo "=== ISO Downloader Pro - Script di Build ==="
echo "Questo script genererà gli eseguibili per macOS e Windows"
echo ""

# Verifica che le dipendenze siano installate
echo "Installazione delle dipendenze..."
pip install -r requirements.txt

# Crea la directory dist se non esiste
mkdir -p dist

# Determina il sistema operativo
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "\nGenerazione dell'applicazione macOS (.app)..."
    python setup.py py2app
    echo "\nApplicazione macOS creata con successo in: dist/ISO Downloader Pro.app"
    
    echo "\nVuoi anche generare l'eseguibile Windows? (s/n)"
    read -r response
    if [[ "$response" =~ ^([sS])$ ]]; then
        echo "\nGenerazione dell'eseguibile Windows (.exe)..."
        echo "Nota: La generazione dell'eseguibile Windows su macOS potrebbe non funzionare correttamente."
        echo "Si consiglia di eseguire questo script su Windows per generare l'eseguibile Windows."
        pyinstaller iso_downloader.spec
        echo "\nEseguibile Windows creato in: dist/ISO Downloader Pro.exe"
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "\nGenerazione dell'eseguibile Windows (.exe)..."
    pyinstaller iso_downloader.spec
    echo "\nEseguibile Windows creato con successo in: dist/ISO Downloader Pro.exe"
    
    echo "\nNota: Per generare l'applicazione macOS (.app), esegui questo script su un sistema macOS."
else
    echo "Sistema operativo non riconosciuto. Esegui questo script su Windows o macOS."
    exit 1
fi

echo "\n=== Processo di build completato ==="
echo "Gli eseguibili si trovano nella cartella 'dist'."