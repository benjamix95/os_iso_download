# Istruzioni per la Creazione degli Eseguibili

Questo documento contiene le istruzioni per creare le versioni eseguibili di ISO Downloader Pro sia per Windows (.exe) che per macOS (.app).

## Prerequisiti

Assicurati di aver installato tutte le dipendenze necessarie:

```
pip install -r requirements.txt
```

## Creazione dell'Eseguibile per Windows (.exe)

Per creare l'eseguibile per Windows, segui questi passaggi:

1. Apri un terminale nella directory del progetto
2. Esegui il seguente comando:

```
pyinstaller iso_downloader.spec
```

3. Al termine del processo, troverai l'eseguibile nella cartella `dist`:
   - `dist/ISO Downloader Pro.exe`

L'eseguibile includerà già l'icona personalizzata definita nel file `.spec`.

## Creazione dell'Applicazione per macOS (.app)

Per creare l'applicazione per macOS, segui questi passaggi:

1. Apri un terminale nella directory del progetto
2. Esegui il seguente comando:

```
python setup.py py2app
```

3. Al termine del processo, troverai l'applicazione nella cartella `dist`:
   - `dist/ISO Downloader Pro.app`

L'applicazione includerà già l'icona personalizzata definita nel file `setup.py`.

## Note Importanti

- Assicurati di eseguire questi comandi sul sistema operativo corrispondente (Windows per .exe, macOS per .app)
- Se stai creando l'eseguibile su macOS per Windows, dovrai utilizzare un ambiente Windows o una macchina virtuale
- L'icona personalizzata (`icon.png`) è già configurata in entrambi i file di build
- Gli eseguibili generati includono tutte le dipendenze necessarie e possono essere distribuiti come file standalone

## Risoluzione dei Problemi

Se riscontri problemi durante la creazione degli eseguibili:

1. Assicurati che tutte le dipendenze siano installate correttamente
2. Verifica che il file `icon.png` sia presente nella directory del progetto
3. Per macOS, potrebbe essere necessario installare le command line tools di Xcode:
   ```
   xcode-select --install
   ```
4. Per Windows, assicurati di avere installato Visual C++ Redistributable