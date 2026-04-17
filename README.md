# Remote Controller

Een mobiele web-app om je pc op afstand te bedienen via een WebSocket-verbinding.  
De interface draait in de browser op je telefoon, terwijl een Python-server op je computer de muis-, toetsenbord- en scroll-acties uitvoert.

Deze versie bevat onder andere:

- muisbesturing met joystick
- linkerklik, rechtermuisklik en dubbelklik
- sleepbare scrollbalk in de linker bedieningsbox
- toetsenbordinvoer en speciale toetsen
- sneltoetsen zoals `Ctrl+C`, `Alt+Tab`, `Win+D`
- een aparte **Vergrendel**-knop die Windows direct vergrendelt

De frontend gebruikt `controller.html` en `style.css`, en de backend draait via `server.py`. 

---

## Bestanden

- `controller.html` – de webinterface met tabs, muis, toetsenbord en sneltoetsen. 
- `style.css` – alle styling voor layout, knoppen, slider en mobiele weergave.
- `server.py` – de WebSocket-server die acties ontvangt en uitvoert met `pyautogui`.

---

## Vereisten

Zorg dat dit op je computer is geïnstalleerd:

- Python 3.10 of nieuwer
- een Windows-pc
- telefoon en computer op hetzelfde netwerk
- Python-pakketten:
  - `websockets`
  - `pyautogui`

Installeer de pakketten met:

```bash
pip install websockets pyautogui
```

---

## Projectstructuur

```text
projectmap/
├── controller.html
├── style.css
└── server.py
```

---

## Starten

### 1. Start de Python-server

Open een terminal of opdrachtprompt in je projectmap en voer uit:

```bash
python server.py
```

Je ziet dan iets zoals:

```text
WebSocket server starting on ws://0.0.0.0:8765
Server running. Press Ctrl+C to stop.
```

De server luistert standaard op poort `8765`. Dit staat ook zo ingesteld in de frontend.

### 2. Open de webinterface

Open `controller.html` in een browser op je telefoon.

Belangrijk:
- je telefoon moet de computer kunnen bereiken via het lokale netwerk
- de WebSocket-URL wordt opgebouwd met `location.hostname` en poort `8765`

Dat betekent in de praktijk meestal dat je de pagina serveert vanaf je pc en daarna op je telefoon opent via het IP-adres van je computer, bijvoorbeeld:

```text
http://192.168.1.25/controller.html
```

### 3. Controleer de verbinding

Als alles goed gaat:
- verdwijnt de overlay
- springt de status op **Verbonden**
- kun je direct de pc bedienen vanuit je telefooninterface.

---

## Functies

## Muis

In de tab **Muis** kun je:

- de cursor bewegen met de joystick
- een gewone linkerklik doen
- een rechtermuisklik doen
- een dubbelklik doen
- in het joystickvlak dubbel tikken / dubbelklikken voor een gewone linkerklik

## Scrollen

De verticale slider in de linkerbox stuurt een `scrollbar_start`, `scrollbar_move` en `scrollbar_end` actie naar de server.  
De Python-server vertaalt die positie naar een echte schermpositie aan de rechterkant van het scherm en sleept daar de scrollbar.

Daardoor geldt:

- slider bovenaan = pagina bovenaan
- slider onderaan = pagina onderaan

### Belangrijk bij scrollen

Deze aanpak werkt het best wanneer:

- de app of browser op je pc een zichtbare verticale scrollbar heeft
- die scrollbar rechts op het scherm staat
- de vensterindeling niet te veel afwijkt van normaal


## Toetsenbord

In de tab **Toetsen** kun je:

- gewone tekst typen
- tekst verzenden naar de pc
- speciale toetsen gebruiken zoals:
  - Enter
  - Backspace
  - Tab
  - Escape
  - Spatie
  - Delete
  - pijltjestoetsen 

De server verwerkt dit met `pyautogui.keyDown`, `keyUp` en `write`. fileciteturn0file1

---

## Sneltoetsen

In de tab **Sneltoetsen** zitten onder andere:

- `Ctrl+C`
- `Ctrl+V`
- `Ctrl+X`
- `Ctrl+Z`
- `Ctrl+Y`
- `Ctrl+A`
- `Ctrl+S`
- `Ctrl+F`
- `Alt+Tab`
- `Alt+F4`
- `Win`
- `Ctrl+Shift+Escape`
- `PrintScreen`
- `Win+D`
- `Win+E`

---

## Vergrendelknop

De knop **Vergrendel** gebruikt niet `Win + L` via een gewone hotkey, maar een aparte `lock`-actie.  
Aan de serverkant wordt daarvoor `ctypes.windll.user32.LockWorkStation()` gebruikt. Dat is op Windows betrouwbaarder dan `pyautogui.hotkey("win", "l")`.

---

## Belangrijke instellingen

### In `controller.html`

De frontend gebruikt:

```javascript
const WS_PORT = 8765;
const WS_URL = `ws://${location.hostname || 'localhost'}:${WS_PORT}`;
```

Dus de browser probeert te verbinden met dezelfde host als waar de pagina vandaan geladen is, op poort `8765`. 

### In `server.py`

De server luistert op:

```python
host = "0.0.0.0"
port = 8765
```

Daardoor is de server bereikbaar op alle netwerkinterfaces van je computer, zolang firewall en netwerk dat toelaten. 

---

## Problemen oplossen

## Verbindt niet

Controleer:

- draait `server.py` nog?
- zitten telefoon en pc op hetzelfde wifi-netwerk?
- staat poort `8765` niet geblokkeerd door Windows Firewall?
- open je de pagina via het IP-adres van je computer, en niet alleen lokaal op je telefoon?


## Veiligheid

Deze tool geeft remote bediening van je computer zonder extra authenticatie.  
Gebruik hem daarom alleen:

- op je eigen netwerk
- op apparaten die je vertrouwt
- niet openbaar via internet zonder extra beveiliging

Dat is belangrijk, omdat elke client die verbinding maakt met de WebSocket-server acties kan sturen die direct op je pc worden uitgevoerd. Dit volgt uit de serveropzet in `server.py`.
