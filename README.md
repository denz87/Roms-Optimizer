# 🎮 ROMS OPTIMIZER v0.8.1

**Advanced ROM Management & Optimization Tool**

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![Version](https://img.shields.io/badge/Version-0.8.1-brightgreen.svg)

Un potente strumento per l'organizzazione e l'ottimizzazione delle collezioni di ROM con supporto completo per i database DAT MAME e algoritmi intelligenti di priorità geografica e qualitativa.
Il programma mantiene una sola versione per ogni singola rom con ordine di importanza regionale impostato.

## ✨ Caratteristiche Principali

### 🎯 Gestione Intelligente dei Duplicati
- **Algoritmo di priorità avanzato** basato su tag geografici e di qualità
- **Supporto completo DAT MAME** per oltre 100.000 giochi arcade
- **Protezione automatica** di BIOS e giochi parent
- **Rilevamento multi-disco** per giochi su più supporti

### 🌍 Supporto Multi-Lingua
Interfaccia completamente tradotta in **20 lingue**:
- 🇮🇹 Italiano | 🇺🇸 English | 🇫🇷 Français | 🇩🇪 Deutsch | 🇪🇸 Español
- 🇧🇷 Português | 🇷🇺 Русский | 🇯🇵 日本語 | 🇨🇳 中文 | 🇰🇷 한국어
- 🇳🇱 Nederlands | 🇸🇪 Svenska | 🇵🇱 Polski | 🇸🇦 العربية | 🇮🇳 हिन्दी
- 🇳🇴 Norsk | 🇩🇰 Dansk | 🇫🇮 Suomi | 🇬🇷 Ελληνικά | 🇹🇷 Türkçe

### 🎮 Piattaforme Supportate
Supporta ROM di **oltre 100 sistemi** gaming, inclusi:

**Console Retro:**
- Nintendo: NES, SNES, N64, GameCube, Wii, Game Boy, GBA, DS, 3DS, Switch
- Sega: Master System, Genesis, Saturn, Dreamcast, Game Gear, 32X
- Sony: PlayStation 1-5, PSP, PS Vita
- Microsoft: Xbox, Xbox 360, Xbox One

**Arcade & Computer:**
- MAME (tutti i sistemi supportati)
- Commodore 64, Amiga, MSX
- ZX Spectrum, Amstrad CPC
- Atari 2600, 5200, 7800, ST, Lynx, Jaguar

E molti altri sistemi retro e moderni!

### 🛡️ Modalità di Sicurezza
- **Modalità Test**: Anteprima delle operazioni senza modificare i file
- **Modalità Copia**: Crea copie invece di spostare i file originali
- **Backup automatico**: I duplicati vengono spostati in una cartella "cleaned"
- **Nessun file viene mai eliminato definitivamente**

## 🚀 Caratteristiche Tecniche

### 🧠 Sistema di Priorità Intelligente
Il programma utilizza un algoritmo sofisticato per determinare la migliore versione di ogni ROM:

**Priorità Geografica (configurabile):**
- **Modalità Europa**: Italia → Europa → USA → UK → Giappone
- **Modalità USA**: USA/UK → Europa → Italia → Giappone  
- **Modalità Giappone**: Giappone → USA → Europa → Italia

**Priorità Qualitativa:**
1. **🌟 Originali** (senza tag `[]`) - Priorità MASSIMA
2. **✅ Verified `[!]`** - Dump verificati e perfetti
3. **🔧 Fixed `[f]`** - Ottimizzati per emulatori
4. **🔄 Alternative `[a]`** - Versioni alternative con bugfix
5. **📝 Translations `[T+]`** - Traduzioni aggiornate
6. **❌ Bad Dumps `[b]`** - Dump corrotti (priorità minima)

### 🎲 Database DAT MAME
- **Supporto nativo** per file DAT compressi (.dat.gz)
- **Protezione automatica** di BIOS e giochi parent
- **Gestione clone relationships** secondo standard MAME
- **Database aggiornabile** con nuove versioni DAT

### 🎨 Interfaccia Futuristica
- **Design dark mode** con palette futuristica
- **Progress bar animata** con percentuali in tempo reale
- **Log dettagliato** con emoji e colori per una migliore leggibilità
- **Finestra non ridimensionabile** per layout ottimale

## 📦 Installazione

### Requisiti di Sistema
- **Python 3.6+**
- **Windows 10/11** (consigliato)
- **Librerie Python**: tkinter, PIL (Pillow), hashlib, configparser

### Installazione Rapida
1. **Scarica** l'ultima release da GitHub
2. **Estrai** il contenuto in una cartella
3. **Installa le dipendenze**:
   ```bash
   pip install pillow
   ```
4. **Esegui** il programma:
   ```bash
   python rom_cleaner.py
   ```

### Installazione Avanzata
Per un'esperienza completa, assicurati di avere:
- File DAT MAME nella cartella `dat/`
- File di traduzione nella cartella `lang/`
- File di istruzioni nella cartella `info/`
- Logo personalizzato: `logo.png` e `FFLogo.png`

## 🎯 Utilizzo

### Workflow Tipico
1. **Avvia** il programma
2. **Seleziona** la cartella contenente le ROM
3. **Configura** le opzioni (modalità test, regione geografica)
4. **Scansiona** per trovare duplicati
5. **Rivedi** il report dettagliato
6. **Pulisci** per organizzare le ROM

### Opzioni di Configurazione
- **🧪 Modalità Test**: Simula le operazioni senza modificare file
- **👁️ Mostra File Mantenuti**: Visualizza anche i duplicati che rimangono
- **📋 Modalità Copia**: Copia invece di spostare i file
- **🌍 Priorità Geografica**: Scegli Europa, USA o Giappone

### File di Configurazione
Il programma salva automaticamente le preferenze in `config.ini`:
```ini
[Settings]
language = it
test_mode = True
show_kept = True
copy_mode = False
geographic_region = EUROPA
last_folder = C:\ROM_Collection
```

## 📊 Statistiche del Progetto

- **2.251 righe** di codice Python ottimizzato
- **20 lingue** supportate con traduzioni complete
- **100+ piattaforme** gaming supportate  
- **Oltre 100.000 giochi** nel database DAT MAME
- **Sistema di priorità** con 15+ livelli di qualità
- **Zero perdite di dati** garantite

## 🔧 Funzionalità Avanzate

### Sistema DAT MAME
```python
# Caricamento automatico dei database DAT
self.load_dat_files()  # Supporta .dat e .dat.gz
# Protezione intelligente di BIOS e parent games
if game_name in self.bios_games:
    protected_files.add(filepath)
```

### Algoritmo di Priorità
```python
def calculate_priority(self, filename):
    # File senza tag [] = priorità massima (15.000 punti)
    # Tag geografici = fino a 1.000 punti  
    # Tag qualità = da -10.000 a +9.000 punti
    return priority_score
```

### Gestione Multi-Disco
Il programma riconosce automaticamente giochi multi-disco e li tratta come entità separate:
- `Game (Disk 1).zip` e `Game (Disk 2).zip` rimangono separati
- Supporto per pattern: Disk, Disc, CD, Part, Side, Tape, etc.

## 🤝 Contributi

I contributi sono benvenuti! Aree di interesse:
- **Nuove traduzioni** per lingue non ancora supportate
- **Database DAT aggiornati** per nuove piattaforme
- **Miglioramenti algoritmo** di priorità
- **Supporto per nuove piattaforme** gaming

## 🐛 Segnalazione Bug

Per segnalare bug o richiedere funzionalità:
1. Apri un **Issue** su GitHub
2. Includi **log dettagliato** e **file di test**
3. Specifica **versione OS** e **versione Python**

## 📄 Licenza

Questo progetto è distribuito sotto **Licenza MIT**. Vedi il file `LICENSE` per maggiori dettagli.

## 👨‍💻 Sviluppatore

**FADESoft** - *Novembre 2025*

- 📧 **Email**: denz.android@gmail.com
- 💻 **GitHub**: denz87

---

## 🙏 Ringraziamenti

- **Comunità MAME** per i database DAT
- **Emulation communities** per i standard di naming delle ROM

---

##  DOWNLOAD ed USO

- Per chi non volesse cimentarsi nella compilaizone del programma,
  nella cartella /dist/ è gia presente la versione compilata .exe
  pronta all'uso.

---

### ⚡ Quick Start

# Installazione dipendenze
pip install pillow

# Esecuzione
python rom_cleaner.py
```

**🎮 Buon gaming con le tue ROM ottimizzate!**
