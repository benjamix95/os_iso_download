# ISO Downloader Pro

## Descrizione
ISO Downloader Pro è un'applicazione desktop che permette di scaricare facilmente le immagini ISO dei sistemi operativi più popolari. L'applicazione offre un'interfaccia grafica intuitiva che consente di selezionare e scaricare le ISO di vari sistemi operativi come Ubuntu, Debian, Fedora, Linux Mint, Kali Linux, Windows e macOS.

## Funzionalità
- Interfaccia grafica moderna e intuitiva
- Download di ISO da diverse distribuzioni Linux, Windows e macOS
- Organizzazione delle ISO per sistema operativo in schede separate
- Possibilità di inserire URL personalizzati per scaricare ISO non presenti nell'elenco
- Barra di progresso per monitorare lo stato del download
- Selezione della posizione di salvataggio del file
- Gestione degli errori durante il download

## Requisiti di Sistema
- Python 3.6 o superiore
- Connessione internet stabile
- Spazio su disco sufficiente per le immagini ISO (tipicamente 1-5 GB per ISO)

## Installazione

1. Clona o scarica questo repository

2. Installa le dipendenze necessarie:
   ```
   pip install -r requirements.txt
   ```

## Utilizzo

1. Avvia l'applicazione:
   ```
   python iso_downloader.py
   ```

2. Seleziona il sistema operativo desiderato dalle schede disponibili

3. Clicca sul pulsante corrispondente alla versione che desideri scaricare

4. Scegli dove salvare il file ISO utilizzando il pulsante "Sfoglia..."

5. Clicca su "Scarica ISO" per avviare il download

6. Attendi il completamento del download, monitorando la barra di progresso

## Sistemi Operativi Disponibili
- Ubuntu (diverse versioni LTS e non)
- Debian (Stable e Testing)
- Fedora (Workstation e Server)
- Linux Mint (diverse edizioni)
- Kali Linux (diverse varianti)
- Windows (versioni di valutazione)
- macOS (versioni non ufficiali)

## Personalizzazione
Se l'ISO che desideri non è presente nell'elenco, puoi utilizzare la funzione "URL Personalizzato" per inserire direttamente l'URL di download.

## Note
- Le ISO di Windows sono versioni di valutazione fornite da Microsoft
- Le ISO di macOS sono versioni non ufficiali e potrebbero non essere legalmente utilizzabili in tutti i contesti
- Assicurati di avere una connessione internet stabile durante il download

## Autore
Creato da Benjamin Stoica

## Versione
1.0