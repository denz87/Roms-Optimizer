#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROM Cleaner - Strumento per la rimozione dei doppioni delle ROM
Mantiene solo la migliore versione basandosi su tag geografici e di qualità
"""

import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import base64
import tempfile

# Icona integrata del programma in formato base64
ICON_DATA = '''
AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAADg07n/4dS6/+LUu//i1bz/49a9/+TWvv/k17//5djA/+bZwf/m2cL/5trD/+baw//m28T/5tvE/+fbxf/n28X/59vF/+fbxf/n28T/5trE/+baw//m2cP/5tnC/+bYwf/l2MD/5Ne//+TWvv/j1r7/4tW9/+LUvP/h1Lv/4NO5/+HTuv/h1Lv/4tW9/+PWvv/k17//5djA/+bZwf/m2cL/5trD/+bbxP/n28X/59zG/+fcxv/o3cf/6N3H/+jdx//o3cf/6N3H/+jdx//n3Mb/59zF/+fbxf/n28T/59rD/+bZwv/l2MH/5djA/+TXv//j1r7/4tW9/+LUvP/h1Lv/4dS7/+LVvf/j1r7/5Ne//+XYwf/m2cL/59rD/+fbxP/n3MX/59zG/+jdyP/p3sj/6d7J/+neyv/p38r/6d/K/+nfyv/p3sr/6d7J/+jdyP/n3Mb/5drE/+XaxP/k2cP/5NjC/+TXwP/m2MH/5djB/+TXv//j1r7/4tW9/+LUu//i1b3/49a+/+TXv//l2MD/5tnC/+faw//n28X/59zG/+jdx//n3Mf/59zI/+jdyf/o3sr/6N7K/+jey//o3sv/6N7L/+jeyv/n3cn/6+HO//Lp1v/17Nj/9OrV//Pn0f/z6NL/8efR/+faw//m2cH/5djB/+TXv//j1r7/4tW9/+PWvv/k17//5djA/+bZwv/m2sP/5tvF/+jdxv/o3sj/6N3I//Ln0//06tb/8unV//bs2v/27dr/9u3b//Xs2f/z6df/9Oza//fu3P/n2cT/w7GZ/6GQev+NgGz/g3ln/4d7aP+snIT/59vF/+fbxP/m2cH/5djA/+TXv//j1r7/5Ne//+XYwP/m2cL/5trD/+fbxf/n3Mb/6N3I/+jdyf/v5dH/xryo/7uwnf/Fu6j/t6yY/7esmf+3rJn/vLKg/8a8q//Cspz/joBs/1tiW/9SeID/Soih/0mVuP9cr9L/Rpe//zRhdf+Uh3P/8eXO/+TXwf/m2cH/5djA/+TXv//l2MD/5tnB/+bZw//n28X/5tvF/+jdx//p3sr/9evX/66kkf90bWL/bGRX/0E4Kv+Xk4v/kIuC/5OPh/9+dWn/OysY/0ZeYf9XoL3/T7Di/2bP+/9y3P//W8Dy/2zS/f9ly/r/RKXc/2FlXP/q3MP/5tvF/+bZwv/l2MH/5NfA/+XYwf/m2cL/59vE/+bbxf/s4cv/7uPP/+HWwv/x59P/f3Ri/93c2v+uqaH/YUYh/5iUi//+////+fb0/2dqYv9frc//Xsb6/2fO/v9szvr/VLLi/2rM+P9jxPL/Xb3r/2rM+P9GpNf/XmZh/+fYv//n3cf/5trD/+bZwv/l2MD/5tnC/+faw//m28T/6+DK/9vQu/96cF7/dm1e/392aP9KQjT/e3Nn/2lcSP+wg0b/i2Qv/3JsYP/t7u3/gH51/0+Knv9v1///Wrjn/2TG9P9lx/X/XLzs/2zQ/f9bu+r/a877/0mo2v9hZl//69zE/+jdx//m28T/5trD/+bZwf/m2cL/59vE/+XZw//37Nb/nZJ+/5mWj//7////enRr/3JXMf+mej7/w5BM/8KRT//Snln/imEr/4iEfP//////l4l7/013gv9v2P//Wbjn/2nL+f9fwO//as36/2DA7/9oy/n/S6fX/2lqYP/v4cr/593H/+fcxf/m2sT/5tnC/+baw//m28X/5drE//fs1/+bkHz/uLWx/5aSiv+BXSr/055X/8iVUP+ddDv/tolL/8iVUf9tUy//ubm1//3/////////mIt+/1GJmv9r1f//W7rp/2zP/P9rzvz/ZMXz/2XH9/9LpNH/cW9i//Hlz//n3Mj/6NzG/+bbxP/m2sP/59rE/+fcxf/m28X/9evW/6eciP9/fHf/fGI+/9CbU/+vgkX/cV1A/3BuaP+Maz7/eVkt/5+fnf//////8vT1//T39//9/Pz/cW1i/1+32P9gw/P/ZMTx/2zN+f9nyPX/ac3+/0igzv92cGL/8+jS/+fcyP/o3cf/59zF/+baw//n28T/59zG/+bbxv/16tb/rKGO/1ZQRf+gekb/zZhS/2lTM//Iy8z/7ezr/0g3H/+Xkor///////P19f/1+Pj/8/X1//7////Qx7//T29z/2za//9mzfn/b9r//23V//9s0v//QHuX/5aJdf/27Nj/59zI/+neyP/n3Mb/5tvE/+fbxf/o3cf/5tvH//Xr1v+roY7/V1FH/6J7R//Ajkr/ZlhF//T09P/4+fn/zc7L//b39//2+Pn/9ff4//X4+P/1+Pj/8/X1//////+EfXL/T4ug/2Snvv9XgYv/Um1y/0peZP9CQTv/zsKt//Hn1P/o3cn/6d7J/+jdx//m28X/59vF/+jdx//m3Mf/9uzY/6abh/+Cf3r/fGNA/9SeVP96XTb/lpeV//T3+v//////9ff3//X3+P/1+Pj/9fj4//X4+P/1+Pj/9ff3//X4+P/19/f/9vn5//T19P9oW0v/QFNp/0ptmv9JdrD/SofQ/zVLYP/CtJz/8+rY/+jdyf/p3sn/6N3H/+fbxf/n3MX/6N3H/+bcx//47tr/m5B8/7Wzrv+YlIz/e1cl/8eTTv+OaTf/c2FH/5yYj//09vf/9fj4//X3+P/19/f/9ff4//X4+P/y9PT//////7Wvpv8yTGf/R3qz/0tqjP9CVWf/amVa/+Taxv/s4tD/6d/L/+neyf/o3cf/59vF/+fcxf/o3cf/5tzH//ju2v+ckX7/raql//////+TkIr/ZVQ5/35iO/9sVDP/b2ZY//Dy8v/4+vv/8/b2//f5+v/1+Pj/9Pb3//b4+P/09vf/9fb3/7Wvpf9iVkP/Plhw/z1FSf/Mvqf/9e3c/+jey//q38z/6d7K/+jdyP/n3MX/59vF/+jdx//n3Mf/+O7a/52Rfv+qqKP///////////+FgXn/qqqo/+nt8f/5+vv/+fv7//Hz8//7/Pz/8PLy//b39//6/Pz/9Pf3//f5+v/z9fX//////62kmP84aZz/OFyA/7Ghiv/17dz/6N7L/+rfzP/p3sn/6N3H/+fcxf/m28X/6N3H/+bbx//47dn/nZF+/6qoov///////f///4mDeP/T0s7/9/n5/42Hfv/Ewr3/lI+G/8vKxv9iWkz/eXFm/8/Oyv+Nh33//v///726tP+koZz/0cq//zxaev81YpL/lIZw//fu3f/n3sv/6d/L/+neyf/o3cf/5tvF/+bbxP/n3Mb/5tvG//ft2f+ckX7/qaeh////////////iIJ4/8vKx//y9PT/YllL/0xCMv+3tK7/e3Ro/8nIxP+blo3/f3ht/4V+c/95cmb/d29j/5qWj//r5t//RVhq/zVsqf94bl3/9OrX/+jey//p38r/6d7I/+fcxv/m28T/5trE/+fcxf/m28X/9+3Y/5yRff+ppqD///////////+Ignj/zMzI//Hz8/9rY1b/op6W/3dvY/9vZ1r/397c/6aimv+Ff3T/XFNE/3FpXf9MQjH/lI+H//38+P9XXmP/NnO1/19dVf/r4Mv/6uDM/+neyf/o3cj/59zF/+fbxP/m2sP/5tvF/+XaxP/37Nf/nJB8/6eln////////////4iCeP/My8f/9fj4/2hgUv9waFv/oZ2V/7i1r/9fVkf/bmZZ/8rJxf9XTj//4+Lg/4N8cf+Mh37//////2VjXP84dLf/TFRZ/9zOt//t49D/6N3I/+jdx//n28X/5trD/+bZwv/m2sT/5NnD//br1v+ckHz/qaah///////+////iYN4/8nJxP//////4+Tj/93d2//5+vr//P7+/9vc2v/o6ej/+vv8/+nq6f/4+vr/8fPy/+7w8P/7/v//aWBR/ztzsP8+VGn/x7ed//Hn0//n3Mb/59zG/+bbxP/m2cL/5dnB/+baw//k2cL/9uvV/5qPev+gnZf///////////+LhXv/ycjE///////4+vv/+/7+//X39//09vb//P7+//n7+//19/f/+fv8//X4+P/v8O7/7Ovn//Lz8f9bTTj/P22e/zdbgP+tnIL/9OrV/+XaxP/n28X/5trD/+bZwv/l2MD/5tnC/+XZw//r4Mr/08ex/3BnV/98dWj/gXlt/1pQQP/Qz8z/+/7///Hz8//z9fX/9Pb2//T29v/z9fX/8/X1//T29v/z9vb/8vTz/9fTyf/i3NL/ioN2/2VUOv9KbI7/NGSX/5CCav/06tT/5NnD/+baxP/m2cL/5djB/+TXv//l2MH/5tnC/+baw//s4cv/49jC/8/Erv/e077/eW1b/9TSz////////f39///////////////////////////////////////8/Pv/6+fe/4Z+cf+Ee2r/28yz/0hdcP85eL3/cmhY/+/jy//l2cP/5tnC/+bZwf/l18D/49a+/+TXwP/l2cH/59rD/+Xaw//p3sj/7OHL//vw2/+XjHn/ioZ+/8nJxv+/vrr/wL+8/8C/vP/Av7z/wL+8/8C/vP/Av7z/wL+7/8XEwP+AeGv/fHFe//Tr2P/p3MX/WltY/ydRfv9uZlj/7uLK/+XYwv/m2MH/5djA/+TXv//i1b3/49e+/+TYwP/m2cL/5trD/+bbxP/m28X/6d3H/+bbxf+aj3v/iX5q/42Bbv+MgW7/jIFu/4yBbv+Mgm//jIJu/4yBbv+Ngm//iX5r/56TgP/u5ND/6d/K/+7jzv/GuqT/inxm/9DDrf/r3sj/5djA/+XYwP/k17//49a9/+LVvP/j1r3/5Ne//+XYwP/m2cH/5trD/+bbxP/n3MX/6d7H//Xq1f/27Nf/9uzY//ft2f/37dr/9+7a//fu2v/37tr/9+3a//ft2f/37dn/9uvX/+neyf/o3cj/59zG/+3izP/06dL/697H/+XYwf/l2MD/5Ne//+PWvf/i1bz/4dS7/+LVvP/j1r3/5Ne//+XYwP/m2MH/5trD/+faxP/m28X/5NnD/+XaxP/m28X/5tvG/+bbx//n3Mj/59zI/+bcyP/n3Mf/59vH/+bbxv/m28X/6N3H/+fcxv/n3MX/5dnC/+PWv//k18D/5djA/+TXv//j1r7/4tW8/+HUu//h07r/4dS7/+LVvP/j1r3/49a+/+TXv//l2MH/5tnC/+baw//m28T/5tvF/+fcxf/n3Mb/6NzH/+jdx//o3cf/6N3H/+jdx//o3cf/59zG/+fcxf/m28X/5tvE/+baw//m2cL/5djB/+TXwP/k177/49a9/+LVvP/h1Lv/4dO6/+DSuP/g07r/4dS6/+LVvP/i1b3/49a+/+TXv//l2MD/5djB/+bZwv/m2sP/5trD/+baxP/m28X/59vF/+fbxf/n28X/59vF/+bbxf/m28T/5trE/+baw//m2cL/5tnB/+XYwP/k17//49a+/+LVvf/i1Lz/4dS7/+HTuv/g0rn/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
'''

from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import hashlib
from collections import defaultdict
import shutil
import configparser

class RomCleaner:
    def set_icon(self):
        """Imposta l'icona della finestra usando i dati integrati"""
        try:
            # Decodifica i dati base64 dell'icona
            icon_bytes = base64.b64decode(ICON_DATA)
            
            # Crea un file temporaneo con l'icona
            with tempfile.NamedTemporaryFile(suffix='.ico', delete=False) as temp_icon:
                temp_icon.write(icon_bytes)
                temp_icon_path = temp_icon.name
            
            # Imposta l'icona della finestra
            self.root.iconbitmap(temp_icon_path)
            
            # Pulisce il file temporaneo (opzionale, il sistema lo farà alla chiusura)
            try:
                os.unlink(temp_icon_path)
            except:
                pass  # Ignora errori nella pulizia
                
        except Exception as e:
            # Se fallisce, continua senza icona
            pass
    
    def create_png_image(self):
        """Carica il logo esterno logo.png per l'interfaccia."""
        try:
            from PIL import Image, ImageTk
            
            # Carica il file logo.png dalla directory del programma
            logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
            if not os.path.exists(logo_path):
                return None
                
            # Carica l'immagine
            pil_image = Image.open(logo_path)
            pil_image.load()
            
            # Ridimensiona per il titolo mantenendo le proporzioni (max 80 altezza per header)
            original_width, original_height = pil_image.size
            max_height = 80
            if original_height > max_height:
                ratio = max_height / original_height
                new_width = int(original_width * ratio)
                pil_image = pil_image.resize((new_width, max_height), Image.Resampling.LANCZOS)
            
            # Converte per Tkinter
            tk_image = ImageTk.PhotoImage(pil_image)
            
            return tk_image
            
        except Exception as e:
            # Se fallisce, ritorna None (nessuna immagine)
            return None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ROMS OPTIMIZER v0.8.1 - Advanced ROM Management")
        
        # Dimensioni fisse ottimali trovate dall'utente
        self.window_width = 850
        self.window_height = 733
        
        # Imposta dimensioni fisse e impedisce il ridimensionamento per mantenere il layout perfetto
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.minsize(self.window_width, self.window_height)
        self.root.maxsize(self.window_width, self.window_height)  # Blocca le dimensioni
        
        # Configura il colore di sfondo della finestra
        self.root.configure(bg='#ffffff')
        
        # Centra la finestra sullo schermo con le dimensioni precise
        self.center_window()
        
        # Imposta l'icona integrata
        self.set_icon()
    
    def center_window(self):
        """Centra la finestra sullo schermo usando le dimensioni precise"""
        # Usa le dimensioni definite invece di quelle rilevate per maggiore precisione
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcola posizione centrale
        x = max(0, (screen_width - self.window_width) // 2)
        y = max(0, (screen_height - self.window_height) // 2)
        
        # Applica posizione centrata mantenendo le dimensioni fisse
        self.root.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')
        
        # Base priorità geografiche secondo definizioni ufficiali (usata come template per le modalità)
        # Ordine di default: Italia > Europa > USA > UK/Inglese > Giappone/Asia > Altri
        self._geographic_base = {
            # Tag geografiche secondo definizioni ufficiali
            # Italiano (massima priorità)
            '(I)': 1000, '(Ita)': 1000, 'Italy': 1000,
            
            # Europa (seconda priorità) - secondo definizioni ufficiali
            '(E)': 900, 'Europe': 900, '(PAL)': 880,  # Europe / European
            '(F)': 850, '(Fre)': 850, 'France': 850,  # France / French
            '(G)': 840, '(Ger)': 840, 'Germany': 840,  # Germany
            '(S)': 830, '(Spa)': 830, 'Spain': 830,   # Spain / Spanish
            '(D)': 820, '(H)': 820, '(NL)': 820, 'Netherlands': 820,  # Netherlands / Holland
            '(Dut)': 820, 'Dutch': 820,              # Dutch
            '(FN)': 810, '(Fin)': 810, 'Finland': 810, 'Finnish': 810,  # Finland / Finnish
            '(No)': 800, '(Nor)': 800, 'Norway': 800, 'Norwegian': 800,  # Norway / Norwegian
            '(SW)': 790, '(Swe)': 790, 'Sweden': 790, 'Swedish': 790,    # Sweden and Switzerland / Swedish
            '(GR)': 780, '(Gre)': 780, 'Greece': 780, 'Greek': 780,      # Greece / Greek
            '(FC)': 770, 'French Canada': 770,       # French Canada
            '(Pol)': 760, 'Polish': 760,             # Polish
            '(Ser)': 750, 'Serbian': 750,            # Serbian
            
            # USA/Americano (terza priorità) - secondo definizioni ufficiali
            '(U)': 700, '(4)': 700, 'USA': 700, 'United States': 700,  # USA and United States / USA and Brazil NTSC
            '(NTSC)': 680, 'American': 680,          # American / NTSC
            
            # Inglese/UK (quarta priorità) - secondo definizioni ufficiali
            '(UK)': 650, 'England': 650, 'United Kingdom': 650,  # United Kingdom
            '(Eng)': 640, 'English': 640,            # English
            
            # Australia e Asia - secondo definizioni ufficiali
            '(A)': 600, 'Australia': 600, 'Asia': 590,  # Australia / Asia
            
            # Brasile/Portoghese - secondo definizioni ufficiali
            '(Bra)': 580, 'Brazil': 580, 'Brazilian': 580,      # Brazilian / Portuguese
            '(Por)': 570, 'Portuguese': 570,         # Portuguese
            
            # Giappone/Asia - secondo definizioni ufficiali
            '(J)': 500, '(1)': 500, 'Japan': 500,    # Japan and South Korea / Japan and Korea
            '(K)': 480, '(Kor)': 480, 'Korea': 480,  # Korea
            '(C)': 460, '(Ch)': 460, 'China': 460,   # China
            '(HK)': 450, 'Hong Kong': 450,           # Hong Kong
            
            # Altri
            '(R)': 400, '(Rus)': 400, 'Russia': 400,
            '(PD)': 300, 'Public Domain': 300,
            '(Unk)': 100, 'Unknown': 100,
        }

        # Imposta la mappa effettiva usata da calculate_priority tramite la modalità
        # Di default useremo la modalità "EUROPA" (che rispecchia la mappa iniziale)
        self.geographic_priority = dict(self._geographic_base)
        
        # Fallback per file senza tag geografici specifici
        self.fallback_priority = 50  # Priorità per ROM senza tag geografici chiari
        
        # Priorità tag qualità secondo definizioni ufficiali (dal più alto al più basso)
        # IMPORTANTE: File senza tag [] hanno priorità MASSIMA (originali/puliti)
        self.quality_priority = {
            # Tag positivi (ma sempre meno di nessun tag)
            '[!]': 9000,   # Verified Good Dump: Verified and perfectly playable version, a must-have
            '[! p]': 8000, # Pending Dump: Closest copy to date, but still waiting for a true ROM copy
            '[f]': 7000,   # Fixed: Optimized to work better on the emulator
            '[a]': 6000,   # Alternative: Alternative version, usually they fix bugs
            '[T+]': 5000,  # Newer translation: Rom translation, use current rom
            '[T]': 3000,   # Translation: Translation by fans
            
            # Tag neutri/negativi
            '[T-]': 2000,  # Older translation: Translation has outgrown the rom, new one exists
            '[h]': 1000,   # Hacked: Modified version, can be anything from cheat mod to wacky hack
            '[c]': 500,    # Cracked: Cracked version
            '[t]': 400,    # Formed: Usually opens a cheat menu when launching the rom
            '[p]': 300,    # Pirate: Non-original rom
            '[o]': 200,    # Overdump: Size larger than standard cartridge, no emulator changes
            '[b]': -5000,  # Bad Dump: The dump was not done correctly, it's a corrupted version
            '[x]': -10000, # Incorrect checksum
        }
        
        # Bonus per file senza tag di qualità (originali/puliti)
        self.clean_file_bonus = 15000  # Priorità MASSIMA per file senza []
        
        # Sistema DAT MAME per gestione dipendenze
        self.mame_database = {}
        self.parent_games = set()
        self.clone_relationships = {}
        self.bios_games = set()
        self.load_dat_files()
        
        # Sistema di localizzazione
        self.current_language = 'it'  # Default: Italiano
        self.setup_translations()
        
        # Inizializza variabili di configurazione con valori di default
        self.dry_run_var = tk.BooleanVar(value=True)
        self.show_kept_var = tk.BooleanVar(value=True)
        self.copy_mode_var = tk.BooleanVar(value=False)
        self.region_var = tk.StringVar(value='EUROPA')
        self.folder_var = tk.StringVar()
        
        # Carica configurazione salvata PRIMA di creare l'UI
        self.config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.load_config(silent=True)
        
        self.setup_ui()
    
    def setup_translations(self):
        """Carica i dizionari di traduzione dai file JSON esterni"""
        import json
        
        self.translations = {}
        self.lang_codes = [
            'it', 'en', 'fr', 'de', 'es',  # Lingue originali
            'pt', 'ru', 'ja', 'zh', 'ko',  # Portoghese, Russo, Giapponese, Cinese, Coreano
            'nl', 'sv', 'pl', 'ar', 'hi',  # Olandese, Svedese, Polacco, Arabo, Hindi
            'no', 'da', 'fi', 'el', 'tr'   # Norvegese, Danese, Finlandese, Greco, Turco
        ]
        
        # Percorso della cartella lang
        lang_dir = os.path.join(os.path.dirname(__file__), 'lang')
        
        # Carica ogni file di traduzione
        for lang_code in self.lang_codes:
            lang_file = os.path.join(lang_dir, f'{lang_code}.json')
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
                print(f"✅ Caricata lingua: {lang_code}")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"❌ Errore caricando {lang_file}: {e}")
                # Fallback per evitare crash - dizionario vuoto
                self.translations[lang_code] = {
                    'title': f'ROM Cleaner ({lang_code})',
                    'error_title': 'Error'
                }


    def load_dat_files(self):
        """Carica tutti i file DAT MAME dalla cartella dat/ (supporta compressi)"""
        import xml.etree.ElementTree as ET
        import gzip
        
        dat_folder = os.path.join(os.path.dirname(__file__), 'dat')
        if not os.path.exists(dat_folder):
            print("⚠️ Cartella DAT non trovata, modalità base attivata")
            return
        
        dat_files_loaded = 0
        
        # Scansiona ricorsivamente per file .dat e .dat.gz
        for root, dirs, files in os.walk(dat_folder):
            for file in files:
                if file.lower().endswith('.dat') or file.lower().endswith('.dat.gz'):
                    dat_path = os.path.join(root, file)
                    try:
                        self._parse_dat_file(dat_path)
                        dat_files_loaded += 1
                    except Exception as e:
                        print(f"❌ Errore caricando {file}: {e}")
        
        if dat_files_loaded > 0:
            print(f"✅ Database MAME caricato: {dat_files_loaded} file DAT, {len(self.mame_database)} giochi")
            print(f"📊 Parent games: {len(self.parent_games)}, BIOS: {len(self.bios_games)}")
        else:
            print("⚠️ Nessun file DAT valido trovato")
    
    def _parse_dat_file(self, dat_path):
        """Parsa un singolo file DAT XML (supporta compressi)"""
        import xml.etree.ElementTree as ET
        import gzip
        
        try:
            # Verifica se è compresso
            if dat_path.lower().endswith('.dat.gz'):
                with gzip.open(dat_path, 'rt', encoding='utf-8') as f:
                    xml_content = f.read()
                root = ET.fromstring(xml_content)
            else:
                tree = ET.parse(dat_path)
                root = tree.getroot()
            
            for game in root.findall('.//game'):
                game_name = game.get('name')
                if not game_name:
                    continue
                
                description_elem = game.find('description')
                description = description_elem.text if description_elem is not None else game_name
                
                romof = game.get('romof')
                cloneof = game.get('cloneof')
                
                # Informazioni base del gioco
                game_info = {
                    'name': game_name,
                    'description': description,
                    'romof': romof,
                    'cloneof': cloneof,
                    'is_bios': romof is None and cloneof is None,
                    'is_parent': romof is not None and cloneof is None,
                    'is_clone': cloneof is not None
                }
                
                # Aggiungi al database
                self.mame_database[game_name] = game_info
                
                # Categorizza il gioco
                if game_info['is_bios'] or 'bios' in description.lower():
                    self.bios_games.add(game_name)
                elif game_info['is_parent']:
                    self.parent_games.add(game_name)
                elif game_info['is_clone']:
                    parent = cloneof
                    if parent not in self.clone_relationships:
                        self.clone_relationships[parent] = []
                    self.clone_relationships[parent].append(game_name)
                    
        except ET.ParseError as e:
            print(f"❌ Errore XML in {dat_path}: {e}")
        except Exception as e:
            print(f"❌ Errore generico in {dat_path}: {e}")
    
    def load_software_info_content(self):
        """Carica il contenuto delle informazioni software dal file appropriato"""
        try:
            # Determina la lingua corrente
            current_language = getattr(self, 'current_language', 'it')
            
            # Costruisci il percorso del file info software
            script_dir = os.path.dirname(os.path.abspath(__file__))
            info_file = os.path.join(script_dir, 'info', f'info_sft_{current_language}.txt')
            
            # Leggi il contenuto del file
            if os.path.exists(info_file):
                with open(info_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # Fallback al file italiano se il file specifico non esiste
                fallback_file = os.path.join(script_dir, 'info', 'info_sft_it.txt')
                if os.path.exists(fallback_file):
                    with open(fallback_file, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    # Contenuto di emergenza se non ci sono file
                    return "🎮 ROMS OPTIMIZER v0.8.1 DAT MAME\n\n💻 Sviluppato da: FADESoft\n📅 Data rilascio: Novembre 2025\n🔧 Sistema: Ottimizzatore ROMS\n\nFile di informazioni non trovato!"
        
        except Exception as e:
            return f"🎮 ROMS OPTIMIZER v0.8.1 DAT MAME\n\nErrore nel caricamento delle informazioni: {str(e)}"

    def load_info_content(self):
        """Carica il contenuto delle istruzioni dal file appropriato"""
        try:
            # Determina la lingua corrente
            current_language = getattr(self, 'current_language', 'it')
            
            # Costruisci il percorso del file info
            script_dir = os.path.dirname(os.path.abspath(__file__))
            info_file = os.path.join(script_dir, 'info', f'info_{current_language}.txt')
            
            # Leggi il contenuto del file
            if os.path.exists(info_file):
                with open(info_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # Fallback al file italiano se il file specifico non esiste
                fallback_file = os.path.join(script_dir, 'info', 'info_it.txt')
                if os.path.exists(fallback_file):
                    with open(fallback_file, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    # Contenuto di emergenza se non ci sono file
                    return "🎮 ROM Cleaner - Istruzioni di Base\n\nFile di istruzioni non trovato!\nVerifica la cartella 'info/'."
        
        except Exception as e:
            return f"🎮 ROM Cleaner - Errore\n\nErrore nel caricamento delle istruzioni: {str(e)}"
    
    def get_text(self, key, *args):
        """Ottiene il testo tradotto per la lingua corrente"""
        text = self.translations.get(self.current_language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def change_language(self, lang_code):
        """Cambia la lingua dell'interfaccia"""
        if lang_code in self.translations:
            self.current_language = lang_code
            self.refresh_ui()
            self.save_config()
    
    def refresh_ui(self):
        """Aggiorna tutti i testi dell'interfaccia con la nuova lingua"""
        # Aggiorna il titolo della finestra
        self.root.title(f"ROMS OPTIMIZER v0.8.1 - {self.get_text('title')}")
        
        # Aggiorna menu
        try:
            self.file_menu.entryconfig(0, label=self.get_text('menu_language'))
            # Il pulsante guida è al secondo posto (indice 2)
            self.file_menu.entryconfig(2, label=self.get_text('guide_button'))
            # Il pulsante info è al terzo posto (indice 3)
            self.file_menu.entryconfig(3, label=self.get_text('info_button'))
            # L'exit è dopo l'ultimo separatore, quindi indice 5
            self.file_menu.entryconfig(5, label=self.get_text('menu_exit'))
            
            # Aggiorna menubar
            self.menubar.entryconfig(0, label=self.get_text('menu_file'))
        except:
            pass
        
        # Aggiorna tutti i widget dell'interfaccia
        try:
            # Aggiorna elementi UI futuristici
            self.title_label.config(text=self.get_text('title'))
            self.folder_frame.config(text=self.get_text('folder_label'))
            self.browse_button.config(text=self.get_text('browse_button'))
            self.options_frame.config(text=self.get_text('options_frame'))
            self.test_check.config(text=self.get_text('test_mode'))
            self.show_check.config(text=self.get_text('show_kept'))
            self.copy_check.config(text=self.get_text('copy_mode'))
            self.region_frame.config(text=self.get_text('geographic_priority'))
            self.europe_radio.config(text=self.get_text('europe'))
            self.usa_radio.config(text=self.get_text('usa'))
            self.japan_radio.config(text=self.get_text('japan'))
            self.scan_button.config(text=self.get_text('scan_button'))
            self.clean_button.config(text=self.get_text('clean_button'))
            self.clear_button.config(text=self.get_text('clear_log'))
            self.log_frame.config(text=self.get_text('log_frame'))
            self.status_label.config(text=self.get_text('status_ready'))
        except:
            pass
    

    
    def setup_menu(self):
        """Crea la barra dei menu con File, Modalità e Lingua"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Menu File
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.get_text('menu_file'), menu=self.file_menu)
        
        # Sottomenu Lingua
        self.language_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label=self.get_text('menu_language'), menu=self.language_menu)
        
        # Opzioni lingua - create dinamicamente da tutte le lingue disponibili
        # Nomi uniformi per il menu (tutti con formato: bandiera + nome + (regione/paese))
        language_names = {
            'it': '🇮🇹 Italiano (Italia)',
            'en': '🇺🇸 English (USA)', 
            'fr': '🇫🇷 Français (France)',
            'de': '🇩🇪 Deutsch (Deutschland)',
            'es': '🇪🇸 Español (España)',
            'pt': '🇧🇷 Português (Brasil)',
            'ru': '🇷🇺 Русский (Россия)',
            'ja': '🇯🇵 日本語 (日本)',
            'zh': '🇨🇳 中文 (中国)',
            'ko': '🇰🇷 한국어 (대한민국)',
            'nl': '🇳🇱 Nederlands (Nederland)',
            'sv': '🇸🇪 Svenska (Sverige)', 
            'pl': '🇵🇱 Polski (Polska)',
            'ar': '🇸🇦 العربية (السعودية)',
            'hi': '🇮🇳 हिन्दी (भारत)',
            'no': '🇳🇴 Norsk (Norge)',
            'da': '🇩🇰 Dansk (Danmark)',
            'fi': '🇫🇮 Suomi (Suomi)',
            'el': '🇬🇷 Ελληνικά (Ελλάδα)',
            'tr': '🇹🇷 Türkçe (Türkiye)'
        }
        
        # Aggiungi tutte le lingue disponibili al menu
        for lang_code in self.lang_codes:
            if lang_code in self.translations:  # Solo se la traduzione è caricata
                lang_display = language_names.get(lang_code, lang_code.upper())
                self.language_menu.add_command(
                    label=lang_display,
                    command=lambda code=lang_code: self.change_language(code)
                )
        
        # Separatore nel menu File
        self.file_menu.add_separator()
        
        # Aggiungi pulsanti istruzioni e info nel menu File
        current_lang_display = self.current_language.upper()
        self.file_menu.add_command(
            label=self.get_text('guide_button'),
            command=self.show_instructions
        )
        self.file_menu.add_command(
            label=self.get_text('info_button'),
            command=self.show_info
        )
        
        # Separatore e Esci
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.get_text('menu_exit'), 
                                 command=self.root.quit, accelerator="Ctrl+Q")
        
        # Shortcut per uscire
        self.root.bind('<Control-q>', lambda e: self.root.quit())

        
    def setup_modern_styles(self):
        """Configura stili futuristici minimalisti"""
        style = ttk.Style()
        
        # Usa clam per migliore personalizzazione
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        else:
            style.theme_use('default')
        
        # Palette futuristica minimalista - Dark mode elegante
        colors = {
            'bg_main': '#0f1419',         # Nero profondo
            'bg_card': '#1a1f2e',         # Grigio scuro per cards
            'bg_input': '#262b3d',        # Grigio medio per input
            'accent': '#00d4aa',          # Verde acqua brillante
            'accent_hover': '#00b893',    # Verde acqua più scuro
            'secondary': '#7c3aed',       # Viola futuristico
            'secondary_hover': '#6d28d9', # Viola più scuro
            'danger': '#ef4444',          # Rosso moderno
            'text_primary': '#f8fafc',    # Bianco quasi puro
            'text_secondary': '#94a3b8',  # Grigio chiaro
            'text_muted': '#64748b',      # Grigio medio
            'border': '#334155',          # Grigio scuro per bordi
            'glow': '#00d4aa40'           # Effetto glow verde acqua
        }
        
        # Configura il background principale
        style.configure('.',
                       background=colors['bg_main'],
                       foreground=colors['text_primary'])
        
        # Frame principale futuristico
        style.configure('Futuristic.TFrame', 
                       background=colors['bg_main'], 
                       relief='flat',
                       borderwidth=0)
        
        # Cards con effetto minimalista
        style.configure('FuturisticCard.TLabelframe',
                       background=colors['bg_card'],
                       borderwidth=0,
                       relief='flat',
                       labelmargins=(12, 8, 12, 8))
        
        style.configure('FuturisticCard.TLabelframe.Label',
                       background=colors['bg_card'],
                       foreground=colors['accent'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Titoli futuristici
        style.configure('FuturisticTitle.TLabel',
                       background=colors['bg_main'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 22, 'bold'))
        
        style.configure('FuturisticSubtitle.TLabel',
                       background=colors['bg_main'],
                       foreground=colors['text_secondary'],
                       font=('Segoe UI', 11))
        
        # Input moderni
        style.configure('FuturisticEntry.TEntry',
                       fieldbackground=colors['bg_input'],
                       foreground=colors['text_primary'],
                       borderwidth=0,
                       relief='flat',
                       insertcolor=colors['accent'])
        
        # Pulsanti primari - Verde acqua futuristico
        style.configure('PrimaryFuturistic.TButton',
                       background=colors['accent'],
                       foreground=colors['bg_main'],
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'),
                       focuscolor='none')
        
        style.map('PrimaryFuturistic.TButton',
                 background=[('active', colors['accent_hover']),
                           ('pressed', colors['accent'])],
                 foreground=[('active', colors['bg_main'])])
        
        # Pulsanti secondari - Viola futuristico  
        style.configure('SecondaryFuturistic.TButton',
                       background=colors['secondary'],
                       foreground=colors['text_primary'],
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'),
                       focuscolor='none')
        
        style.map('SecondaryFuturistic.TButton',
                 background=[('active', colors['secondary_hover']),
                           ('pressed', colors['secondary'])])
        
        # Pulsanti utility - Minimalisti
        style.configure('UtilityFuturistic.TButton',
                       background=colors['bg_input'],
                       foreground=colors['text_secondary'],
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 9),
                       focuscolor='none')
        
        style.map('UtilityFuturistic.TButton',
                 background=[('active', colors['border']),
                           ('pressed', colors['bg_input'])],
                 foreground=[('active', colors['text_primary'])])
        
        # Checkbox e radiobutton futuristici
        style.configure('FuturisticCheck.TCheckbutton',
                       background=colors['bg_card'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 10),
                       focuscolor='none')
        
        style.configure('FuturisticRadio.TRadiobutton',
                       background=colors['bg_card'],
                       foreground=colors['text_primary'],
                       font=('Segoe UI', 10),
                       focuscolor='none')
        
        # Progress bar futuristica
        style.configure('FuturisticProgress.Horizontal.TProgressbar',
                       background=colors['accent'],
                       troughcolor=colors['bg_input'],
                       borderwidth=0,
                       lightcolor=colors['accent'],
                       darkcolor=colors['accent'])
        
        # Label stato futuristico
        style.configure('FuturisticStatus.TLabel',
                       background=colors['bg_main'],
                       foreground=colors['text_secondary'],
                       font=('Segoe UI', 10))
        

        


    
    def setup_ui(self):
        # Configura stili moderni
        self.setup_modern_styles()
        
        # Barra dei menu
        self.setup_menu()
        
        # Configura background principale
        self.root.configure(bg='#0f1419')
        
        # Frame principale futuristico
        self.main_container = ttk.Frame(self.root, padding="20", style="Futuristic.TFrame")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurazione griglia principale
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=1)  # Colonna destra (log) si espande
        self.main_container.rowconfigure(1, weight=1)     # Riga centrale si espande
        
        # === HEADER CON TITOLO E LOGO ===
        self.header_frame = ttk.Frame(self.main_container, style="Futuristic.TFrame")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        self.header_frame.columnconfigure(1, weight=1)
        
        # Logo del programma
        self.png_image = self.create_png_image()
        if self.png_image:
            self.image_label = ttk.Label(self.header_frame, image=self.png_image, 
                                       style="Futuristic.TLabel")
            self.image_label.grid(row=0, column=0, padx=(0, 20))
        
        # Container titolo futuristico
        title_container = ttk.Frame(self.header_frame, style="Futuristic.TFrame")
        title_container.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N))
        
        self.title_label = ttk.Label(title_container, text=self.get_text('title'), 
                                    style="FuturisticTitle.TLabel")
        self.title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(title_container, text="Advanced ROM Management & Optimization Tool",
                                 style="FuturisticSubtitle.TLabel")
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(3, 0))
        
        # === LAYOUT PRINCIPALE: SINISTRA CONTROLLI, DESTRA LOG ===
        
        # COLONNA SINISTRA - Controlli e opzioni futuristici
        left_panel = ttk.Frame(self.main_container, style="Futuristic.TFrame")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.N, tk.S), padx=(0, 20))
        
        # Selezione cartella - Design futuristico
        self.folder_frame = ttk.LabelFrame(left_panel, text=self.get_text('folder_label'), 
                                          padding="15", style="FuturisticCard.TLabelframe")
        self.folder_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.folder_frame.columnconfigure(0, weight=1)
        
        folder_input_frame = ttk.Frame(self.folder_frame, style="Futuristic.TFrame")
        folder_input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        folder_input_frame.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_input_frame, textvariable=self.folder_var, 
                                    width=35, font=('Segoe UI', 10),
                                    style="FuturisticEntry.TEntry")
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10), pady=5)
        
        self.browse_button = ttk.Button(folder_input_frame, text=self.get_text('browse_button'), 
                                      command=self.browse_folder, width=12,
                                      style="UtilityFuturistic.TButton")
        self.browse_button.grid(row=0, column=1, pady=5)
        
        # Opzioni di processing - Card futuristica
        self.options_frame = ttk.LabelFrame(left_panel, text=self.get_text('options_frame'), 
                                          padding="15", style="FuturisticCard.TLabelframe")
        self.options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.test_check = ttk.Checkbutton(self.options_frame, text=self.get_text('test_mode'), 
                                        variable=self.dry_run_var, style="FuturisticCheck.TCheckbutton",
                                        command=self.on_option_changed)
        self.test_check.grid(row=0, column=0, sticky=tk.W, pady=4)
        
        self.show_check = ttk.Checkbutton(self.options_frame, text=self.get_text('show_kept'), 
                                        variable=self.show_kept_var, style="FuturisticCheck.TCheckbutton",
                                        command=self.on_option_changed)
        self.show_check.grid(row=1, column=0, sticky=tk.W, pady=4)
        
        self.copy_check = ttk.Checkbutton(self.options_frame, text=self.get_text('copy_mode'), 
                                        variable=self.copy_mode_var, style="FuturisticCheck.TCheckbutton",
                                        command=self.on_option_changed)
        self.copy_check.grid(row=2, column=0, sticky=tk.W, pady=4)
        
        # Priorità geografica - Card futuristica
        self.region_frame = ttk.LabelFrame(left_panel, text=self.get_text('geographic_priority'), 
                                         padding="15", style="FuturisticCard.TLabelframe")
        self.region_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.europe_radio = ttk.Radiobutton(self.region_frame, text=self.get_text('europe'), 
                                          variable=self.region_var, value='EUROPA',
                                          command=lambda: self.set_geographic_mode(self.region_var.get()),
                                          style="FuturisticRadio.TRadiobutton")
        self.europe_radio.grid(row=0, column=0, sticky=tk.W, pady=3)
        
        self.usa_radio = ttk.Radiobutton(self.region_frame, text=self.get_text('usa'), 
                                       variable=self.region_var, value='USA',
                                       command=lambda: self.set_geographic_mode(self.region_var.get()),
                                       style="FuturisticRadio.TRadiobutton")
        self.usa_radio.grid(row=1, column=0, sticky=tk.W, pady=3)
        
        self.japan_radio = ttk.Radiobutton(self.region_frame, text=self.get_text('japan'), 
                                         variable=self.region_var, value='GIAPPONE',
                                         command=lambda: self.set_geographic_mode(self.region_var.get()),
                                         style="FuturisticRadio.TRadiobutton")
        self.japan_radio.grid(row=2, column=0, sticky=tk.W, pady=3)
        
        # === PULSANTI GRID FUTURISTICO ===
        button_frame = ttk.Frame(left_panel, style="Futuristic.TFrame")
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 15))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # Prima riga - Pulsanti principali
        self.scan_button = ttk.Button(button_frame, text=self.get_text('scan_button'), 
                                    command=self.scan_duplicates,
                                    style="PrimaryFuturistic.TButton")
        self.scan_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 8), pady=(0, 8))
        
        self.clean_button = ttk.Button(button_frame, text=self.get_text('clean_button'), 
                                     command=self.clean_duplicates, state='disabled',
                                     style="SecondaryFuturistic.TButton")
        self.clean_button.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 8))
        
        # Seconda riga - Pulsante utility centrato
        self.clear_button = ttk.Button(button_frame, text=self.get_text('clear_log'), 
                                     command=self.clear_log,
                                     style="UtilityFuturistic.TButton")
        self.clear_button.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # COLONNA DESTRA - Log futuristico
        right_panel = ttk.Frame(self.main_container, style="Futuristic.TFrame")
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        self.log_frame = ttk.LabelFrame(right_panel, text=self.get_text('log_frame'), 
                                       padding="15", style="FuturisticCard.TLabelframe")
        self.log_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        
        # Area di log con stile futuristico dark
        self.log_text = ScrolledText(self.log_frame, width=65, height=28, wrap=tk.WORD,
                                   font=('JetBrains Mono', 9),
                                   bg='#0f1419', fg='#f8fafc',
                                   selectbackground='#00d4aa', selectforeground='#0f1419',
                                   insertbackground='#00d4aa',
                                   relief=tk.FLAT, borderwidth=0)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === BARRA DI PROGRESSO FUTURISTICA IN FONDO ===
        self.progress_frame = ttk.Frame(self.main_container, style="Futuristic.TFrame")
        self.progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        self.progress_frame.columnconfigure(0, weight=1)
        
        # Label stato futuristico
        self.status_label = ttk.Label(self.progress_frame, text=self.get_text('status_ready'), 
                                     style="FuturisticStatus.TLabel")
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # Container per progress bar con percentuale sovrapposta
        progress_container = ttk.Frame(self.progress_frame, style="Futuristic.TFrame")
        progress_container.grid(row=1, column=0, sticky=(tk.W, tk.E))
        progress_container.columnconfigure(0, weight=1)
        
        # Progress bar futuristica (modalità determinate per controllo completo)
        self.progress = ttk.Progressbar(progress_container, mode='determinate', 
                                      style="FuturisticProgress.Horizontal.TProgressbar",
                                      length=400, maximum=100, value=0)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Inizializzazione variabili
        self.duplicates = {}
        self.singles = {}
        
        # Applica la modalità geografica iniziale
        try:
            self.set_geographic_mode(self.region_var.get())
        except Exception:
            pass
        
    def load_config(self, silent=False):
        """Carica le impostazioni dal file config.ini"""
        config = configparser.ConfigParser()
        
        # Valori di default
        defaults = {
            'language': 'it',
            'test_mode': True,
            'show_kept': True,
            'copy_mode': False,
            'geographic_region': 'EUROPA',
            'last_folder': ''
        }
        
        try:
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')
                
                # Carica impostazioni dalla sezione [Settings]
                if config.has_section('Settings'):
                    # Lingua
                    language = config.get('Settings', 'language', fallback=defaults['language'])
                    if language in self.translations:
                        self.current_language = language
                    
                    # Impostazioni booleane
                    self.dry_run_var.set(config.getboolean('Settings', 'test_mode', fallback=defaults['test_mode']))
                    self.show_kept_var.set(config.getboolean('Settings', 'show_kept', fallback=defaults['show_kept']))
                    self.copy_mode_var.set(config.getboolean('Settings', 'copy_mode', fallback=defaults['copy_mode']))
                    
                    # Regione geografica
                    region = config.get('Settings', 'geographic_region', fallback=defaults['geographic_region'])
                    self.region_var.set(region)
                    
                    # Ultima cartella
                    last_folder = config.get('Settings', 'last_folder', fallback=defaults['last_folder'])
                    if last_folder and os.path.exists(last_folder):
                        self.folder_var.set(last_folder)
                    
                    if not silent and hasattr(self, 'log_text'):
                        self.log("✅ Configurazione caricata da config.ini")
                else:
                    self.create_default_config(silent=silent)
            else:
                self.create_default_config(silent=silent)
                
        except Exception as e:
            if not silent and hasattr(self, 'log_text'):
                self.log(f"⚠️ Errore nel caricamento configurazione: {e}")
            self.create_default_config(silent=silent)
    
    def create_default_config(self, silent=False):
        """Crea il file di configurazione con valori di default"""
        try:
            config = configparser.ConfigParser()
            config['Settings'] = {
                'language': self.current_language,
                'test_mode': str(self.dry_run_var.get()),
                'show_kept': str(self.show_kept_var.get()),
                'copy_mode': str(self.copy_mode_var.get()),
                'geographic_region': self.region_var.get(),
                'last_folder': self.folder_var.get()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
            
            if not silent and hasattr(self, 'log_text'):
                self.log("📁 Creato nuovo file config.ini con impostazioni di default")
            
        except Exception as e:
            if not silent and hasattr(self, 'log_text'):
                self.log(f"❌ Errore nella creazione config.ini: {e}")
    
    def save_config(self):
        """Salva le impostazioni correnti nel file config.ini"""
        try:
            config = configparser.ConfigParser()
            config['Settings'] = {
                'language': self.current_language,
                'test_mode': str(self.dry_run_var.get()),
                'show_kept': str(self.show_kept_var.get()),
                'copy_mode': str(self.copy_mode_var.get()),
                'geographic_region': self.region_var.get(),
                'last_folder': self.folder_var.get()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
            
            # Log silenzioso per non intasare il log durante l'uso normale
            
        except Exception as e:
            self.log(f"⚠️ Errore nel salvataggio configurazione: {e}")
    
    def on_option_changed(self):
        """Callback per salvare configurazione quando cambiano le opzioni"""
        self.save_config()
    
    def update_ui(self):
        """Aggiorna l'interfaccia utente per mantenerla responsiva"""
        try:
            self.root.update_idletasks()
            self.root.update()
            # Piccola pausa per evitare il 100% CPU
            import time
            time.sleep(0.001)  # 1ms di pausa
        except tk.TclError:
            # Finestra chiusa durante l'operazione
            pass
    
    def update_progress(self, value, status_text=None):
        """Aggiorna la progress bar con percentuale"""
        try:
            # Assicura che il valore sia tra 0 e 100
            value = max(0, min(100, value))
            
            # Aggiorna la barra di progresso
            self.progress['value'] = value
            
            # Aggiorna il testo di stato se fornito
            if status_text:
                self.status_label.config(text=status_text)
            
            # Aggiorna l'interfaccia
            self.update_ui()
        except Exception as e:
            pass
    
    def reset_progress(self):
        """Reset della progress bar allo stato iniziale"""
        self.update_progress(0, self.get_text('status_ready'))
    
    def start_progress_animation(self, status_text):
        """Avvia animazione progress per operazioni di durata indefinita"""
        self.status_label.config(text=status_text)
        self.progress.config(mode='indeterminate')
        self.progress.start(10)  # Velocità animazione
    
    def stop_progress_animation(self):
        """Ferma animazione e torna a modalità normale"""
        self.progress.stop()
        self.progress.config(mode='determinate')
        self.reset_progress()
        
    def browse_folder(self):
        folder = filedialog.askdirectory(title=self.get_text('folder_label'))
        if folder:
            self.folder_var.set(folder)
            self.save_config()
            
    def log(self, message):
        """Aggiunge un messaggio al log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Pulisce il log"""
        self.log_text.delete(1.0, tk.END)
        
    def show_info(self):
        """Mostra informazioni sullo sviluppatore"""
        info_window = tk.Toplevel(self.root)
        info_window.title("ROMS OPTIMIZER v0.8.1 - Informazioni Software")
        info_window.geometry("400x500")
        info_window.resizable(False, False)
        
        # Centra la finestra
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Frame principale con padding
        main_frame = ttk.Frame(info_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con logo
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Carica e mostra il logo FFLogo.png
        try:
            from PIL import Image, ImageTk
            logo_path = os.path.join(os.path.dirname(__file__), 'FFLogo.png')
            if os.path.exists(logo_path):
                pil_image = Image.open(logo_path)
                # Ridimensiona il logo (max 80 altezza)
                original_width, original_height = pil_image.size
                max_height = 80
                if original_height > max_height:
                    ratio = max_height / original_height
                    new_width = int(original_width * ratio)
                    pil_image = pil_image.resize((new_width, max_height), Image.Resampling.LANCZOS)
                
                logo_image = ImageTk.PhotoImage(pil_image)
                logo_label = ttk.Label(header_frame, image=logo_image)
                logo_label.image = logo_image  # Mantieni riferimento
                logo_label.pack(pady=(0, 15))
        except Exception:
            pass  # Se fallisce, continua senza logo
        
        # Carica contenuto dal file info della lingua corrente
        info_content = self.load_software_info_content()
        
        # Label semplice per il testo delle informazioni (senza textbox)
        info_label = ttk.Label(main_frame, text=info_content, 
                              font=('Segoe UI', 10), justify=tk.LEFT, 
                              wraplength=550)
        info_label.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Pulsante chiudi
        close_button = ttk.Button(main_frame, text="Chiudi", command=info_window.destroy)
        close_button.pack()
    
    def show_instructions(self):
        """Mostra la finestra di istruzioni del programma"""
        info_window = tk.Toplevel(self.root)
        info_window.title("ROMS OPTIMIZER v0.8.1 - Istruzioni")
        info_window.geometry("800x800")
        info_window.resizable(True, True)
        
        # Centra la finestra
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Frame principale con padding
        main_frame = ttk.Frame(info_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con logo
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Carica e mostra il logo FFLogo.png
        try:
            from PIL import Image, ImageTk
            logo_path = os.path.join(os.path.dirname(__file__), 'FFLogo.png')
            if os.path.exists(logo_path):
                pil_image = Image.open(logo_path)
                # Ridimensiona il logo per l'header (max 60 altezza)
                original_width, original_height = pil_image.size
                max_height = 60
                if original_height > max_height:
                    ratio = max_height / original_height
                    new_width = int(original_width * ratio)
                    pil_image = pil_image.resize((new_width, max_height), Image.Resampling.LANCZOS)
                
                logo_image = ImageTk.PhotoImage(pil_image)
                logo_label = ttk.Label(header_frame, image=logo_image)
                logo_label.image = logo_image  # Mantieni riferimento
                logo_label.pack(pady=(0, 10))
        except Exception:
            pass  # Se fallisce, continua senza logo
        
        # Titolo
        title_label = ttk.Label(header_frame, text="🎮 ROMS OPTIMIZER - Istruzioni Complete", 
                               font=('Arial', 14, 'bold'))
        title_label.pack()
        
        # Carica contenuto dal file info della lingua corrente
        info_content = self.load_info_content()
        
        # Label semplice per il testo delle istruzioni (senza textbox)
        info_label = ttk.Label(main_frame, text=info_content, 
                              font=('Segoe UI', 10), justify=tk.LEFT, 
                              wraplength=750)
        info_label.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Pulsante chiudi
        close_button = ttk.Button(main_frame, text="Chiudi", command=info_window.destroy)
        close_button.pack(pady=(15, 0))

    def load_info_content(self):
        """Carica il contenuto delle informazioni dal file appropriato"""
        try:
            # Determina la lingua corrente
            current_language = getattr(self, 'current_language', 'it')
            
            # Costruisci il percorso del file info
            script_dir = os.path.dirname(os.path.abspath(__file__))
            info_file = os.path.join(script_dir, 'info', f'info_{current_language}.txt')
            
            # Leggi il contenuto del file
            if os.path.exists(info_file):
                with open(info_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # Fallback al file italiano se il file specifico non esiste
                fallback_file = os.path.join(script_dir, 'info', 'info_it.txt')
                if os.path.exists(fallback_file):
                    with open(fallback_file, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    # Contenuto di emergenza se non ci sono file
                    return self.get_fallback_info_content()
        
        except Exception as e:
            # In caso di errore, usa il contenuto di fallback
            return self.get_fallback_info_content()

    def get_fallback_info_content(self):
        """Contenuto informativo di emergenza se i file esterni non sono disponibili"""
        return """� ROM Cleaner - Guida di Base

⚠️ ATTENZIONE: File di configurazione delle informazioni non trovato!

� SCOPO
ROM Cleaner organizza le collezioni di ROM mantenendo solo le versioni migliori.

� ISTRUZIONI BASE
1. Seleziona la cartella contenente le ROM
2. Clicca "Scansiona Duplicati" per analizzare
3. Usa "Modalità Test" per vedere cosa accadrebbe
4. Clicca "Pulisci ROM" per eseguire l'operazione

⚠️ SICUREZZA
• Nessun file viene mai cancellato definitivamente
• I duplicati vengono spostati nella cartella "cleaned"
• Le ROM migliori rimangono nella cartella originale

Per maggiori informazioni, controlla i file nella cartella /info/"""

        info_text.insert(tk.END, info_content)
        info_text.config(state='disabled')  # Rende il testo di sola lettura
        
        # Pulsante chiudi
        close_button = ttk.Button(main_frame, text="Chiudi", command=info_window.destroy)
        close_button.pack(pady=(15, 0))
        
    def get_file_hash(self, filepath):
        """Calcola l'hash MD5 di un file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except:
            return None
        return hash_md5.hexdigest()
        
    def extract_base_name(self, filename):
        """Estrae il nome base per matching DAT MAME mantenendo compatibilità con dischi"""
        # Rimuovi estensione
        name = os.path.splitext(filename)[0]
        original_name = name
        
        # Per MAME: controlla prima se è un nome DAT standard
        name_lower = name.lower()
        if name_lower in self.mame_database:
            return name_lower
        
        # Trova e preserva riferimenti a dischi/parti (questi identificano giochi diversi!)
        disk_patterns = [
            r'[Dd]isk\s*\d+',           # Disk 1, disk 2, Disk1, etc.
            r'[Dd]isc\s*\d+',           # Disc 1, disc 2, etc. 
            r'[Cc]d\s*\d+',             # CD 1, cd 2, etc.
            r'[Pp]art\s*\d+',           # Part 1, part 2, etc.
            r'[Ss]ide\s*[AB12]',        # Side A, Side B, Side 1, Side 2
            r'\(\s*\d+\s*of\s*\d+\s*\)', # (1 of 2), (2 of 3), etc.
            r'[Vv]ol\s*\d+',            # Vol 1, vol 2, etc.
            r'[Tt]ape\s*[AB12]',        # Tape A, Tape B, etc.
            r'[Ff]loppy\s*[AB12]',      # Floppy A, Floppy B, etc.
        ]
        
        disk_info = ""
        for pattern in disk_patterns:
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                disk_info = "_" + match.group(0).replace(" ", "").lower()
                break
        
        # Rimuovi tag tra parentesi quadre
        name = re.sub(r'\[.*?\]', '', name)
        
        # Rimuovi tag tra parentesi tonde (geografici, revisioni, ecc.)
        name = re.sub(r'\(.*?\)', '', name)
        
        # Pulisci spazi multipli e caratteri speciali
        name = re.sub(r'\s+', ' ', name).strip()
        name = re.sub(r'[_-]+', ' ', name).strip()
        
        # Aggiungi informazioni disco per distinguere le parti
        base_name = name.lower() + disk_info
        
        # Verifica finale nel database MAME con nome pulito
        if base_name in self.mame_database:
            return base_name
        
        # Prova senza disk_info per matching più flessibile
        clean_name = name.lower()
        if clean_name in self.mame_database:
            return clean_name
        
        return base_name
        
    def set_geographic_mode(self, mode):
        """Imposta la mappa di punteggi geografici in modo chiuso.
        mode: 'EUROPA', 'USA' o 'GIAPPONE'
        """
        # Copia della mappa base
        base = dict(self._geographic_base)

        italy_keys = ['(I)', '(Ita)', 'Italy']
        usa_keys = ['(U)', '(4)', 'USA', 'United States', '(NTSC)']
        uk_keys = ['(UK)', 'England', 'United Kingdom', '(Eng)', 'English', '(En)', 'Britain', 'GB']
        japan_keys = ['(J)', '(1)', 'Japan']
        europe_keys = ['(E)', 'Europe', '(PAL)', '(F)', '(Fre)', 'France', '(G)', '(Ger)', 'Germany',
                       '(S)', '(Spa)', 'Spain', '(D)', '(H)', '(NL)', 'Netherlands', '(FN)', 'Finland',
                       '(No)', '(Nor)', 'Norway', '(SW)', '(Swe)', 'Sweden', '(GR)', '(Gre)', '(FC)']

        mode = (mode or 'EUROPA').upper()

        if mode == 'USA':
            # USA e UK insieme alla pari (stessi punteggi)
            for k in usa_keys:
                if k in base:
                    base[k] = 1000
            for k in uk_keys:
                if k in base:
                    base[k] = 1000  # UK = USA (stessa priorità)
            for k in europe_keys:
                if k in base:
                    base[k] = 750
            for k in italy_keys:
                if k in base:
                    base[k] = 700
            for k in japan_keys:
                if k in base:
                    base[k] = 600

        elif mode == 'GIAPPONE':
            for k in japan_keys:
                if k in base:
                    base[k] = 1000
            for k in usa_keys:
                if k in base:
                    base[k] = 900
            for k in europe_keys:
                if k in base:
                    base[k] = 750
            for k in italy_keys:
                if k in base:
                    base[k] = 700
            for k in uk_keys:
                if k in base:
                    base[k] = 600

        else:
            # EUROPA: lasciamo la mappa base così com'è
            base = dict(self._geographic_base)

        # Applica la mappa scelta
        self.geographic_priority = base
        # Aggiorna UI/log
        try:
            self.log(self.get_text('geo_mode_set').format(mode))
            self.update_ui()
        except Exception:
            pass
        # Salva configurazione
        self.save_config()
        
    def calculate_priority(self, filename):
        """Calcola la priorità di un file basandosi sui tag"""
        priority = 0
        geographic_found = False
        quality_tag_found = False
        
        # Priorità geografica (ordine: Italia > Europa > USA > Giappone/Asia)
        for tag, value in self.geographic_priority.items():
            if tag in filename:
                priority += value
                geographic_found = True
                break  # Prendi solo il primo tag geografico trovato
        
        # Se non trova tag geografici specifici, usa priorità fallback
        if not geographic_found:
            priority += self.fallback_priority
        
        # Controlla se ha tag di qualità tra parentesi quadre
        has_square_brackets = re.search(r'\[.*?\]', filename)
        
        if not has_square_brackets:
            # BONUS MASSIMO: File senza tag [] (originale/pulito)
            priority += self.clean_file_bonus
            self.log_quality_reason = "🌟 ORIGINALE (senza tag)"
        else:
            # Priorità qualità per file con tag []
            quality_tag_found = False
            for tag, value in self.quality_priority.items():
                if tag in filename:
                    priority += value
                    quality_tag_found = True
                    if tag == '[!]':
                        self.log_quality_reason = "✅ Verified"
                    elif tag == '[b]':
                        self.log_quality_reason = "💥 Bad Dump"
                    elif tag == '[f]':
                        self.log_quality_reason = "🔧 Fixed"
                    elif tag == '[a]':
                        self.log_quality_reason = "🔄 Alternative"
                    elif tag == '[h]':
                        self.log_quality_reason = "🔓 Hack"
                    elif tag == '[x]':
                        self.log_quality_reason = "❌ Bad Checksum"
                    else:
                        self.log_quality_reason = f"📝 {tag}"
                    break
            
            if not quality_tag_found:
                self.log_quality_reason = "❓ Tag sconosciuto"
                
        # Priorità per revisioni (numeri più alti = meglio)
        rev_match = re.search(r'\(Rev\s*(\d+)\)', filename, re.IGNORECASE)
        if rev_match:
            priority += int(rev_match.group(1)) * 10
            
        # Priorità per versioni (numeri più alti = meglio)  
        ver_match = re.search(r'\(V(\d+)\.(\d+)\)', filename, re.IGNORECASE)
        if ver_match:
            major = int(ver_match.group(1))
            minor = int(ver_match.group(2))
            priority += (major * 100 + minor)
            
        # Bonus per multilingual (più lingue = meglio)
        multi_match = re.search(r'\(M(\d+)\)', filename)
        if multi_match:
            priority += int(multi_match.group(1)) * 5
            
        return priority
        
    def get_geographic_info(self, filename):
        """Estrae informazioni geografiche per il log - usa il tag con priorità più alta"""
        best_tag = None
        best_priority = 0
        
        # Trova il tag geografico con priorità più alta
        for tag, priority in self.geographic_priority.items():
            if tag in filename and priority > best_priority:
                best_tag = tag
                best_priority = priority
        
        if best_tag:
            if best_tag in ['(I)', '(Ita)', 'Italy']:
                return "🇮🇹 ITA"
            elif best_tag in ['(U)', '(4)', 'USA', 'United States', '(NTSC)']:
                return "🇺🇸 USA"
            elif best_tag in ['(UK)', '(Eng)', '(En)', 'England', 'Britain', 'GB']:
                return "🇬🇧 UK"
            elif best_tag in ['(E)', 'Europe', '(PAL)']:
                return "🇪🇺 EUR"
            elif best_tag in ['(J)', '(1)', 'Japan']:
                return "🇯🇵 JAP"
            elif best_tag in ['(F)', '(Fre)', 'France']:
                return "🇫🇷 FRA"
            elif best_tag in ['(G)', '(Ger)', 'Germany']:
                return "🇩🇪 GER"
            elif best_tag in ['(S)', '(Spa)', 'Spain']:
                return "🇪🇸 SPA"
            elif best_tag in ['(A)', 'Australia']:
                return "🇦🇺 AUS"
            elif best_tag in ['(Bra)', 'Brazil']:
                return "🇧🇷 BRA"
            else:
                return f"🌍 {best_tag}"
        
        return "❓ UNK"
        for tag in self.geographic_priority.keys():
            if tag in filename:
                if tag in ['(I)', '(Ita)']:
                    return "🇮🇹 ITA"
                elif tag in ['(U)', '(4)', '(NTSC)']:
                    return "🇸 USA"
                elif tag in ['(UK)', '(Eng)', '(En)', 'England', 'Britain', 'GB']:
                    return "�� UK"
                elif tag in ['(E)', '(PAL)']:
                    return "🇪🇺 EUR"
                elif tag in ['(J)', '(1)']:
                    return "🇯🇵 JAP"
                elif tag in ['(F)', '(Fre)']:
                    return "🇫🇷 FRA"
                elif tag in ['(G)', '(Ger)']:
                    return "🇩🇪 GER"
                elif tag in ['(S)', '(Spa)']:
                    return "🇪🇸 SPA"
                elif tag in ['(A)', 'Australia']:
                    return "🇦🇺 AUS"
                elif tag in ['(Bra)', 'Brazil']:
                    return "🇧🇷 BRA"
                else:
                    return f"🌍 {tag}"
        return "❓ UNK"
        
    def get_quality_info(self, filename):
        """Estrae informazioni di qualità per il log"""
        # Controlla se ha tag tra parentesi quadre
        has_square_brackets = re.search(r'\[.*?\]', filename)
        
        if not has_square_brackets:
            return ' 🌟 ORIGINALE'
        
        qualities = []
        if '[!]' in filename:
            qualities.append('✅ Verified')
        elif '[! p]' in filename:
            qualities.append('⏳ Pending')
        elif '[f]' in filename:
            qualities.append('🔧 Fixed')
        elif '[a]' in filename:
            qualities.append('🔄 Alt')
        elif '[b]' in filename:
            qualities.append('💥 Bad')
        elif '[h]' in filename:
            qualities.append('🔓 Hack')
        elif '[T+]' in filename:
            qualities.append('📝 Trans+')
        elif '[T]' in filename:
            qualities.append('📝 Trans')
        elif '[x]' in filename:
            qualities.append('❌ BadCRC')
        elif '[c]' in filename:
            qualities.append('🔓 Crack')
        elif '[p]' in filename:
            qualities.append('🏴‍☠️ Pirate')
        elif '[o]' in filename:
            qualities.append('💿 Over')
        else:
            # Ha [] ma tag non riconosciuto
            square_content = re.findall(r'\[(.*?)\]', filename)
            if square_content:
                qualities.append(f'❓ [{square_content[0]}]')
            
        return ' ' + ' '.join(qualities) if qualities else ' ❓ Tag?'
        
    def scan_duplicates(self):
        """Scansiona la cartella per trovare duplicati"""
        folder = self.folder_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror(self.get_text('error_title'), self.get_text('folder_error'))
            return
        
        # Pulisci automaticamente il log ad ogni nuova scansione
        self.clear_log()
        
        # Disabilita pulsanti durante la scansione per evitare doppi click
        self.scan_button.config(state='disabled', text=self.get_text('scanning'))
        self.clean_button.config(state='disabled')
        
        try:
            self._perform_scan(folder)
        except Exception as e:
            self.log(self.get_text('scan_error').format(str(e)))
            self.reset_progress()
            messagebox.showerror(self.get_text('error_title'), self.get_text('scan_error').format(str(e)))
        finally:
            # Riabilita i pulsanti
            self.scan_button.config(state='normal', text=self.get_text('scan_button'))
            if hasattr(self, 'duplicates') and (self.duplicates or getattr(self, 'singles', {})):
                self.clean_button.config(state='normal')
    
    def _perform_scan(self, folder):
        """Esegue la scansione vera e propria"""
        self.log(self.get_text('scan_start'))
        self.log(self.get_text('scan_folder').format(folder))
        
        # Imposta barra di progresso come determinata
        self.progress.config(mode='determinate', value=0, maximum=100)
        self.update_ui()
        
        # Estensioni ROM COMPLETE per TUTTE le piattaforme
        rom_extensions = {
            # === ARCHIVI COMPRESSI ===
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.lzh', '.ace', '.arj',
            
            # === NINTENDO ===
            # NES/Famicom
            '.nes', '.fds', '.unf', '.unif', '.nsf', 
            # SNES/Super Famicom  
            '.sfc', '.smc', '.swc', '.fig', '.mgd', '.ufo',
            # Game Boy / Game Boy Color
            '.gb', '.gbc', '.cgb', '.sgb',
            # Game Boy Advance
            '.gba', '.agb', '.bin', '.mb', '.sav',
            # Nintendo 64
            '.n64', '.z64', '.v64', '.rom', '.u1', '.ndd',
            # GameCube
            '.gcm', '.iso', '.ciso', '.wbfs', '.rvz', '.dol',
            # Wii
            '.wad', '.wbfs', '.iso', '.ciso', '.rvz',
            # Nintendo DS
            '.nds', '.srl', '.dsi',
            # Nintendo 3DS
            '.3ds', '.cci', '.cxi', '.cia', '.app',
            # Switch
            '.nsp', '.nsz', '.xci', '.xcz', '.nro', '.nso',
            # Virtual Console
            '.wad', '.u8', '.app',
            
            # === SEGA ===
            # Master System
            '.sms', '.gg', '.sc', '.sf7', '.sg',
            # Genesis/Mega Drive
            '.md', '.gen', '.smd', '.bin', '.rom',
            # Sega CD/Mega CD
            '.iso', '.bin', '.cue', '.img', '.ccd', '.sub', '.chd',
            # Saturn
            '.iso', '.bin', '.cue', '.img', '.ccd', '.mds', '.chd',
            # Dreamcast  
            '.cdi', '.gdi', '.chd', '.iso', '.bin', '.cue',
            # Game Gear
            '.gg', '.bin', '.sms',
            # 32X
            '.32x', '.bin', '.md',
            
            # === SONY ===
            # PlayStation 1
            '.iso', '.bin', '.cue', '.img', '.ccd', '.sub', '.chd', '.pbp', '.ecm',
            # PlayStation 2
            '.iso', '.bin', '.img', '.nrg', '.cso', '.chd',
            # PlayStation Portable (PSP)
            '.iso', '.cso', '.dax', '.pbp', '.prx',
            # PlayStation Vita
            '.vpk', '.mai', '.pkg',
            # PlayStation 3
            '.pkg', '.rap', '.iso', '.ps3',
            
            # === MICROSOFT ===
            # Xbox
            '.iso', '.xbe', '.xdvdfs',
            # Xbox 360
            '.iso', '.xex', '.god', '.xcp',
            # Xbox One
            '.xvd', '.msixvc',
            
            # === ATARI ===
            # Atari 2600
            '.a26', '.bin', '.rom',
            # Atari 5200
            '.a52', '.bin', '.rom', '.car',
            # Atari 7800
            '.a78', '.bin', '.rom',
            # Atari ST
            '.st', '.msa', '.dim', '.stx',
            # Atari Lynx
            '.lyx', '.lnx', '.bin', '.rom',
            # Atari Jaguar
            '.j64', '.jag', '.rom', '.bin',
            
            # === NEC ===
            # PC Engine / TurboGrafx-16
            '.pce', '.bin', '.rom', '.sgx',
            # PC-FX
            '.iso', '.bin', '.cue', '.img',
            
            # === SNK ===
            # Neo Geo
            '.neo', '.bin', '.rom',
            # Neo Geo Pocket
            '.ngp', '.ngc', '.bin', '.rom',
            # Neo Geo CD
            '.iso', '.bin', '.cue',
            
            # === BANDAI ===
            # WonderSwan
            '.ws', '.wsc', '.bin', '.rom',
            
            # === WATARA ===
            # Supervision
            '.sv', '.bin', '.rom',
            
            # === OUTRAS HANDHELDS ===
            # Mega Duck/Cougar Boy
            '.md1', '.md2', '.bin', '.rom',
            # Game.com (Tiger Electronics)
            '.tgc', '.bin', '.rom',
            # GP32 (GamePark)
            '.gxb', '.fxe', '.bin',
            # GP2X (GamePark Holdings)
            '.gpe', '.gpu', '.bin',
            
            # === ARCADE ===
            # MAME
            '.zip', '.7z', '.rar', '.chd',
            # FinalBurn
            '.zip', '.7z', 
            # CPS1/CPS2/CPS3
            '.zip', '.7z',
            
            # === COMPUTER SYSTEMS ===
            # Commodore 64
            '.d64', '.t64', '.prg', '.p00', '.c64', '.g64', '.x64',
            # Amiga  
            '.adf', '.adz', '.dms', '.fdi', '.ipf', '.zip',
            # MSX
            '.rom', '.mx1', '.mx2', '.col', '.dsk', '.cas',
            # ZX Spectrum
            '.tap', '.tzx', '.z80', '.sna', '.szx', '.dsk',
            # Amstrad CPC
            '.dsk', '.cdt', '.voc', '.sna', '.z80',
            # Apple II
            '.dsk', '.do', '.po', '.nib', '.2mg',
            # DOS
            '.exe', '.com', '.bat', '.img', '.ima', '.vfd',
            
            # === MOBILE/HANDHELD ===
            # Game & Watch
            '.mgw', '.bin', '.rom',
            # Tiger Electronics
            '.bin', '.rom',
            # Pokémon Mini
            '.min', '.bin', '.rom',
            
            # === FORMATS GENERICI ===
            '.rom', '.bin', '.img', '.ima', '.dsk', '.tap', '.wav', '.mp3',
            '.dat', '.sav', '.cfg', '.ini', '.txt', '.nfo', '.cue', '.m3u',
            '.chd', '.cso', '.dax', '.pbp', '.ecm', '.ape', '.minipsf',
            
            # === CONSOLE VIRTUALI & FANTASY ===
            # PICO-8 (Lexaloffle)
            '.p8', '.p8.png', '.p8l',
            # WASM-4
            '.wasm', '.w4',
            # TIC-80
            '.tic',
            # LÖVE (Love2D)
            '.love',
            # Voxatron
            '.vox',
            # Splore (PICO-8 BBS)
            '.p8.png',
            # Pyxel
            '.pyxapp',
            # CHIP-8 / SCHIP / XO-CHIP
            '.ch8', '.c8h', '.sc8', '.xo8', '.chip8',
            # Octo (CHIP-8)
            '.8o',
            # Petit Computer
            '.ptc', '.prg',
            # SmileBASIC
            '.sb', '.sbx',
            # Bitsy
            '.html', '.bitsy',
            # Twine
            '.tw', '.tw2', '.twee',
            # Puzzlescript
            '.txt', '.pzl',
            # Inform 7 / Z-machine
            '.z3', '.z5', '.z8', '.zblorb', '.gblorb',
            # TADS
            '.gam', '.t3',
            # AGS (Adventure Game Studio)
            '.ags',
            # Ren'Py
            '.rpy', '.rpyc',
            # Decker
            '.deck',
            # Playdate
            '.pdx',
            
            # === FORMATI SPECIALIZZATI ===
            # Compressed Hunks of Data
            '.chd',
            # Error Code Modeller  
            '.ecm',
            # Compressed ISO
            '.cso', '.zso', '.dax',
            # Multi-file formats
            '.001', '.002', '.003', '.r00', '.r01', '.r02',
            
            # === EMULATORI SPECIFICI ===
            # RetroArch
            '.lpl', '.rpl',
            # MESS/MAME
            '.zip', '.7z', '.chd',
            # Mednafen
            '.mcf',
            # No$GBA
            '.sav', '.dsv',
            
            # === HOMEBREW & INDIE PLATFORMS ===
            # Lua-based engines
            '.lua', '.luac',
            # JavaScript games
            '.js', '.json', '.html', '.htm',
            # Flash (legacy)
            '.swf', '.fla',
            # Java games
            '.jar', '.jad',
            # Game Boy homebrew
            '.gb', '.gbc', '.gba', '.pocket',
            # Arduboy
            '.hex', '.arduboy',
            # ESP32/Arduino games
            '.bin', '.uf2',
            
            # === WEB & MODERN FORMATS ===
            # WebAssembly games
            '.wasm', '.wat',
            # PWA/WebGL games  
            '.html', '.js', '.wasm',
            # Electron games
            '.asar',
            # Unity WebGL
            '.unity3d', '.unityweb',
        }
        
        # Scansione ottimizzata con conteggio in tempo reale
        self.log(self.get_text('scanning_folders'))
        total_files_to_check = 0
        scanned_folders = set()
        folder_count = 0
        
        # Prima passata: conta cartelle per stimare il progresso
        for root, dirs, files in os.walk(folder):
            folder_count += 1
            
        self.log(self.get_text('folders_found').format(folder_count))
        
        # Seconda passata: conta file con progress in tempo reale
        current_folder = 0
        for root, dirs, files in os.walk(folder):
            current_folder += 1
            
            # Mostra progresso cartelle
            relative_path = os.path.relpath(root, folder)
            if relative_path not in scanned_folders and relative_path != '.':
                self.log(f"  📂 [{current_folder}/{folder_count}] {relative_path}")
                scanned_folders.add(relative_path)
            elif relative_path == '.':
                self.log(f"  📂 [{current_folder}/{folder_count}] Cartella principale")
            
            # Conta file ROM in questa cartella
            files_in_folder = 0
            for file in files:
                if any(file.lower().endswith(ext) for ext in rom_extensions):
                    total_files_to_check += 1
                    files_in_folder += 1
            
            if files_in_folder > 0:
                self.log(f"     📄 {files_in_folder} file ROM trovati (totale: {total_files_to_check})")
            
            # Aggiorna progress bar (primi 25% per conteggio)
            progress_percent = (current_folder / folder_count) * 25
            self.update_progress(progress_percent)
            self.update_ui()  # Mantieni responsiva l'UI
        
        folders_count = len(scanned_folders) + 1  # +1 per la cartella principale
        self.log(self.get_text('roms_found_total').format(total_files_to_check, folders_count))
        
        if total_files_to_check == 0:
            self.log(self.get_text('no_roms_found'))
            self.reset_progress()
            self.clean_button.config(state='disabled')
            return
        
        # Raccolta file ROM con progress dettagliato
        self.log(self.get_text('collecting_roms'))
        rom_files = []
        processed = 0
        current_folder = ""
        files_per_update = max(1, total_files_to_check // 100)  # Aggiorna ogni 1% o almeno ogni file
        
        for root, dirs, files in os.walk(folder):
            # Mostra la cartella corrente durante la scansione
            relative_path = os.path.relpath(root, folder)
            if relative_path != current_folder:
                current_folder = relative_path
                folder_display = "cartella principale" if current_folder == '.' else current_folder
                self.log(f"  🔍 Raccogliendo da: {folder_display}")
            
            files_in_this_folder = 0
            for file in files:
                if any(file.lower().endswith(ext) for ext in rom_extensions):
                    rom_files.append(os.path.join(root, file))
                    processed += 1
                    files_in_this_folder += 1
                    
                    # Aggiorna progress ogni file o gruppo di file
                    if processed % files_per_update == 0 or processed == total_files_to_check:
                        # Progress bar 25-60% per la raccolta file
                        progress_percent = 25 + ((processed / total_files_to_check) * 35)
                        self.update_progress(progress_percent)
                        
                        # Aggiorna log con conteggio preciso
                        if processed % (files_per_update * 10) == 0 or processed == total_files_to_check:
                            self.log(f"     📊 Raccolti {processed}/{total_files_to_check} file ROM ({progress_percent:.1f}%)")
                        
                        self.update_ui()
            
            # Log per cartelle con molti file
            if files_in_this_folder > 10:
                self.log(f"     ✅ {files_in_this_folder} file ROM in questa cartella")
                    
        self.log(self.get_text('scan_completed_files').format(len(rom_files)))
        
        # Raggruppa per nome base con progress dettagliato
        self.log(self.get_text('analyzing_duplicates'))
        groups = defaultdict(list)
        analysis_per_update = max(1, len(rom_files) // 50)  # Aggiorna ogni 2% o almeno ogni file
        
        for i, filepath in enumerate(rom_files):
            filename = os.path.basename(filepath)
            base_name = self.extract_base_name(filename)
            if base_name:  # Ignora nomi vuoti
                groups[base_name].append(filepath)
            
            # Aggiorna progress ogni gruppo di file
            if (i + 1) % analysis_per_update == 0 or i == len(rom_files) - 1:
                # Progress bar 60-80% per l'analisi (ridotto per lasciare spazio al report)
                progress_percent = 60 + ((i + 1) / len(rom_files)) * 20
                self.update_progress(progress_percent)
                
                # Log periodico per mostrare progresso
                if (i + 1) % (analysis_per_update * 5) == 0 or i == len(rom_files) - 1:
                    self.log(f"  📊 Analizzati {i + 1}/{len(rom_files)} file ({progress_percent:.1f}%)")
                
                self.update_ui()
                
        # Applica logica DAT MAME intelligente
        self.log("🎮 Applicando logica DAT MAME...")
        self.update_progress(82)
        self.update_ui()
        
        # Analisi intelligente con protezione BIOS/Parent
        protected_files = set()
        smart_duplicates = {}
        smart_singles = {}
        
        for base_name, file_list in groups.items():
            if base_name in self.bios_games:
                # BIOS: proteggi tutti
                for i, filepath in enumerate(file_list):
                    protected_files.add(filepath)
                    smart_singles[f"{base_name}_bios_{i}"] = [filepath]
                self.log(f"  🔒 BIOS protetto: {base_name} ({len(file_list)} file)")
            elif base_name in self.parent_games:
                # Parent: proteggi tutti  
                for i, filepath in enumerate(file_list):
                    protected_files.add(filepath)
                    smart_singles[f"{base_name}_parent_{i}"] = [filepath]
                self.log(f"  🔒 Parent protetto: {base_name} ({len(file_list)} file)")
            elif len(file_list) > 1:
                smart_duplicates[base_name] = file_list
            else:
                smart_singles[base_name] = file_list
        
        self.duplicates = smart_duplicates
        self.singles = smart_singles
        
        # Progress 82-85% per identificazione
        self.update_progress(85)
        self.update_ui()
        
        total_to_process = len(self.duplicates) + len(self.singles)
        
        if total_to_process == 0:
            self.log(self.get_text('no_rom_files'))
            self.clean_button.config(state='disabled')
            self.reset_progress()
            return
            
        self.log(self.get_text('analysis_complete'))
        self.log(self.get_text('duplicate_groups').format(len(self.duplicates)))
        self.log(self.get_text('single_files').format(len(self.singles)))
        
        # Progress 85% - Inizio generazione report
        self.update_progress(87)
        self.update_ui()
        
        # Prima mostra i file singoli (già puliti)
        if self.singles:
            self.log(self.get_text('single_files_header').format(len(self.singles)))
            
            # Calcola aggiornamenti per i singoli
            singles_per_update = max(1, len(self.singles) // 10)
            
            for i, (game_name, files) in enumerate(self.singles.items()):
                filepath = files[0]  # Un solo file per definizione
                filename = os.path.basename(filepath)
                
                # Controlla se è un gioco multi-disco
                is_multi_disk = re.search(r'(disk|disc|cd|part|side|tape|floppy)\s*\d+', 
                                        filename, re.IGNORECASE)
                disk_icon = "💿" if is_multi_disk else "📄"
                
                geo_info = self.get_geographic_info(filename)
                quality_info = self.get_quality_info(filename)
                details = f"({geo_info}{quality_info})"
                
                self.log(f"{disk_icon} {game_name}")
                self.log(f"  {self.get_text('unique_file')} {filename} {details}")
                
                # Aggiorna progresso ogni gruppo di singoli
                if (i + 1) % singles_per_update == 0 or i == len(self.singles) - 1:
                    # Progress 87-90% per i singoli
                    progress_percent = 87 + ((i + 1) / len(self.singles)) * 3
                    self.update_progress(progress_percent)
                    self.update_ui()
        
        # Progress 90% - Singoli completati
        self.update_progress(90)
        self.update_ui()
        
        # Poi mostra i duplicati
        total_duplicates = 0
        multi_disk_games = 0
        
        if self.duplicates:
            self.log(self.get_text('duplicate_groups_header').format(len(self.duplicates)))
            
            # Calcola aggiornamenti per i duplicati
            duplicates_per_update = max(1, len(self.duplicates) // 10)
            
        for i, (game_name, files) in enumerate(self.duplicates.items()):
            total_duplicates += len(files)
            
            # Controlla se è un gioco multi-disco
            is_multi_disk = any(re.search(r'(disk|disc|cd|part|side|tape|floppy)\s*\d+', 
                                        os.path.basename(f), re.IGNORECASE) for f in files)
            
            if is_multi_disk:
                multi_disk_games += 1
                disk_icon = "💿"
            else:
                disk_icon = "📁"
                
            self.log(f"\n{disk_icon} {game_name} ({len(files)} {self.get_text('versions_count')}):")
            
            if is_multi_disk:
                self.log(f"   {self.get_text('multi_disk_warning')}")
            
            # Calcola priorità per ogni file
            file_priorities = []
            for filepath in files:
                filename = os.path.basename(filepath)
                priority = self.calculate_priority(filename)
                file_priorities.append((filepath, filename, priority))
                
            # Ordina per priorità (più alta prima)
            file_priorities.sort(key=lambda x: x[2], reverse=True)
            
            # Mostra l'ordine con dettagli di priorità
            for i, (filepath, filename, priority) in enumerate(file_priorities):
                status = self.get_text('keep_file') if i == 0 else self.get_text('remove_file')
                geo_info = self.get_geographic_info(filename)
                quality_info = self.get_quality_info(filename)
                details = f"({geo_info}{quality_info})"
                self.log(f"  {status} - {filename} {details} (priorità: {priority})")
                
            # Aggiorna progresso ogni gruppo di duplicati
            if (i + 1) % duplicates_per_update == 0 or i == len(self.duplicates) - 1:
                # Progress 90-95% per i duplicati
                progress_percent = 90 + ((i + 1) / len(self.duplicates)) * 5
                self.update_progress(progress_percent)
                self.update_ui()
                
        # Progress 95% - Duplicati completati, inizia riepilogo finale
        self.update_progress(95)
        self.update_ui()
                
        files_to_move = len(self.duplicates) + len(self.singles)  # Migliori + Singoli
        singles_count = len(self.singles)
        remaining_duplicates = total_duplicates - len(self.duplicates) if total_duplicates > 0 else 0
        
        self.log(self.get_text('summary_complete'))
        self.log(self.get_text('summary_singles').format(singles_count))
        self.log(self.get_text('summary_duplicates').format(len(self.duplicates)))
        if multi_disk_games > 0:
            self.log(self.get_text('summary_multi_disk').format(multi_disk_games))
        self.log(self.get_text('summary_total_analyzed').format(total_duplicates + singles_count))
        self.log(self.get_text('summary_files_to_move').format(files_to_move))
        if remaining_duplicates > 0:
            self.log(self.get_text('summary_remaining_dupes').format(remaining_duplicates))
        
        if multi_disk_games > 0:
            self.log(f"\n{self.get_text('multi_disk_attention').format(multi_disk_games)}")
            self.log(self.get_text('multi_disk_separate'))
            
        self.log(f"\n{self.get_text('cleaned_summary').format(singles_count, len(self.duplicates), files_to_move)}")
        
        # Completa progress bar al 100% e poi resetta
        self.update_progress(100)
        self.update_ui()
        
        self.clean_button.config(state='normal')
        
        # Reset progress bar dopo un breve momento
        self.reset_progress()
        
    def clean_duplicates(self):
        """Sposta le ROM migliori e i file singoli nella cartella 'cleaned'"""
        if not self.duplicates and not hasattr(self, 'singles'):
            messagebox.showwarning("Attenzione", "Esegui prima una scansione!")
            return
        
        if not self.duplicates and not self.singles:
            messagebox.showwarning("Attenzione", "Nessun file da processare!")
            return
            
        folder = self.folder_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Errore", "Cartella non valida!")
            return
            
        dry_run = self.dry_run_var.get()
        show_kept = self.show_kept_var.get()
        copy_mode = self.copy_mode_var.get()
        
        # Crea cartella cleaned
        cleaned_folder = os.path.join(folder, "cleaned")
        
        mode_text = "MODALITÀ TEST" if dry_run else "MODALITÀ REALE"
        action_text = "COPIA" if copy_mode else "SPOSTA"
        self.log(f"\n=== Inizio organizzazione ROM - {mode_text} ({action_text}) ===")
        self.log(f"📁 Cartella destinazione: {cleaned_folder}")
        
        if dry_run:
            self.log(f"⚠️  I file NON verranno realmente {action_text.lower()}ti")
        else:
            result = messagebox.askyesno(
                "Conferma", 
                f"Sei sicuro di voler {action_text.lower()} le ROM migliori nella cartella 'cleaned'?\n"
                f"Cartella destinazione: {cleaned_folder}",
                icon='question'
            )
            if not result:
                self.log(self.get_text('operation_cancelled'))
                return
                
        # Imposta barra di progresso determinata
        total_operations = len(self.duplicates) + (len(self.singles) if hasattr(self, 'singles') else 0)
        self.reset_progress()
        self.update_ui()
        
        moved_count = 0
        kept_count = 0
        errors = 0
        
        # Crea cartella cleaned se non esiste
        if not dry_run:
            try:
                os.makedirs(cleaned_folder, exist_ok=True)
                self.log(f"✅ Cartella 'cleaned' creata/verificata")
            except Exception as e:
                self.log(f"❌ ERRORE creando cartella 'cleaned': {str(e)}")
                self.reset_progress()
                return
        
        completed_operations = 0
        singles_update_freq = max(1, len(self.singles) // 20) if hasattr(self, 'singles') else 1
        duplicates_update_freq = max(1, len(self.duplicates) // 20) if self.duplicates else 1
        
        # Prima processa i file singoli (già puliti)
        if hasattr(self, 'singles') and self.singles:
            self.log(f"\n💎 Processando {len(self.singles)} file singoli (già puliti)...")
            
            singles_processed = 0
            for game_name, files in self.singles.items():
                singles_processed += 1
                
                # Aggiorna progress bar con frequenza intelligente
                if singles_processed % singles_update_freq == 0 or singles_processed == len(self.singles):
                    progress_percent = (completed_operations / total_operations) * 100
                    self.update_progress(progress_percent)
                    
                    # Log periodico
                    if singles_processed % (singles_update_freq * 3) == 0 or singles_processed == len(self.singles):
                        self.log(f"  📊 Processati {singles_processed}/{len(self.singles)} file singoli")
                    
                    self.update_ui()
                
                single_file = files[0]  # Un solo file per definizione
                filename = os.path.basename(single_file)
                destination = os.path.join(cleaned_folder, filename)
                
                if not dry_run:
                    try:
                        if copy_mode:
                            shutil.copy2(single_file, destination)
                            action_done = "COPIATO"
                        else:
                            shutil.move(single_file, destination)
                            action_done = "SPOSTATO"
                        
                        moved_count += 1
                        geo_info = self.get_geographic_info(filename)
                        quality_info = self.get_quality_info(filename)
                        self.log(f"✨ {action_done} SINGOLO: {filename} {geo_info}{quality_info}")
                        
                    except Exception as e:
                        self.log(f"❌ ERRORE {action_text.lower()}ando {filename}: {str(e)}")
                        errors += 1
                else:
                    moved_count += 1
                    geo_info = self.get_geographic_info(filename)
                    quality_info = self.get_quality_info(filename)
                    self.log(f"✨ DA {action_text} SINGOLO: {filename} {geo_info}{quality_info}")
                
                completed_operations += 1
        
        # Poi processa i duplicati
        if self.duplicates:
            self.log(f"\n🔄 Processando {len(self.duplicates)} gruppi di duplicati...")
            
        duplicates_processed = 0
        for game_name, files in self.duplicates.items():
            duplicates_processed += 1
            
            # Aggiorna progress bar con frequenza intelligente
            if duplicates_processed % duplicates_update_freq == 0 or duplicates_processed == len(self.duplicates):
                progress_percent = (completed_operations / total_operations) * 100
                self.update_progress(progress_percent)
                
                # Log periodico
                if duplicates_processed % (duplicates_update_freq * 2) == 0 or duplicates_processed == len(self.duplicates):
                    self.log(f"  📊 Processati {duplicates_processed}/{len(self.duplicates)} gruppi duplicati")
                
                self.update_ui()
            
            # Calcola priorità per ogni file
            file_priorities = []
            for filepath in files:
                filename = os.path.basename(filepath)
                priority = self.calculate_priority(filename)
                file_priorities.append((filepath, filename, priority))
                
            # Ordina per priorità (più alta prima)
            file_priorities.sort(key=lambda x: x[2], reverse=True)
            
            # Sposta/copia il migliore nella cartella cleaned
            best_file = file_priorities[0]
            best_filepath, best_filename, best_priority = best_file
            
            destination = os.path.join(cleaned_folder, best_filename)
            
            if not dry_run:
                try:
                    if copy_mode:
                        shutil.copy2(best_filepath, destination)
                        action_done = "COPIATO"
                    else:
                        shutil.move(best_filepath, destination)
                        action_done = "SPOSTATO"
                    
                    moved_count += 1
                    geo_info = self.get_geographic_info(best_filename)
                    quality_info = self.get_quality_info(best_filename)
                    self.log(f"📦 {action_done}: {best_filename} {geo_info}{quality_info}")
                    
                except Exception as e:
                    self.log(f"❌ ERRORE {action_text.lower()}ando {best_filename}: {str(e)}")
                    errors += 1
            else:
                moved_count += 1
                geo_info = self.get_geographic_info(best_filename)
                quality_info = self.get_quality_info(best_filename)
                self.log(f"📦 DA {action_text}: {best_filename} {geo_info}{quality_info}")
            
            # Mostra gli altri file che rimarranno nella cartella originale
            if show_kept and len(file_priorities) > 1:
                for i in range(1, len(file_priorities)):
                    _, other_filename, other_priority = file_priorities[i]
                    self.log(f"   📁 RIMANE: {other_filename}")
                    kept_count += 1
            
            completed_operations += 1
        
        # Completa progress bar
        self.update_progress(100)
        self.update_ui()
        
        self.log(f"\n📊 Operazione completata:")
        self.log(f"   • ROM migliori {action_text.lower()}te in 'cleaned': {moved_count}")
        self.log(f"   • ROM rimaste nella cartella originale: {kept_count}")
        if errors > 0:
            self.log(f"   • Errori: {errors}")
            
        if not dry_run:
            messagebox.showinfo("Completato", 
                              f"Organizzazione completata!\n"
                              f"ROM migliori {action_text.lower()}te: {moved_count}\n"
                              f"ROM rimaste: {kept_count}\n"
                              f"Controlla la cartella: {cleaned_folder}")
        else:
            messagebox.showinfo("Test completato", 
                              f"Simulazione completata!\n"
                              f"ROM che verrebbero {action_text.lower()}te: {moved_count}\n"
                              f"ROM che rimarrebbero: {kept_count}")
        
        # Reset progress bar
        self.reset_progress()
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RomCleaner()
    app.run()
