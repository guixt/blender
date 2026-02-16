# Blender AI Scene Starter

Dieses Repository ist ein minimaler Starter, um Blender-Szenen **iterativ per Python** aufzubauen.

## Ziel

- Erste Version: Nur Python-Skripte (ohne komplexes Addon/Server)
- Iterativ erweitern: Jede Runde neue Funktionen, neue Objekte, neue Materialien
- Klare Modulstruktur, damit KI und Mensch gemeinsam schnell arbeiten können

## Projektstruktur

```text
.
├── run_in_blender.py
├── scene_project
│   ├── __init__.py
│   ├── camera.py
│   ├── config.py
│   ├── lights.py
│   ├── main.py
│   ├── materials.py
│   └── objects.py
└── README.md
```

## Voraussetzungen

- Blender 3.x
- Python innerhalb von Blender (wird automatisch mitgeliefert)

## So startest du das Skript

### Variante A: Über Blender GUI
1. Blender öffnen.
2. `Scripting` Workspace öffnen.
3. `run_in_blender.py` laden.
4. `Run Script` klicken.

> Ohne zusätzliche Parameter wird die Standard-Szene `forest` gebaut.

### Variante B: Über CLI

```bash
blender --factory-startup --python run_in_blender.py
```

**Szenenauswahl per Parameter:**

```bash
blender --factory-startup --python run_in_blender.py -- --scene city
```

Alternativ:

```bash
blender --factory-startup --python run_in_blender.py -- --scene=forest
```

> `--factory-startup` sorgt für einen sauberen Start ohne alte User-Settings.

## Verfügbare Szenen

- `forest`: Erweiterte Naturszene (Boden + Baum-Cluster + Felsen + Büsche + Teich).
- `city`: Neues Beispiel für eine futuristische Stadt (dunkler Boden + Tower-Grid).

## Iterativer Workflow (empfohlen)

1. **Neue Idee definieren** (z. B. "mehr Neon", "mehr Props", "Fog").
2. Funktion in passendem Modul ergänzen (`objects.py`, `materials.py`, ...).
3. In `scene_project/main.py` Builder ergänzen oder erweitern.
4. `run_in_blender.py` neu ausführen (mit optionalem `--scene ...`).
5. Ergebnis prüfen und nächste Iteration planen.

## "Includes" in Python

Python hat keine `#include`-Direktiven wie C/C++. Das Äquivalent sind Imports:

```python
from scene_project.objects import add_ground
from scene_project.lights import setup_sun_light
```

Für häufiges Neu-Ausführen in Blender nutzt `run_in_blender.py` automatisch `importlib.reload(...)`,
damit Änderungen in den Modulen sofort wirksam werden.

## Häufiger Fehler in Blender: `ModuleNotFoundError: scene_project`

Falls Blender meldet, dass `scene_project` nicht gefunden wird, lag bisher meist der
Projektordner nicht im Python-Suchpfad. `run_in_blender.py` ergänzt den passenden
Projektpfad jetzt automatisch (Blend-Datei-Ordner oder Script-Ordner als Fallback).

Wenn es trotzdem auftritt:
- Prüfen, dass `scene_project/__init__.py` existiert.
- Die `.blend` speichern, damit Blender einen stabilen Projektordner hat.
- Sicherstellen, dass `run_in_blender.py` aus diesem Repository geladen wurde.

## Nächste sinnvolle Erweiterungen

- Eigene Licht-Presets pro Szene (`city_night`, `sunset_forest`, ...)
- Emission-Materialien + volumetrischer Nebel für mehr Cyberpunk-Look
- Export von `scene_summary` als JSON für KI-Feedback pro Iteration
- Optional später: Addon + API + Action-Whitelist
