"""Entry point für Blender.

Warum diese Datei?
- In Blender wird oft wiederholt "Run Script" gedrückt.
- Damit Änderungen in Modulen sofort aktiv sind, laden wir die Module per importlib.reload neu.
- Zusätzlich stellen wir sicher, dass der Projektordner in ``sys.path`` liegt,
  damit ``scene_project`` sowohl aus der GUI als auch per CLI zuverlässig importiert wird.
"""

import importlib
import sys
from pathlib import Path


def _ensure_project_root_in_syspath() -> Path:
    """Fügt den Projektordner zu ``sys.path`` hinzu (falls nötig).

    Reihenfolge der Kandidaten:
    1. Ordner der aktuell geöffneten ``.blend``-Datei (falls gespeichert)
    2. Ordner dieses Scripts

    Returns:
        Verwendeter Projektordner.
    """

    project_root = Path(__file__).resolve().parent

    # ``bpy`` ist nur in Blender verfügbar.
    try:
        import bpy  # type: ignore

        blend_dir = bpy.path.abspath("//")
        if blend_dir and blend_dir != "//":
            candidate = Path(blend_dir).resolve()
            if (candidate / "scene_project").exists():
                project_root = candidate
    except Exception:
        # Fallback für Ausführung außerhalb von Blender.
        pass

    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

    return project_root


_ensure_project_root_in_syspath()

import scene_project.camera as camera
import scene_project.config as config
import scene_project.lights as lights
import scene_project.main as main
import scene_project.materials as materials
import scene_project.objects as objects

# Module in kontrollierter Reihenfolge neu laden (Dependencies zuerst)
for module in (materials, objects, lights, camera, config, main):
    importlib.reload(module)

# Szene bauen
main.build_scene(config.SceneConfig())
